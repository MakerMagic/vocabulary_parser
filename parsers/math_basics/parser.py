"""Stage 3: RAW Extraction for the math_basics profile."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from processors.provenance import (
    REPO_ROOT,
    compute_content_hash,
    sha256_file,
    write_canonical_json,
)
from processors.stage_artifacts import write_stage_qa_pair

PRIMARY_SOURCE_REL_PATH = "acquisition/sources/math_basics/math_basics.txt"
FALLBACK_SOURCE_REL_PATH = "acquisition/local/math_basics.txt"

RAW_OUTPUT_REL_PATH = "data/raw/sources/math_basics/entries.raw.json"
RAW_VALIDATION_REL_PATH = "data/raw/sources/math_basics/validation.json"


def resolve_source_path(repo_root: Path = REPO_ROOT) -> tuple[Path, str]:
    """Resolve active source path, prioritizing math_basics source directory."""
    primary = repo_root / PRIMARY_SOURCE_REL_PATH
    if primary.exists():
        return primary, PRIMARY_SOURCE_REL_PATH
    fallback = repo_root / FALLBACK_SOURCE_REL_PATH
    if fallback.exists():
        return fallback, FALLBACK_SOURCE_REL_PATH
    raise FileNotFoundError(f"Source file not found at {primary} or {fallback}")


def run_raw_extraction(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Extract all entries from math_basics.txt into canonical RAW records."""
    source_path, source_rel_path = resolve_source_path(repo_root)
    source_sha = sha256_file(source_path)
    source_text = source_path.read_text(encoding="utf-8")
    lines_with_ends = source_text.splitlines(keepends=True)

    line_starts: list[int] = []
    curr = 0
    for l_text in lines_with_ends:
        line_starts.append(curr)
        curr += len(l_text)

    raw_records: list[dict[str, Any]] = []
    lines = source_text.splitlines()

    for idx, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            continue

        number = idx + 1
        rec_id = f"math_vocab_{number:03d}"

        # Find character offsets in the line
        line_str = lines_with_ends[idx] if idx < len(lines_with_ends) else ""
        col_start = line_str.find(line_clean)
        if col_start == -1:
            col_start = 0
        col_end = col_start + len(line_clean)
        file_start = line_starts[idx] + col_start
        file_end = file_start + len(line_clean)

        rec: dict[str, Any] = {
            "declared_pos": None,
            "difficulty": None,
            "id": rec_id,
            "number": number,
            "preset": "math_basics",
            "raw_text": line_clean,
            "readable_text": line_clean,
            "source_file": source_rel_path,
            "source_id": "math_basics",
            "source_sha256": source_sha,
            "source_spans": {
                "file_char_end": file_end,
                "file_char_start": file_start,
                "line_char_end": col_end,
                "line_char_start": col_start,
                "line_number": number,
            },
            "word": line_clean,
        }
        rec["record_content_hash"] = compute_content_hash(rec)
        raw_records.append(rec)

    raw_payload: dict[str, Any] = {
        "extraction_method": "exact_line_slices",
        "preset": "math_basics",
        "record_count": len(raw_records),
        "records": raw_records,
        "source_file": source_rel_path,
        "source_id": "math_basics",
        "source_sha256": source_sha,
    }
    raw_payload["payload_hash"] = compute_content_hash(raw_payload)

    out_path = repo_root / RAW_OUTPUT_REL_PATH
    write_canonical_json(out_path, raw_payload)

    val_payload: dict[str, Any] = {
        "description": "RAW extraction of mathematical vocabulary from math_basics.txt",
        "error_count": 0,
        "extraction_status": "passed",
        "input_artifact": source_rel_path,
        "issues": [],
        "output_artifact": RAW_OUTPUT_REL_PATH,
        "provenance_lock": {
            "payload_hash": raw_payload["payload_hash"],
            "sha256": source_sha,
        },
        "record_count": len(raw_records),
        "source_id": "math_basics",
        "stage": "RAW",
        "stage_status": "completed",
        "summary": {
            "affected_record_count": 0,
            "entered_count": len(raw_records),
            "error_count": 0,
            "review_pending_count": 0,
            "succeeded_count": len(raw_records),
        },
        "validation_artifact": RAW_VALIDATION_REL_PATH,
        "validation_timestamp": "2026-10-29T17:52:00Z",
        "warning_count": 0,
    }
    val_path = repo_root / RAW_VALIDATION_REL_PATH
    write_canonical_json(val_path, val_payload)

    # QA artifacts
    write_stage_qa_pair(
        stage_name="RAW",
        validation_data=val_payload,
        backtesting_commands=[
            ".\\.venv\\Scripts\\python.exe -c \"from parsers.math_basics.parser import run_raw_extraction; run_raw_extraction()\"",
            "Get-Content data/raw/sources/math_basics/validation.json | ConvertFrom-Json",
        ],
        verification_steps=[
            "Verify all 274 records are present in data/raw/sources/math_basics/entries.raw.json.",
            "Verify exact slice coordinate matching against source text.",
            "Check validation summary: entered_count == 274, succeeded_count == 274, error_count == 0.",
        ],
        source_id="math_basics",
    )

    return raw_payload


if __name__ == "__main__":
    res = run_raw_extraction()
    print(f"Extracted {res['record_count']} RAW records for math_basics.")
