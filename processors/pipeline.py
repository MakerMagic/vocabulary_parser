"""Unified CLI entry point for running and backtesting the Vocabulary Parsing Pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from parsers.justprepy_wordlist.parser import run_raw_extraction
from processors.acquisition import run_acquisition
from processors.enrichment.enricher import run_enrichment
from processors.inspection import run_inspection
from processors.normalization.cleaner import run_cleaning
from processors.provenance import REPO_ROOT
from processors.review_ui.html_generator import generate_html_review
from processors.validation.validator import run_validation


def run_all(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Execute all implemented pipeline stages in topological order and generate the HTML review UI."""
    acq = run_acquisition(repo_root)
    insp = run_inspection(repo_root)
    raw = run_raw_extraction(repo_root)
    clean = run_cleaning(repo_root)
    enr = run_enrichment(repo_root)
    val = run_validation(repo_root)
    html_path = generate_html_review(repo_root)
    return {
        "acquisition": acq,
        "clean": clean,
        "enrichment": enr,
        "html_review_path": str(html_path),
        "inspection": insp,
        "raw": raw,
        "validation": val,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Vocabulary Parsing Pipeline Runner")
    parser.add_argument(
        "stage",
        nargs="?",
        default="all",
        choices=["all", "acquisition", "inspection", "raw", "clean", "enrichment", "validation", "html"],
        help="Pipeline stage to execute (default: all)",
    )
    args = parser.parse_args()

    if args.stage == "acquisition":
        run_acquisition()
    elif args.stage == "inspection":
        run_inspection()
    elif args.stage == "raw":
        run_raw_extraction()
    elif args.stage == "clean":
        run_cleaning()
    elif args.stage == "enrichment":
        run_enrichment()
    elif args.stage == "validation":
        run_validation()
    elif args.stage == "html":
        generate_html_review()
    else:
        res = run_all()
        summary = res["validation"]["summary"]
        print(
            f"Pipeline complete: entered={summary['entered_count']}, "
            f"validated={summary['succeeded_count']}, "
            f"review_pending={summary['review_pending_count']}, "
            f"errors={summary['error_count']}. "
            f"HTML: {res['html_review_path']}"
        )


if __name__ == "__main__":
    main()
