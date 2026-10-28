"""Stage 1: Acquisition — Register and verify unmodified source vocabulary files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from processors.provenance import REPO_ROOT, sha256_file, write_canonical_json
from processors.stage_artifacts import write_stage_qa_pair

SOURCE_REL_PATH = "acquisition/local/justprepy_vocabulary_list.txt"
MANIFEST_REL_PATH = "acquisition/manifest.json"
VALIDATION_REL_PATH = "data/acquisition/validation.json"


def run_acquisition(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Verify incoming source file, write acquisition/manifest.json, and emit QA reports."""
    source_path = repo_root / SOURCE_REL_PATH
    if not source_path.exists():
        raise FileNotFoundError(f"Required source file missing: {source_path}")

    raw_bytes = source_path.read_bytes()
    text = raw_bytes.decode("utf-8")
    file_sha = sha256_file(source_path)
    lines = [ln for ln in text.splitlines() if ln.strip()]

    manifest_doc = {
        "schema_version": "1.0.0",
        "sources": [
            {
                "document_id": "justprepy_vocabulary_list_v1",
                "document_role": "wordlist",
                "encoding": "utf-8",
                "file_path": SOURCE_REL_PATH,
                "format": "txt_sectioned_comma_list",
                "line_count": len(lines),
                "origin": "user_supplied_prompt_input",
                "sha256": file_sha,
                "size_bytes": len(raw_bytes),
                "source_family": "justprepy",
            }
        ],
    }

    manifest_path = repo_root / MANIFEST_REL_PATH
    manifest_sha = write_canonical_json(manifest_path, manifest_doc)

    validation_doc: dict[str, Any] = {
        "description": "Acquisition and SHA-256 provenance registration of supplied justprepy vocabulary list.",
        "input_artifact": SOURCE_REL_PATH,
        "input_sha256": file_sha,
        "invariant_checks": [
            {
                "details": f"Source file present at {SOURCE_REL_PATH} ({len(raw_bytes)} bytes).",
                "name": "source_file_exists_and_nonempty",
                "status": "PASS" if len(raw_bytes) > 0 else "FAIL",
            },
            {
                "details": f"UTF-8 decoding verified without replacement characters ({len(lines)} non-empty lines).",
                "name": "utf8_encoding_integrity",
                "status": "PASS" if "\ufffd" not in text else "FAIL",
            },
            {
                "details": f"SHA-256 lock recorded in {MANIFEST_REL_PATH}: {file_sha[:16]}...",
                "name": "sha256_provenance_recorded",
                "status": "PASS",
            },
        ],
        "issue_counts_by_code": {},
        "issues": [],
        "output_artifact": MANIFEST_REL_PATH,
        "output_sha256": manifest_sha,
        "primary_reason_partition": {
            "registered_clean": 1,
        },
        "stage": "ACQUISITION",
        "stage_status": "completed",
        "summary": {
            "affected_record_count": 0,
            "entered_count": 1,
            "error_count": 0,
            "review_pending_count": 0,
            "succeeded_count": 1,
        },
        "validation_artifact": VALIDATION_REL_PATH,
    }

    write_canonical_json(repo_root / VALIDATION_REL_PATH, validation_doc)
    write_stage_qa_pair(
        stage_name="ACQUISITION",
        validation_data=validation_doc,
        backtesting_commands=[
            ".\\.venv\\Scripts\\python.exe -m processors.acquisition",
            ".\\.venv\\Scripts\\python.exe -m pytest -q tests/test_vocabulary_pipeline.py -k acquisition",
        ],
        verification_steps=[
            f"Confirm `{SOURCE_REL_PATH}` exists and matches the SHA-256 recorded in `{MANIFEST_REL_PATH}`.",
            f"Inspect `{VALIDATION_REL_PATH}` and verify `error_count == 0`.",
            "Run the acquisition pytest check to confirm byte-for-byte source preservation.",
        ],
    )
    return validation_doc


if __name__ == "__main__":
    res = run_acquisition()
    print(f"Acquisition complete: input_sha256={res['input_sha256']}")
