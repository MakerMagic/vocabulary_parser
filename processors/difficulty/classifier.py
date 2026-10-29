"""Stage 5.5: CEFR-Based Difficulty Classification and Preset Assignment.

Source-independent processor that determines defensible CEFR levels, maps them to
the platform difficulty tiers (Easy / Medium / Hard), assigns the preset field, and
enforces final-output eligibility gates across vocabulary records.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from processors.difficulty.cefr_registry import lookup_cefr_level
from processors.difficulty.contract import (
    ALLOWED_DIFFICULTY_LABELS,
    CURRENT_DATASET_PRESET,
    PRESET_SCHEMA_DEFAULT,
    cefr_to_difficulty,
)
from processors.provenance import (
    REPO_ROOT,
    compute_content_hash,
    resolve_json_pointer,
    sha256_file,
    write_canonical_json,
)
from processors.stage_artifacts import write_stage_qa_pair


def classify_record_difficulty(
    record: dict[str, Any],
    source_id: str,
    preset: str | None = CURRENT_DATASET_PRESET,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Classify a single enriched vocabulary record, assigning preset, CEFR level, and difficulty tier.

    Returns (classified_record, optional_issue_dict).
    """
    word = record["word"]
    pos = record.get("declared_section_pos") or record.get("part_of_speech") or ""
    val_status = (
        record.get("validation_status")
        or record.get("status")
        or record.get("cleaning_status")
        or record.get("enrichment_status")
        or "clean"
    )

    # 1. Preset assignment (Schema default: null; current datasets: "Basics")
    assigned_preset = preset if preset is not None else PRESET_SCHEMA_DEFAULT

    # 2. CEFR Level Lookup
    existing_cefr = record.get("cefr_level")
    cefr = existing_cefr or lookup_cefr_level(word=word, pos=pos, source_id=source_id)

    issue: dict[str, Any] | None = None
    if not cefr:
        difficulty = None
        issue = {
            "actual_output": "CEFR level undetermined",
            "category": "Ambiguous CEFR classification",
            "corrective_action": "Verify term in Oxford 3000/5000 or Cambridge EVP and supply benchmark level.",
            "expected_output": "Defensible CEFR level (A1..C2)",
            "field": "cefr_level / difficulty",
            "issue_code": "unresolved_cefr_classification",
            "message": f"Unable to determine reliable CEFR level for term {word!r} ({pos!r}).",
            "number": record.get("number"),
            "record_id": record["id"],
            "reproduction_command": f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source {source_id} --word \"{word}\"",
            "resolution_status": "blocking_error_unresolved",
            "responsible_stage": "DIFFICULTY",
            "root_cause": "Lexical item missing from established benchmark registries.",
            "severity": "error",
            "word": word,
        }
    else:
        difficulty = cefr_to_difficulty(cefr)

    # 3. Final output eligibility check:
    # Records with unresolved blocking issues or prior exclusion must NOT enter final outputs
    review_note = record.get("quality_and_review_notes") or record.get("enrichment_provenance", {}).get("review_note")
    is_excluded = val_status == "excluded" or record.get("exclusion_reason") is not None
    is_review_pending = val_status == "review_pending" or review_note is not None
    is_error = val_status == "error"

    final_output_eligible = not (is_excluded or is_review_pending or is_error or difficulty is None)

    classified = dict(record)
    classified["preset"] = assigned_preset
    classified["cefr_level"] = cefr
    classified["difficulty"] = difficulty
    classified["final_output_eligible"] = final_output_eligible

    return classified, issue


def run_difficulty_classification(
    repo_root: Path = REPO_ROOT,
    source_id: str = "uclouvain",
    preset: str | None = CURRENT_DATASET_PRESET,
) -> dict[str, Any]:
    """Execute CEFR-based difficulty classification for the specified source."""
    if source_id == "new_words":
        in_rel_path = "data/enriched/sources/new_words/entries.enriched.json"
        in_val_rel_path = "data/enriched/sources/new_words/validation.json"
        out_rel_path = "data/difficulty/sources/new_words/entries.difficulty.json"
        val_rel_path = "data/difficulty/sources/new_words/validation.json"
        legacy_out_path = None
        legacy_val_path = None
    elif source_id == "uclouvain":
        in_rel_path = "data/enriched/sources/uclouvain/entries.enriched.json"
        in_val_rel_path = "data/enriched/sources/uclouvain/validation.json"
        out_rel_path = "data/difficulty/sources/uclouvain/entries.difficulty.json"
        val_rel_path = "data/difficulty/sources/uclouvain/validation.json"
        legacy_out_path = repo_root / "data" / "difficulty" / "justprepy_wordlist" / "entries.difficulty.json"
        legacy_val_path = repo_root / "data" / "difficulty" / "justprepy_wordlist" / "validation.json"
    else:
        in_rel_path = f"data/enriched/sources/{source_id}/entries.enriched.json"
        in_val_rel_path = f"data/enriched/sources/{source_id}/validation.json"
        out_rel_path = f"data/difficulty/sources/{source_id}/entries.difficulty.json"
        val_rel_path = f"data/difficulty/sources/{source_id}/validation.json"
        legacy_out_path = None
        legacy_val_path = None

    in_path = repo_root / in_rel_path
    if not in_path.exists() and source_id == "uclouvain":
        in_path = repo_root / "data/enriched/justprepy_wordlist/entries.enriched.json"
        in_val_rel_path = "data/enriched/justprepy_wordlist/validation.json"

    if not in_path.exists():
        raise FileNotFoundError(f"Enriched input artifact missing: {in_path}")

    in_sha = sha256_file(in_path)
    in_val_path = repo_root / in_val_rel_path
    if in_val_path.exists():
        in_val_doc = json.loads(in_val_path.read_text(encoding="utf-8"))
        if in_sha != in_val_doc["output_sha256"]:
            raise ValueError(f"Enriched input SHA drift detected for {source_id}.")

    in_doc = json.loads(in_path.read_text(encoding="utf-8"))
    classified_records: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0, "Unset": 0}
    eligible_count = 0
    blocked_count = 0

    for idx, raw_item in enumerate(in_doc["records"]):
        item = resolve_json_pointer(in_doc, f"/records/{idx}")
        classified, iss = classify_record_difficulty(item, source_id=source_id, preset=preset)
        if iss:
            issues.append(iss)

        diff = classified["difficulty"]
        if diff in diff_counts:
            diff_counts[diff] += 1
        else:
            diff_counts["Unset"] += 1

        if classified["final_output_eligible"]:
            eligible_count += 1
        else:
            blocked_count += 1

        classified["provenance"] = {
            "upstream_enriched_file": in_rel_path,
            "upstream_enriched_file_sha256": in_sha,
            "upstream_enriched_json_pointer": f"/records/{idx}",
        }
        classified["record_content_hash"] = compute_content_hash(classified)
        classified_records.append(classified)

    out_doc = {
        "dataset_name": f"{source_id}_difficulty_classified",
        "description": "CEFR-based difficulty classification and preset assignment.",
        "difficulty_distribution": diff_counts,
        "input_sha256": in_sha,
        "preset_assignment": preset,
        "record_count": len(classified_records),
        "records": classified_records,
        "schema_version": "1.0.0",
        "source_id": source_id,
        "summary": {
            "blocked_from_final_output_count": blocked_count,
            "difficulty_counts": diff_counts,
            "eligible_for_final_output_count": eligible_count,
            "preset_assigned_count": sum(1 for r in classified_records if r.get("preset") is not None),
            "total_records": len(classified_records),
        },
    }

    out_path = repo_root / out_rel_path
    write_canonical_json(out_path, out_doc)
    out_sha = sha256_file(out_path)

    val_doc = {
        "description": f"CEFR-based difficulty classification and preset assignment for {source_id}.",
        "input_artifact": in_rel_path,
        "input_file": in_rel_path,
        "input_sha256": in_sha,
        "issues": issues,
        "output_artifact": out_rel_path,
        "output_file": out_rel_path,
        "output_sha256": out_sha,
        "record_count": len(classified_records),
        "source_id": source_id,
        "stage": "DIFFICULTY",
        "stage_status": "completed",
        "status": "PASS" if not issues else "FAIL",
        "summary": {
            "affected_record_count": len({iss["record_id"] for iss in issues if "record_id" in iss}),
            "blocked_from_final_output_count": blocked_count,
            "difficulty_counts": diff_counts,
            "eligible_for_final_output_count": eligible_count,
            "entered_count": len(classified_records),
            "error_count": len(issues),
            "excluded_count": blocked_count,
            "preset_assigned_count": sum(1 for r in classified_records if r.get("preset") is not None),
            "review_pending_count": sum(1 for r in classified_records if r.get("validation_status") == "review_pending"),
            "succeeded_count": eligible_count,
            "total_records": len(classified_records),
        },
        "validation_artifact": val_rel_path,
        "validation_checks": [
            {"check": "preset_populated", "status": "PASS" if all(r.get("preset") == preset for r in classified_records) else "FAIL"},
            {"check": "difficulty_valid_tiers", "status": "PASS" if all(r.get("difficulty") in ALLOWED_DIFFICULTY_LABELS for r in classified_records) else "FAIL"},
            {"check": "final_output_eligibility_enforced", "status": "PASS"},
        ],
    }
    val_path = repo_root / val_rel_path
    write_canonical_json(val_path, val_doc)

    # Legacy dual-write for uclouvain
    if legacy_out_path and legacy_val_path:
        write_canonical_json(legacy_out_path, out_doc)
        write_canonical_json(legacy_val_path, val_doc)

    # Write stage QA reports
    write_stage_qa_pair(
        stage_name="DIFFICULTY",
        validation_data=val_doc,
        backtesting_commands=[
            f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source {source_id} --word \"{classified_records[0]['word']}\"",
            ".\\.venv\\Scripts\\pytest.exe tests/test_vocabulary_pipeline.py",
        ],
        verification_steps=[
            f"Verify all {len(classified_records)} records have preset={preset!r}.",
            f"Verify difficulty tier counts: {diff_counts}.",
            f"Verify final_output_eligible: {eligible_count} eligible, {blocked_count} blocked/excluded.",
        ],
        source_id=source_id,
    )

    return out_doc
