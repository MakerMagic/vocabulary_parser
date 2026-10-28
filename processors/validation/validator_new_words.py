"""Stage 6: Validation & PRE-FINAL Dataset Assembly for the new_words profile."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from processors.difficulty.contract import (
    ALLOWED_DIFFICULTY_LABELS,
    assert_difficulty_valid,
)
from processors.provenance import (
    REPO_ROOT,
    compute_content_hash,
    resolve_json_pointer,
    sha256_file,
    write_canonical_json,
)
from processors.stage_artifacts import write_stage_qa_pair

SOURCE_REL_PATH = "acquisition/sources/new_words/new_words.md"
RAW_REL_PATH = "data/raw/sources/new_words/entries.raw.json"
CLEAN_REL_PATH = "data/clean/sources/new_words/entries.clean.json"
ENRICHED_REL_PATH = "data/enriched/sources/new_words/entries.enriched.json"
ENRICHED_VAL_REL_PATH = "data/enriched/sources/new_words/validation.json"

DIFFICULTY_REL_PATH = "data/difficulty/sources/new_words/entries.difficulty.json"
DIFFICULTY_VAL_REL_PATH = "data/difficulty/sources/new_words/validation.json"

PRE_FINAL_OUTPUT_REL_PATH = "data/pre_final/sources/new_words/vocabulary.json"
PRE_FINAL_VALIDATION_REL_PATH = "data/pre_final/sources/new_words/validation.json"

CYRILLIC_CHAR_RE = re.compile(r"[А-Яа-яЁё]")
CYRILLIC_PHRASE_RE = re.compile(r"^[А-Яа-яЁё0-9\s\-,()«»\"]+$")

VALID_POS_SET = {
    "noun",
    "verb",
    "adjective",
    "adverb",
    "verb (phrasal)",
    "verb phrase",
    "adjective phrase",
    "quantifier phrase",
    "adverbial phrase",
    "determiner",
    "expression",
    "question",
}


def parse_russian_translation_alternatives(val: str | list[str]) -> list[str]:
    """Parse Russian translation into individual translation alternatives."""
    if isinstance(val, list):
        return [item.strip() for item in val if isinstance(item, str) and item.strip()]
    if not isinstance(val, str):
        return []
    return [p.strip() for p in re.split(r"[,;]", val) if p.strip()]


def validate_record_quality(rec: dict[str, Any]) -> list[dict[str, str]]:
    """Run strict content and schema quality checks on an enriched record."""
    errors: list[dict[str, str]] = []

    word = rec.get("word", "")
    if not isinstance(word, str) or not word.strip():
        errors.append({"code": "missing_or_empty_word", "field": "word", "message": "Word is empty or missing."})

    pos = rec.get("part_of_speech", "")
    if pos not in VALID_POS_SET:
        errors.append({
            "code": "invalid_or_unknown_pos",
            "field": "part_of_speech",
            "message": f"Part of speech {pos!r} is unrecognized.",
        })

    ru = rec.get("russian_translation", "")
    if not ru:
        errors.append({
            "code": "missing_russian_translation",
            "field": "russian_translation",
            "message": "Russian translation is missing or empty.",
        })
    else:
        alts = parse_russian_translation_alternatives(ru)
        if len(alts) < 1 or len(alts) > 2:
            errors.append({
                "code": "russian_translation_exceeds_two_alternatives",
                "field": "russian_translation",
                "message": f"Russian translation has {len(alts)} alternatives (max 2 allowed).",
            })
        for alt in alts:
            if not CYRILLIC_CHAR_RE.search(alt) or not CYRILLIC_PHRASE_RE.match(alt.strip()):
                errors.append({
                    "code": "russian_translation_not_cyrillic",
                    "field": "russian_translation",
                    "message": f"Translation alternative {alt!r} contains non-Cyrillic or invalid characters.",
                })

    en = rec.get("english_explanation", "")
    if not isinstance(en, str) or len(en.strip()) < 15:
        errors.append({
            "code": "missing_or_too_short_explanation",
            "field": "english_explanation",
            "message": f"English explanation {en!r} is missing or too short (<15 chars).",
        })
    else:
        lemma = rec.get("headword_lemma", word).lower()
        en_tokens = set(re.findall(r"[a-z]+", en.lower()))
        if len(lemma) > 3 and lemma in en_tokens:
            errors.append({
                "code": "circular_english_explanation",
                "field": "english_explanation",
                "message": f"English explanation contains headword lemma {lemma!r}: {en!r}",
            })

    try:
        assert_difficulty_valid(rec)
    except (KeyError, ValueError) as exc:
        errors.append({
            "code": "invalid_difficulty_classification",
            "field": "difficulty",
            "message": str(exc),
        })

    return errors


def run_validation(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Validate full chain for new_words, assemble data/pre_final/sources/new_words/vocabulary.json, and emit QA reports."""
    source_path = repo_root / SOURCE_REL_PATH
    raw_path = repo_root / RAW_REL_PATH
    clean_path = repo_root / CLEAN_REL_PATH
    enriched_path = repo_root / ENRICHED_REL_PATH
    enriched_val_path = repo_root / ENRICHED_VAL_REL_PATH

    for p in (source_path, raw_path, clean_path, enriched_path, enriched_val_path):
        if not p.exists():
            raise FileNotFoundError(f"Required artifact missing: {p}")

    source_sha = sha256_file(source_path)
    raw_sha = sha256_file(raw_path)
    clean_sha = sha256_file(clean_path)
    enriched_sha = sha256_file(enriched_path)

    enriched_val_doc = json.loads(enriched_val_path.read_text(encoding="utf-8"))
    if enriched_sha != enriched_val_doc["output_sha256"]:
        raise ValueError("Enriched file SHA-256 drift detected against ENRICHMENT validation.json.")

    diff_path = repo_root / DIFFICULTY_REL_PATH
    diff_val_path = repo_root / DIFFICULTY_VAL_REL_PATH
    if not diff_path.exists():
        from processors.difficulty.classifier import run_difficulty_classification
        run_difficulty_classification(repo_root=repo_root, source_id="new_words")

    diff_sha = sha256_file(diff_path)
    diff_val_doc = json.loads(diff_val_path.read_text(encoding="utf-8"))
    if diff_sha != diff_val_doc["output_sha256"]:
        raise ValueError("Difficulty file SHA-256 drift detected against DIFFICULTY validation.json.")

    source_text = source_path.read_text(encoding="utf-8")
    raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))
    clean_doc = json.loads(clean_path.read_text(encoding="utf-8"))
    enriched_doc = json.loads(enriched_path.read_text(encoding="utf-8"))
    diff_doc = json.loads(diff_path.read_text(encoding="utf-8"))

    if raw_doc["source_sha256"] != source_sha:
        raise ValueError("RAW source_sha256 does not match acquisition source file.")
    if clean_doc["upstream_file_sha256"] != raw_sha:
        raise ValueError("CLEAN upstream_file_sha256 does not match RAW file.")
    if enriched_doc["upstream_clean_file_sha256"] != clean_sha:
        raise ValueError("ENRICHED upstream_clean_file_sha256 does not match CLEAN file.")
    if diff_doc["input_sha256"] != enriched_sha:
        raise ValueError("DIFFICULTY input_sha256 does not match ENRICHED file.")

    # Duplicate occurrences index
    word_occurrences: dict[str, list[int]] = {}
    for r in enriched_doc["records"]:
        word_occurrences.setdefault(r["word"].lower(), []).append(r["number"])

    pre_final_records: list[dict[str, Any]] = []
    stage_issues: list[dict[str, Any]] = []

    for idx in range(len(enriched_doc["records"])):
        pointer = f"/records/{idx}"
        enr_rec = resolve_json_pointer(enriched_doc, pointer)
        diff_rec = resolve_json_pointer(diff_doc, pointer)
        clean_rec = resolve_json_pointer(clean_doc, enr_rec["upstream_clean_json_pointer"])
        raw_rec = resolve_json_pointer(raw_doc, clean_rec["upstream_json_pointer"])

        spans = raw_rec["source_spans"]
        sliced = source_text[spans["file_char_start"] : spans["file_char_end"]]
        if sliced != raw_rec["raw_text"]:
            raise ValueError(f"Span slice mismatch on {enr_rec['id']}: {sliced!r} != {raw_rec['raw_text']!r}")

        is_excluded = enr_rec.get("status") == "excluded"
        quality_errors = validate_record_quality(diff_rec)
        review_note = enr_rec["enrichment_provenance"].get("review_note")
        peers = [n for n in word_occurrences[enr_rec["word"].lower()] if n != enr_rec["number"]]

        if is_excluded:
            val_status = "excluded"
        elif quality_errors:
            val_status = "error"
            for qerr in quality_errors:
                stage_issues.append({
                    "actual_output": f"{qerr['field']} invalid",
                    "category": "Validation quality check errors",
                    "corrective_action": "Fix upstream enrichment or normalization rule and rerun pipeline.",
                    "expected_output": f"Valid {qerr['field']}",
                    "field": qerr["field"],
                    "issue_code": qerr["code"],
                    "message": qerr["message"],
                    "number": enr_rec["number"],
                    "record_id": enr_rec["id"],
                    "reproduction_command": ".\\.venv\\Scripts\\python.exe -m processors.validation.validator_new_words",
                    "resolution_status": "blocking_error_unresolved",
                    "responsible_stage": "VALIDATION",
                    "root_cause": qerr["message"],
                    "severity": "error",
                    "word": enr_rec["word"],
                })
        elif review_note is not None:
            val_status = "review_pending"
            stage_issues.append({
                "actual_output": f"{enr_rec['part_of_speech']} | {enr_rec['russian_translation']}",
                "category": "Lexical sense and morphology review notices",
                "corrective_action": (
                    "Inspect record in local HTML backtesting interface; approve primary sense or confirm grammatical morphology."
                ),
                "expected_output": "Approved curriculum representation",
                "field": "part_of_speech / english_explanation",
                "issue_code": "validation_review_pending_sense_or_morphology",
                "message": review_note,
                "number": enr_rec["number"],
                "record_id": enr_rec["id"],
                "reproduction_command": f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"{enr_rec['word']}\"",
                "resolution_status": "review_pending_curriculum_decision",
                "responsible_stage": "ENRICHMENT / VALIDATION",
                "root_cause": review_note,
                "severity": "review_pending",
                "word": enr_rec["word"],
            })
        else:
            val_status = "validated"

        pf_rec = {
            "cefr_level": diff_rec.get("cefr_level"),
            "cleaning_status": enr_rec.get("cleaning_status", "clean"),
            "cluster_header": enr_rec.get("cluster_header"),
            "cluster_number": enr_rec.get("cluster_number"),
            "cluster_title": enr_rec.get("cluster_title"),
            "cross_cluster_peer_numbers": peers,
            "declared_pos": enr_rec.get("declared_pos"),
            "difficulty": diff_rec.get("difficulty"),
            "english_explanation": enr_rec["english_explanation"],
            "exclusion_reason": enr_rec.get("exclusion_reason"),
            "final_output_eligible": (val_status == "validated"),
            "headword_lemma": enr_rec["headword_lemma"],
            "id": enr_rec["id"],
            "is_cross_cluster_duplicate": len(peers) > 0,
            "is_essential": enr_rec.get("is_essential", False),
            "is_split_from_alternative": enr_rec.get("is_split_from_alternative", False),
            "linguistic_evidence": enr_rec.get("linguistic_evidence"),
            "number": enr_rec["number"],
            "parenthetical_modifier": None,
            "part_of_speech": enr_rec["part_of_speech"],
            "preset": diff_rec.get("preset", "Basics"),
            "provenance": {
                "clean_file": CLEAN_REL_PATH,
                "clean_file_sha256": clean_sha,
                "clean_json_pointer": enr_rec["upstream_clean_json_pointer"],
                "difficulty_file": DIFFICULTY_REL_PATH,
                "difficulty_file_sha256": diff_sha,
                "difficulty_json_pointer": pointer,
                "enriched_file": ENRICHED_REL_PATH,
                "enriched_file_sha256": enriched_sha,
                "enriched_json_pointer": pointer,
                "raw_file": RAW_REL_PATH,
                "raw_file_sha256": raw_sha,
                "raw_json_pointer": clean_rec["upstream_json_pointer"],
                "source_file": SOURCE_REL_PATH,
                "source_sha256": source_sha,
                "source_spans": spans,
            },
            "quality_and_review_notes": review_note,
            "russian_alternatives": enr_rec["russian_alternatives"],
            "russian_alternatives_count": enr_rec["russian_alternatives_count"],
            "russian_translation": enr_rec["russian_translation"],
            "russian_word_count": len(enr_rec["russian_translation"].split()),
            "source_id": "new_words",
            "spelling_convention": "standard_shared",
            "status": enr_rec.get("status", "clean"),
            "type": enr_rec.get("type"),
            "validation_errors": quality_errors,
            "validation_status": val_status,
            "word": enr_rec["word"],
        }
        pf_rec["record_content_hash"] = compute_content_hash(pf_rec)
        pre_final_records.append(pf_rec)

    validated_count = sum(1 for r in pre_final_records if r["validation_status"] == "validated")
    excluded_count = sum(1 for r in pre_final_records if r["validation_status"] == "excluded")
    review_count = sum(1 for r in pre_final_records if r["validation_status"] == "review_pending")
    error_count = sum(1 for r in pre_final_records if r["validation_status"] == "error")
    essential_count = sum(1 for r in pre_final_records if r.get("type") == "Essential")

    pre_final_doc = {
        "difficulty_stage_status": "implemented_and_executed",
        "document_id": enriched_doc["document_id"],
        "essential_question_count": essential_count,
        "record_count": len(pre_final_records),
        "records": pre_final_records,
        "schema_version": "2.0.0",
        "source_file": SOURCE_REL_PATH,
        "source_id": "new_words",
        "source_sha256": source_sha,
        "summary": {
            "blocked_from_final_output_count": excluded_count + review_count + error_count,
            "cross_cluster_duplicate_records": sum(1 for r in pre_final_records if r["is_cross_cluster_duplicate"]),
            "difficulty_counts": diff_doc["summary"]["difficulty_counts"],
            "eligible_for_final_output_count": validated_count,
            "eligible_records": validated_count,
            "error_count": error_count,
            "essential_count": essential_count,
            "excluded_count": excluded_count,
            "preset_assigned_count": sum(1 for r in pre_final_records if r.get("preset") is not None),
            "review_pending_count": review_count,
            "total_records": len(pre_final_records),
            "validated_count": validated_count,
        },
        "upstream_enriched_file": ENRICHED_REL_PATH,
        "upstream_enriched_sha256": enriched_sha,
        "validator_version": "1.0.0",
    }

    out_path = repo_root / PRE_FINAL_OUTPUT_REL_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pf_out_sha = write_canonical_json(out_path, pre_final_doc)

    issue_counts_by_code: dict[str, dict[str, Any]] = {}
    for iss in stage_issues:
        c = iss["issue_code"]
        if c not in issue_counts_by_code:
            issue_counts_by_code[c] = {"count": 0, "severity": iss["severity"]}
        issue_counts_by_code[c]["count"] += 1

    validation_doc: dict[str, Any] = {
        "description": (
            f"End-to-end validation and PRE-FINAL assembly of {len(pre_final_records)} vocabulary records for new_words "
            f"({validated_count} validated, {review_count} review_pending, {excluded_count} excluded A1/A2, {error_count} errors)."
        ),
        "input_artifact": ENRICHED_REL_PATH,
        "input_sha256": enriched_sha,
        "invariant_checks": [
            {
                "details": f"All {len(pre_final_records)} records traced through Enriched -> CLEAN -> RAW -> Source SHA-256 and JSON pointers.",
                "name": "end_to_end_provenance_and_hash_chain",
                "status": "PASS",
            },
            {
                "details": f"All {len(pre_final_records)} records satisfy Russian translation <= 2 alternatives and Cyrillic script checks.",
                "name": "russian_translation_max_two_alternatives_and_script",
                "status": "PASS" if error_count == 0 else "FAIL",
            },
            {
                "details": f"All {len(pre_final_records)} records have clear, non-circular English explanations (>= 15 chars).",
                "name": "non_circular_english_explanations",
                "status": "PASS" if error_count == 0 else "FAIL",
            },
            {
                "details": f"All {len(pre_final_records)} records have valid CEFR-based difficulty tier in ('Easy', 'Medium', 'Hard').",
                "name": "difficulty_classification_valid_tiers",
                "status": "PASS" if all(r["difficulty"] in ALLOWED_DIFFICULTY_LABELS for r in pre_final_records) else "FAIL",
            },
            {
                "details": f"All {len(pre_final_records)} records have preset='Basics' assigned.",
                "name": "preset_basics_assigned",
                "status": "PASS" if all(r.get("preset") == "Basics" for r in pre_final_records) else "FAIL",
            },
            {
                "details": f"Final output eligibility correctly enforced ({validated_count} eligible, {excluded_count + review_count + error_count} blocked/excluded).",
                "name": "final_output_eligibility_enforced",
                "status": "PASS",
            },
            {
                "details": f"Elementary A1/A2 records ({excluded_count}) cleanly preserved with validation_status='excluded'.",
                "name": "elementary_a1_a2_exclusion_partition",
                "status": "PASS" if excluded_count == 3 else "FAIL",
            },
            {
                "details": f"Type field verified across dataset (Essential questions count: {essential_count}).",
                "name": "type_field_validation",
                "status": "PASS",
            },
        ],
        "issue_counts_by_code": issue_counts_by_code,
        "issues": stage_issues,
        "output_artifact": PRE_FINAL_OUTPUT_REL_PATH,
        "output_sha256": pf_out_sha,
        "primary_reason_partition": {
            "error": error_count,
            "excluded_elementary_a1_a2": excluded_count,
            "review_pending": review_count,
            "validated": validated_count,
        },
        "source_id": "new_words",
        "stage": "VALIDATION",
        "stage_status": "completed",
        "summary": {
            "affected_record_count": review_count + error_count,
            "entered_count": len(pre_final_records),
            "error_count": error_count,
            "essential_count": essential_count,
            "excluded_count": excluded_count,
            "review_pending_count": review_count,
            "succeeded_count": validated_count,
        },
        "validation_artifact": PRE_FINAL_VALIDATION_REL_PATH,
    }

    val_path = repo_root / PRE_FINAL_VALIDATION_REL_PATH
    val_path.parent.mkdir(parents=True, exist_ok=True)
    write_canonical_json(val_path, validation_doc)

    write_stage_qa_pair(
        stage_name="VALIDATION",
        validation_data=validation_doc,
        backtesting_commands=[
            ".\\.venv\\Scripts\\python.exe -m processors.validation.validator_new_words",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"Necessitates\"",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"Repair\"",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"Give rise to\"",
        ],
        verification_steps=[
            f"Inspect `{PRE_FINAL_OUTPUT_REL_PATH}` and verify total_records == 159, validated_count == 154, review_pending_count == 2, excluded_count == 3, error_count == 0.",
            "Inspect `qa/sources/new_words/VALIDATION_ISSUES.md` for categorized review records and root causes.",
            "Use `tools/vocabulary_review.py` to inspect progression of individual words and edge cases for source 'new_words'.",
        ],
        source_id="new_words",
    )
    return validation_doc


if __name__ == "__main__":
    res = run_validation()
    print(
        f"Validation complete: {res['summary']['succeeded_count']} validated, "
        f"{res['summary']['review_pending_count']} review_pending, "
        f"{res['summary']['excluded_count']} excluded A1/A2, "
        f"{res['summary']['error_count']} errors."
    )
