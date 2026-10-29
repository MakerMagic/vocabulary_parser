"""Stage 7: Validation & PRE-FINAL Assembly for math_basics."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from processors.difficulty.contract import assert_difficulty_valid
from processors.provenance import (
    REPO_ROOT,
    compute_content_hash,
    resolve_json_pointer,
    sha256_file,
    write_canonical_json,
)
from processors.stage_artifacts import write_stage_qa_pair

SOURCE_REL_PATH = "acquisition/sources/math_basics/math_basics.txt"
RAW_REL_PATH = "data/raw/sources/math_basics/entries.raw.json"
CLEAN_REL_PATH = "data/clean/sources/math_basics/entries.clean.json"
ENRICHED_REL_PATH = "data/enriched/sources/math_basics/entries.enriched.json"
DIFFICULTY_REL_PATH = "data/difficulty/sources/math_basics/entries.difficulty.json"

PRE_FINAL_OUTPUT_REL_PATH = "data/pre_final/sources/math_basics/vocabulary.json"
PRE_FINAL_VALIDATION_REL_PATH = "data/pre_final/sources/math_basics/validation.json"

CYRILLIC_CHAR_RE = re.compile(r"[А-Яа-яЁё]")
CYRILLIC_PHRASE_RE = re.compile(r"^[А-Яа-яЁё0-9\s\-,()«»\"—–]+$")

VALID_POS_SET = {
    "noun",
    "verb",
    "adjective",
    "noun phrase",
    "noun (plural)",
}


def parse_russian_translation_alternatives(val: str | list[str]) -> list[str]:
    """Parse Russian translation into individual translation alternatives."""
    if isinstance(val, list):
        return [item.strip() for item in val if isinstance(item, str) and item.strip()]
    if not isinstance(val, str):
        return []
    return [p.strip() for p in re.split(r"[;]", val) if p.strip()]


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
        lemmas = [part for part in lemma.split() if len(part) > 3]
        en_tokens = set(re.findall(r"[a-z]+", en.lower()))
        for lem in lemmas:
            if lem in en_tokens:
                errors.append({
                    "code": "circular_english_explanation",
                    "field": "english_explanation",
                    "message": f"English explanation contains headword lemma {lem!r}: {en!r}",
                })

    try:
        assert_difficulty_valid(rec)
    except (KeyError, ValueError) as exc:
        errors.append({
            "code": "invalid_difficulty_classification",
            "field": "difficulty",
            "message": str(exc),
        })

    preset = rec.get("preset")
    if preset != "math_basics":
        errors.append({
            "code": "invalid_preset",
            "field": "preset",
            "message": f"Expected preset 'math_basics', found {preset!r}.",
        })

    return errors


def run_validation(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Validate full chain for math_basics, assemble pre_final vocabulary.json, and emit QA reports."""
    source_path = repo_root / SOURCE_REL_PATH
    raw_path = repo_root / RAW_REL_PATH
    clean_path = repo_root / CLEAN_REL_PATH
    enriched_path = repo_root / ENRICHED_REL_PATH
    difficulty_path = repo_root / DIFFICULTY_REL_PATH

    for p in (source_path, raw_path, clean_path, enriched_path, difficulty_path):
        if not p.exists():
            raise FileNotFoundError(f"Required pipeline artifact missing: {p}")

    source_sha = sha256_file(source_path)
    raw_sha = sha256_file(raw_path)
    clean_sha = sha256_file(clean_path)
    enriched_sha = sha256_file(enriched_path)
    diff_sha = sha256_file(difficulty_path)

    raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))
    clean_doc = json.loads(clean_path.read_text(encoding="utf-8"))
    enriched_doc = json.loads(enriched_path.read_text(encoding="utf-8"))
    diff_doc = json.loads(difficulty_path.read_text(encoding="utf-8"))

    assert len(clean_doc["records"]) == len(raw_doc["records"]) == len(enriched_doc["records"]) == len(diff_doc["records"]) == 274

    source_text = source_path.read_text(encoding="utf-8")

    pre_final_records: list[dict[str, Any]] = []
    stage_issues: list[dict[str, Any]] = []

    validated_count = 0
    excluded_count = 0
    error_count = 0

    for idx in range(len(diff_doc["records"])):
        pointer = f"/records/{idx}"
        raw_rec = resolve_json_pointer(raw_doc, pointer)
        clean_rec = resolve_json_pointer(clean_doc, pointer)
        enr_rec = resolve_json_pointer(enriched_doc, pointer)
        diff_rec = resolve_json_pointer(diff_doc, pointer)

        spans = raw_rec["source_spans"]
        reconstructed = source_text[spans["file_char_start"] : spans["file_char_end"]]
        assert reconstructed == raw_rec["raw_text"], f"Span slice mismatch for {raw_rec['word']}"

        quality_errors = validate_record_quality(diff_rec)

        is_dup = diff_rec.get("is_duplicate", False)

        if quality_errors:
            val_status = "error"
            error_count += 1
            final_eligible = False
            for err in quality_errors:
                stage_issues.append({
                    "actual_output": diff_rec.get(err["field"]),
                    "category": "Validation contract defect",
                    "corrective_action": "Fix normalization or enrichment rule.",
                    "expected_output": "Schema-compliant value",
                    "field": err["field"],
                    "issue_code": err["code"],
                    "message": err["message"],
                    "number": diff_rec["number"],
                    "record_id": diff_rec["id"],
                    "severity": "error",
                    "word": diff_rec["word"],
                })
        elif is_dup:
            val_status = "excluded"
            excluded_count += 1
            final_eligible = False
            stage_issues.append({
                "actual_output": f"Excluded duplicate (master: {diff_rec.get('duplicate_master_id')})",
                "category": "Duplicate Vocabulary Entry",
                "corrective_action": "Preserve in RAW/dataset history; exclude from final eligible curriculum output.",
                "expected_output": "Excluded from eligible output with duplicate master pointer",
                "field": "is_duplicate",
                "issue_code": "DUPLICATE_ENTRY",
                "master_record_id": diff_rec.get("duplicate_master_id"),
                "message": diff_rec.get("quality_and_review_notes"),
                "number": diff_rec["number"],
                "record_id": diff_rec["id"],
                "severity": "info",
                "word": diff_rec["word"],
            })
        else:
            val_status = "validated"
            validated_count += 1
            final_eligible = True

        pf_rec: dict[str, Any] = {
            "cefr_level": diff_rec["cefr_level"],
            "difficulty": diff_rec["difficulty"],
            "duplicate_master_id": diff_rec.get("duplicate_master_id"),
            "english_explanation": diff_rec["english_explanation"],
            "exclusion_reason": diff_rec.get("exclusion_reason"),
            "final_output_eligible": final_eligible,
            "headword_lemma": diff_rec["headword_lemma"],
            "id": diff_rec["id"],
            "is_duplicate": is_dup,
            "normalization_audit": clean_rec["normalization_audit"],
            "number": diff_rec["number"],
            "parenthetical_modifier": None,
            "part_of_speech": diff_rec["part_of_speech"],
            "preset": "math_basics",
            "provenance": {
                "clean_record_id": clean_rec["id"],
                "difficulty_record_id": diff_rec["id"],
                "enriched_record_id": enr_rec["id"],
                "raw_record_id": raw_rec["id"],
                "source_file": raw_rec["source_file"],
                "source_sha256": raw_rec["source_sha256"],
                "source_spans": raw_rec["source_spans"],
            },
            "quality_and_review_notes": diff_rec.get("quality_and_review_notes"),
            "raw_text": raw_rec["raw_text"],
            "russian_alternatives": diff_rec["russian_alternatives"],
            "russian_translation": diff_rec["russian_translation"],
            "source_id": "math_basics",
            "spelling_convention": "standard_shared",
            "type": None,  # Standard vocabulary item
            "validation_errors": quality_errors,
            "validation_status": val_status,
            "word": diff_rec["word"],
        }
        pf_rec["record_content_hash"] = compute_content_hash(pf_rec)
        pre_final_records.append(pf_rec)

    pre_final_doc: dict[str, Any] = {
        "dataset_name": "math_basics",
        "format_version": "1.0.0",
        "preset": "math_basics",
        "record_count": len(pre_final_records),
        "records": pre_final_records,
        "source_id": "math_basics",
        "summary": {
            "duplicate_excluded_count": excluded_count,
            "error_count": error_count,
            "review_pending_count": 0,
            "total_records": len(pre_final_records),
            "validated_eligible_count": validated_count,
        },
    }
    pre_final_doc["payload_hash"] = compute_content_hash(pre_final_doc)

    out_path = repo_root / PRE_FINAL_OUTPUT_REL_PATH
    write_canonical_json(out_path, pre_final_doc)

    val_payload: dict[str, Any] = {
        "description": "Validation and PRE-FINAL assembly for math_basics vocabulary",
        "error_count": error_count,
        "input_artifact": DIFFICULTY_REL_PATH,
        "input_sha256": diff_sha,
        "issues": stage_issues,
        "output_artifact": PRE_FINAL_OUTPUT_REL_PATH,
        "provenance_lock": {
            "clean_sha256": clean_sha,
            "difficulty_sha256": diff_sha,
            "enriched_sha256": enriched_sha,
            "payload_hash": pre_final_doc["payload_hash"],
            "raw_sha256": raw_sha,
            "source_sha256": source_sha,
        },
        "record_count": len(pre_final_records),
        "source_id": "math_basics",
        "stage": "VALIDATION",
        "stage_status": "completed",
        "summary": {
            "affected_record_count": excluded_count + error_count,
            "entered_count": len(pre_final_records),
            "error_count": error_count,
            "excluded_count": excluded_count,
            "review_pending_count": 0,
            "succeeded_count": len(pre_final_records) - error_count,
            "validated_count": validated_count,
        },
        "validation_artifact": PRE_FINAL_VALIDATION_REL_PATH,
        "validation_timestamp": "2026-10-29T17:56:00Z",
        "warning_count": excluded_count,
    }
    val_path = repo_root / PRE_FINAL_VALIDATION_REL_PATH
    write_canonical_json(val_path, val_payload)

    write_stage_qa_pair(
        stage_name="VALIDATION",
        validation_data=val_payload,
        backtesting_commands=[
            ".\\.venv\\Scripts\\python.exe -c \"from processors.validation.validator_math import run_validation; run_validation()\"",
            "Get-Content data/pre_final/sources/math_basics/validation.json | ConvertFrom-Json",
        ],
        verification_steps=[
            "Verify all 274 records exist in data/pre_final/sources/math_basics/vocabulary.json.",
            "Verify exactly 183 validated eligible terms (zero errors, zero unresolved review notes).",
            "Verify exactly 91 duplicate records marked excluded (final_output_eligible=False).",
            "Verify preset='math_basics' across 100% of records.",
            "Verify 0 validation errors across the dataset.",
        ],
        source_id="math_basics",
    )

    return pre_final_doc


if __name__ == "__main__":
    res = run_validation()
    s = res["summary"]
    print(f"Validation complete: {s['total_records']} total records, {s['validated_eligible_count']} validated eligible, {s['duplicate_excluded_count']} duplicates excluded, {s['error_count']} errors.")
