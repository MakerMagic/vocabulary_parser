"""Stage 4: Cleaning & Deduplication for the math_basics profile."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from processors.normalization.cleaner import verify_token_ledger
from processors.provenance import (
    REPO_ROOT,
    compute_content_hash,
    sha256_file,
    write_canonical_json,
)
from processors.stage_artifacts import write_stage_qa_pair

RAW_INPUT_REL_PATH = "data/raw/sources/math_basics/entries.raw.json"
CLEAN_OUTPUT_REL_PATH = "data/clean/sources/math_basics/entries.clean.json"
CLEAN_VALIDATION_REL_PATH = "data/clean/sources/math_basics/validation.json"


def run_cleaning_and_deduplication(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Clean records and deduplicate mathematical vocabulary terms."""
    raw_path = repo_root / RAW_INPUT_REL_PATH
    if not raw_path.exists():
        raise FileNotFoundError(f"RAW input missing at {raw_path}")

    raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))
    raw_records: list[dict[str, Any]] = raw_doc["records"]
    raw_sha = sha256_file(raw_path)

    clean_records: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    seen_terms: dict[str, dict[str, Any]] = {}
    eligible_count = 0
    duplicate_count = 0

    for r in raw_records:
        rec_id = r["id"]
        number = r["number"]
        raw_text = r["raw_text"]
        normalized_word = raw_text.strip().lower()

        # Non-whitespace token ledger verification
        ledger_match, _, _ = verify_token_ledger(raw_text, normalized_word)
        if not ledger_match:
            issues.append({
                "category": "Token Ledger Mismatch",
                "details": f"Token ledger mismatch for {raw_text!r} vs {normalized_word!r}",
                "issue_code": "LEDGER_MISMATCH",
                "record_id": rec_id,
                "severity": "error",
            })

        # Deduplication check
        if normalized_word not in seen_terms:
            # Primary / Retained occurrence
            seen_terms[normalized_word] = {
                "id": rec_id,
                "line": number,
                "word": normalized_word,
            }
            is_dup = False
            master_id = None
            status = "clean"
            excl_reason = None
            review_note = None
            final_eligible = True
            eligible_count += 1
        else:
            # Duplicate occurrence
            master_entry = seen_terms[normalized_word]
            is_dup = True
            master_id = master_entry["id"]
            status = "excluded"
            excl_reason = "duplicate_term"
            review_note = f"Duplicate occurrence of '{normalized_word}' (master entry is {master_id} at line {master_entry['line']})."
            final_eligible = False
            duplicate_count += 1
            issues.append({
                "category": "Duplicate Vocabulary Entry",
                "details": review_note,
                "issue_code": "DUPLICATE_ENTRY",
                "master_record_id": master_id,
                "record_id": rec_id,
                "severity": "info",
                "word": normalized_word,
            })

        clean_rec: dict[str, Any] = {
            "declared_pos": None,
            "difficulty": None,  # Invariant: null in Clean stage
            "duplicate_master_id": master_id,
            "exclusion_reason": excl_reason,
            "final_output_eligible": final_eligible,
            "headword_lemma": normalized_word,
            "id": rec_id,
            "is_duplicate": is_dup,
            "normalization_audit": {
                "cleaning_transforms": ["strip_whitespace", "lowercase_normalize"],
                "token_ledger_match": ledger_match,
            },
            "number": number,
            "parenthetical_modifier": None,
            "preset": "math_basics",
            "provenance": {
                "raw_record_id": rec_id,
                "source_file": r["source_file"],
                "source_sha256": r["source_sha256"],
                "source_spans": r["source_spans"],
            },
            "quality_and_review_notes": review_note,
            "raw_text": raw_text,
            "source_id": "math_basics",
            "spelling_convention": "standard_shared",
            "status": status,
            "word": normalized_word,
        }
        clean_rec["record_content_hash"] = compute_content_hash(clean_rec)
        clean_records.append(clean_rec)

    clean_payload: dict[str, Any] = {
        "deduplication_summary": {
            "duplicate_count": duplicate_count,
            "eligible_unique_count": eligible_count,
            "total_records": len(clean_records),
        },
        "preset": "math_basics",
        "record_count": len(clean_records),
        "records": clean_records,
        "source_file": raw_doc["source_file"],
        "source_id": "math_basics",
        "source_sha256": raw_doc["source_sha256"],
    }
    clean_payload["payload_hash"] = compute_content_hash(clean_payload)

    out_path = repo_root / CLEAN_OUTPUT_REL_PATH
    write_canonical_json(out_path, clean_payload)

    val_payload: dict[str, Any] = {
        "description": "Cleaned and deduplicated mathematical vocabulary records from math_basics",
        "error_count": sum(1 for i in issues if i.get("severity") == "error"),
        "input_artifact": RAW_INPUT_REL_PATH,
        "input_sha256": raw_sha,
        "issues": issues,
        "output_artifact": CLEAN_OUTPUT_REL_PATH,
        "provenance_lock": {
            "payload_hash": clean_payload["payload_hash"],
            "raw_payload_hash": raw_doc.get("payload_hash"),
        },
        "record_count": len(clean_records),
        "source_id": "math_basics",
        "stage": "CLEAN",
        "stage_status": "completed",
        "summary": {
            "affected_record_count": duplicate_count,
            "duplicate_count": duplicate_count,
            "entered_count": len(clean_records),
            "error_count": 0,
            "review_pending_count": 0,
            "succeeded_count": len(clean_records),
            "unique_terms_retained": eligible_count,
        },
        "validation_artifact": CLEAN_VALIDATION_REL_PATH,
        "validation_timestamp": "2026-10-29T17:53:00Z",
        "warning_count": duplicate_count,
    }
    val_path = repo_root / CLEAN_VALIDATION_REL_PATH
    write_canonical_json(val_path, val_payload)

    write_stage_qa_pair(
        stage_name="CLEAN",
        validation_data=val_payload,
        backtesting_commands=[
            ".\\.venv\\Scripts\\python.exe -c \"from processors.normalization.cleaner_math import run_cleaning_and_deduplication; run_cleaning_and_deduplication()\"",
            "Get-Content data/clean/sources/math_basics/validation.json | ConvertFrom-Json",
        ],
        verification_steps=[
            "Verify all 274 records are present in data/clean/sources/math_basics/entries.clean.json.",
            "Verify exactly 183 records have status='clean' and final_output_eligible=True.",
            "Verify exactly 91 records have status='excluded', exclusion_reason='duplicate_term', and final_output_eligible=False.",
            "Check 100% token ledger conservation across all records.",
            "Check preset='math_basics' on 100% of records.",
        ],
        source_id="math_basics",
    )

    return clean_payload


if __name__ == "__main__":
    res = run_cleaning_and_deduplication()
    print(f"Cleaned {res['record_count']} records: {res['deduplication_summary']['eligible_unique_count']} unique eligible, {res['deduplication_summary']['duplicate_count']} duplicates excluded.")
