"""Deterministic generator for categorized stage issue reports and backtesting artifacts.

Adheres strictly to the error-type grouping requirements:
- Groups issues by TYPE OF ERROR / Category.
- Outputs upfront ISSUE SUMMARY with counts per category and total distinct issues.
- Distinguishes total issue occurrences from unique affected records.
- Records structured metadata: Category name, issue count, affected entries, problem description,
  actual output, expected output, root cause, corrective action, backtesting command, and resolution status.
- Writes to both qa/ and qa/sources/<source_id>/.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from processors.provenance import REPO_ROOT

QA_DIR = REPO_ROOT / "qa"


def write_stage_qa_pair(
    stage_name: str,
    validation_data: dict[str, Any],
    backtesting_commands: list[str],
    verification_steps: list[str],
    source_id: str = "uclouvain",
) -> tuple[Path, Path]:
    """Generate categorized <STAGE>_BACKTESTING.md and <STAGE>_ISSUES.md reports."""
    stage_upper = stage_name.upper()
    QA_DIR.mkdir(parents=True, exist_ok=True)
    source_qa_dir = QA_DIR / "sources" / source_id
    source_qa_dir.mkdir(parents=True, exist_ok=True)

    backtest_path = QA_DIR / f"{stage_upper}_BACKTESTING.md"
    issues_path = QA_DIR / f"{stage_upper}_ISSUES.md"
    source_issues_path = source_qa_dir / f"{stage_upper}_ISSUES.md"

    summary = validation_data["summary"]
    issues = validation_data.get("issues", [])
    stage_desc = validation_data.get("description", f"{stage_upper} pipeline stage")
    input_artifact = validation_data.get("input_artifact", "N/A")
    output_artifact = validation_data.get("output_artifact", "N/A")
    validation_artifact = validation_data.get("validation_artifact", "N/A")

    # Group issues by category
    categories_map: dict[str, list[dict[str, Any]]] = {}
    unique_affected_ids: set[str] = set()

    for item in issues:
        cat = item.get("category") or item.get("issue_code") or "General Stage Findings"
        categories_map.setdefault(cat, []).append(item)
        rec_id = item.get("record_id") or str(item.get("number", ""))
        if rec_id:
            unique_affected_ids.add(rec_id)

    total_issue_occurrences = len(issues)
    unique_affected_records = len(unique_affected_ids)

    # 1. Build <STAGE>_BACKTESTING.md
    bt_lines = [
        f"# {stage_upper} Stage Backtesting Report (`{stage_upper}_BACKTESTING.md`)",
        "",
        f"> **Source:** `{source_id}`  ",
        f"> **Generated deterministically from:** `{validation_artifact}`  ",
        f"> **Stage Status:** `{validation_data.get('stage_status', 'completed')}`",
        "",
        "## 1. Stage Execution Summary",
        "",
        f"- **What was processed:** {stage_desc}",
        f"- **Input artifact:** `{input_artifact}` (SHA-256: `{validation_data.get('input_sha256', 'N/A')}`)",
        f"- **Output artifact:** `{output_artifact}` (SHA-256: `{validation_data.get('output_sha256', 'N/A')}`)",
        "",
        "| Metric | Count |",
        "|---|---|",
        f"| **Records Entered Stage** | `{summary['entered_count']}` |",
        f"| **Successfully Processed (Clean/Validated)** | `{summary['succeeded_count']}` |",
        f"| **Excluded from Eligible Dataset (e.g. A1/A2)** | `{summary.get('excluded_count', 0)}` |",
        f"| **Flagged for Review (`review_pending`)** | `{summary.get('review_pending_count', 0)}` |",
        f"| **Unresolved Blocking Errors (`error`)** | `{summary.get('error_count', 0)}` |",
        f"| **Total Distinct Issue Occurrences** | `{total_issue_occurrences}` |",
        f"| **Unique Affected Records** | `{unique_affected_records}` |",
        "",
    ]

    partition = validation_data.get("primary_reason_partition", {})
    if partition:
        bt_lines.extend([
            "## 2. Primary-Reason Partition (Disjoint Record Counts)",
            "",
            "| Primary State / Reason | Unique Record Count |",
            "|---|---|",
        ])
        for k, v in partition.items():
            bt_lines.append(f"| `{k}` | `{v}` |")
        bt_lines.append("")

    checks = validation_data.get("invariant_checks", [])
    if checks:
        bt_lines.extend([
            "## 3. Automated Invariant Checks",
            "",
            "| Check Name | Status | Details |",
            "|---|---|---|",
        ])
        for chk in checks:
            bt_lines.append(f"| `{chk['name']}` | **{chk['status']}** | {chk['details']} |")
        bt_lines.append("")

    bt_lines.extend([
        "## 4. Reproducible Backtesting Commands",
        "",
        "Run the following commands from the repository root:",
        "",
        "```powershell",
    ])
    bt_lines.extend(backtesting_commands)
    bt_lines.extend([
        "```",
        "",
        "## 5. Verification Procedure",
        "",
    ])
    for idx, step in enumerate(verification_steps, 1):
        bt_lines.append(f"{idx}. {step}")
    bt_lines.append("")

    backtest_content = "\n".join(bt_lines)
    backtest_path.write_text(backtest_content, encoding="utf-8")
    (source_qa_dir / f"{stage_upper}_BACKTESTING.md").write_text(backtest_content, encoding="utf-8")

    # 2. Build <STAGE>_ISSUES.md grouped by error category
    iss_lines = [
        f"# {stage_upper} Stage Issues Report (`{stage_upper}_ISSUES.md`)",
        "",
        f"> **Source:** `{source_id}`  ",
        f"> **Generated deterministically from:** `{validation_artifact}`  ",
        f"> **Total Issue Occurrences:** `{total_issue_occurrences}`  ",
        f"> **Unique Affected Records:** `{unique_affected_records}`",
        "",
        "```text",
        f"ISSUE SUMMARY — {source_id.upper()} / {stage_upper}",
    ]

    for cat_name, cat_items in sorted(categories_map.items()):
        iss_lines.append(f"{cat_name}: {len(cat_items)}")

    iss_lines.extend([
        f"TOTAL DISTINCT ISSUES: {total_issue_occurrences}",
        f"UNIQUE AFFECTED RECORDS: {unique_affected_records}",
        "```",
        "",
        "---",
        "",
        "## 1. Issue Summary by Error Category",
        "",
        "| Error Category | Issue Occurrences | Unique Records | Primary Severity |",
        "|---|---|---|---|",
    ])

    for cat_name, cat_items in sorted(categories_map.items()):
        cat_rec_ids = {it.get("record_id", str(it.get("number", ""))) for it in cat_items}
        sev = cat_items[0].get("severity", "notice") if cat_items else "notice"
        iss_lines.append(f"| `{cat_name}` | `{len(cat_items)}` | `{len(cat_rec_ids)}` | `{sev}` |")

    iss_lines.extend([
        f"| **TOTAL DISTINCT ISSUES** | **`{total_issue_occurrences}`** | **`{unique_affected_records}`** | |",
        "",
        "---",
        "",
        "## 2. Itemized Issues Grouped by Error Category",
        "",
    ])

    if not issues:
        iss_lines.extend([
            "**0 active issues detected in this stage.**",
            "",
            "All input records satisfied every invariant check for this stage.",
            "",
        ])
    else:
        for cat_name, cat_items in sorted(categories_map.items()):
            iss_lines.extend([
                f"### Category: {cat_name} (Count: {len(cat_items)})",
                "",
                "- **Affected Vocabulary Entries:** "
                + ", ".join(f"`{it.get('word', 'N/A')}` (#{it.get('number', '?')})" for it in cat_items[:15])
                + (f" ... and {len(cat_items) - 15} more" if len(cat_items) > 15 else ""),
                "",
            ])

            for idx, item in enumerate(cat_items, 1):
                iss_lines.extend([
                    f"#### [{cat_name[:4].upper()}-{idx:03d}] `#{item.get('number', '?')}` (`{item.get('record_id', 'N/A')}`) — `{item.get('word', 'N/A')}`",
                    "",
                    f"- **Problem Description:** {item.get('message', 'N/A')}",
                    f"- **Actual Observed Output:** `{item.get('actual_output', item.get('message', 'N/A'))}`",
                    f"- **Expected Output:** `{item.get('expected_output', item.get('corrective_action', 'N/A'))}`",
                    f"- **Root Cause:** {item.get('root_cause', 'N/A')}",
                    f"- **Corrective Action:** {item.get('corrective_action', 'N/A')}",
                    f"- **Verification / Backtesting:** `{item.get('reproduction_command', 'N/A')}`",
                    f"- **Resolution Status:** `{item.get('resolution_status', item.get('severity', 'open'))}`",
                    "",
                ])

    issues_content = "\n".join(iss_lines)
    issues_path.write_text(issues_content, encoding="utf-8")
    source_issues_path.write_text(issues_content, encoding="utf-8")
    return backtest_path, issues_path
