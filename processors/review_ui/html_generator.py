"""Stage 8: Local HTML Backtesting & Review Interface Generator."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from parsers.justprepy_wordlist.parser import RAW_OUTPUT_REL_PATH
from processors.enrichment.enricher import ENRICHED_OUTPUT_REL_PATH
from processors.normalization.cleaner import CLEAN_OUTPUT_REL_PATH
from processors.provenance import REPO_ROOT, sha256_file
from processors.validation.validator import (
    PRE_FINAL_OUTPUT_REL_PATH,
    PRE_FINAL_VALIDATION_REL_PATH,
)

HTML_REVIEW_REL_PATH = "inspections/review/vocabulary_review.html"


def generate_html_review(repo_root: Path = REPO_ROOT) -> Path:
    """Generate a self-contained local HTML QA interface from canonical pipeline JSON outputs."""
    pf_path = repo_root / PRE_FINAL_OUTPUT_REL_PATH
    pf_val_path = repo_root / PRE_FINAL_VALIDATION_REL_PATH
    raw_path = repo_root / RAW_OUTPUT_REL_PATH
    clean_path = repo_root / CLEAN_OUTPUT_REL_PATH
    enr_path = repo_root / ENRICHED_OUTPUT_REL_PATH

    for p in (pf_path, pf_val_path, raw_path, clean_path, enr_path):
        if not p.exists():
            raise FileNotFoundError(f"Required canonical JSON missing: {p}")

    pf_doc = json.loads(pf_path.read_text(encoding="utf-8"))
    pf_val = json.loads(pf_val_path.read_text(encoding="utf-8"))
    raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))
    clean_doc = json.loads(clean_path.read_text(encoding="utf-8"))

    records: list[dict[str, Any]] = pf_doc["records"]
    raw_by_num = {r["number"]: r for r in raw_doc["records"]}
    clean_by_num = {r["number"]: r for r in clean_doc["records"]}

    total_count = len(records)
    validated_count = pf_doc["summary"]["validated_count"]
    review_count = pf_doc["summary"]["review_pending_count"]
    error_count = pf_doc["summary"]["error_count"]
    excluded_count = pf_doc["summary"].get("excluded_count", 0)
    verbs_count = pf_doc["summary"]["verbs_count"]
    adjectives_count = pf_doc["summary"]["adjectives_count"]
    homograph_count = pf_doc["summary"]["cross_section_homograph_records"]
    two_word_ru_count = sum(1 for r in records if r["russian_word_count"] == 2)

    table_rows_html: list[str] = []
    for rec in records:
        num = rec["number"]
        raw_rec = raw_by_num[num]
        clean_rec = clean_by_num[num]

        status = rec["validation_status"]
        if status == "validated":
            badge_cls = "badge-validated"
            badge_label = "Validated"
        elif status == "review_pending":
            badge_cls = "badge-review"
            badge_label = "Review Pending"
        elif status == "excluded":
            badge_cls = "badge-excluded"
            badge_label = "Excluded (A1/A2)"
        else:
            badge_cls = "badge-error"
            badge_label = "Error"

        is_homograph = "true" if rec["is_cross_section_homograph"] else "false"
        sec_pos = rec["declared_section_pos"]
        ru_wc = rec["russian_word_count"]

        word_esc = html.escape(rec["word"])
        pos_esc = html.escape(rec["part_of_speech"])
        ru_esc = html.escape(rec["russian_translation"])
        en_esc = html.escape(rec["english_explanation"])

        spans = raw_rec["source_spans"]
        span_str = f"L{spans['line_number']}:{spans['line_char_start']}..{spans['line_char_end']} (file {spans['file_char_start']}..{spans['file_char_end']})"
        clean_meta = f"lemma={clean_rec['headword_lemma']}"
        if clean_rec.get("parenthetical_modifier"):
            clean_meta += f", modifier=({clean_rec['parenthetical_modifier']})"
        if clean_rec.get("spelling_convention") != "standard_shared":
            clean_meta += f", spelling={clean_rec['spelling_convention']}"

        extra_badges: list[str] = []
        rec_preset = rec.get("preset", "Basics")
        extra_badges.append(f'<span class="tag tag-preset" title="Preset">{html.escape(rec_preset)}</span>')
        rec_diff = rec.get("difficulty") or "Unset"
        rec_cefr = rec.get("cefr_level") or "N/A"
        diff_cls = f"tag-diff-{str(rec_diff).lower()}"
        extra_badges.append(f'<span class="tag {diff_cls}" title="Difficulty">{html.escape(str(rec_diff))} ({html.escape(str(rec_cefr))})</span>')
        if rec.get("final_output_eligible"):
            extra_badges.append('<span class="tag tag-eligible" title="Eligible for final website output">Eligible</span>')
        else:
            extra_badges.append(f'<span class="tag tag-blocked" title="Blocked: {html.escape(status.upper())}">Blocked</span>')

        if rec["is_cross_section_homograph"]:
            peer = rec["cross_section_homograph_numbers"][0]
            extra_badges.append(f'<span class="tag tag-homograph" title="Also appears at #{peer}">Homograph (#{peer})</span>')
        if rec.get("parenthetical_modifier"):
            extra_badges.append('<span class="tag tag-phrasal">Parenthetical</span>')
        if rec["spelling_convention"] != "standard_shared":
            extra_badges.append(f'<span class="tag tag-spelling">{html.escape(rec["spelling_convention"])}</span>')

        review_note = rec.get("Quality_and_review_notes")
        note_html = ""
        if review_note:
            note_html = f'<div class="review-note"><strong>QA Review Note:</strong> {html.escape(review_note)}</div>'
        if rec.get("validation_errors"):
            err_msgs = "; ".join(e["message"] for e in rec["validation_errors"])
            note_html += f'<div class="error-note"><strong>Validation Error:</strong> {html.escape(err_msgs)}</div>'

        row_cls = f"row-{status}"
        table_rows_html.append(
            f'<tr class="{row_cls}" '
            f'data-number="{num}" '
            f'data-status="{status}" '
            f'data-section="{sec_pos}" '
            f'data-homograph="{is_homograph}" '
            f'data-ru-words="{ru_wc}" '
            f'data-word="{word_esc.lower()}" '
            f'data-pos-final="{pos_esc}" '
            f'data-pos-clean="{html.escape(sec_pos)} (section header)" '
            f'data-pos-raw="{html.escape(raw_rec["section_header"])}" '
            f'data-ru-final="{ru_esc}" '
            f'data-en-final="{en_esc}" '
            f'data-span="{html.escape(span_str)}" '
            f'data-clean-meta="{html.escape(clean_meta)}">'
            f'<td class="col-num">{num}</td>'
            f'<td class="col-word">'
            f'<div class="word-main">{word_esc}</div>'
            f'<div class="word-meta"><code>{html.escape(rec["id"])}</code> {" ".join(extra_badges)}</div>'
            f'<div class="stage-trace">{html.escape(span_str)}</div>'
            f"</td>"
            f'<td class="col-pos">'
            f'<span class="cell-pos-val">{pos_esc}</span>'
            f'<div class="status-wrap"><span class="badge {badge_cls}">{badge_label}</span></div>'
            f"</td>"
            f'<td class="col-ru">'
            f'<span class="cell-ru-val">{ru_esc}</span> '
            f'<span class="wc-badge" title="Russian word count ({ru_wc} of max 2)">{ru_wc}w</span>'
            f"</td>"
            f'<td class="col-en">'
            f'<div class="cell-en-val">{en_esc}</div>'
            f"{note_html}"
            f"</td>"
            f"</tr>"
        )

    review_items_html: list[str] = []
    for iss in pf_val.get("issues", []):
        review_items_html.append(
            f'<li>'
            f'<a href="#" onclick="filterByNumber({iss["number"]}); return false;">'
            f'<strong>#{iss["number"]} {html.escape(iss["word"])}</strong> (<code>{html.escape(iss["record_id"])}</code>)'
            f"</a> — <span class=\"issue-code\">{html.escape(iss['issue_code'])}</span>: "
            f"{html.escape(iss['message'])}"
            f"</li>"
        )

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Vocabulary Pipeline Backtesting &amp; QA Review Interface</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --border: #cbd5e1;
      --border-light: #e2e8f0;
      --text: #0f172a;
      --text-muted: #475569;
      --accent: #1d4ed8;
      --ok-bg: #dcfce7;
      --ok-text: #166534;
      --ok-border: #86efac;
      --warn-bg: #fef9c3;
      --warn-text: #854d0e;
      --warn-border: #fde047;
      --err-bg: #fee2e2;
      --err-text: #991b1b;
      --err-border: #fca5a5;
      --pending-bg: #f1f5f9;
      --pending-text: #64748b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 20px 28px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 14px;
      line-height: 1.45;
      color: var(--text);
      background: var(--bg);
    }}
    header {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 16px 20px;
      margin-bottom: 16px;
    }}
    header h1 {{
      margin: 0 0 6px 0;
      font-size: 20px;
      font-weight: 700;
    }}
    .header-meta {{
      color: var(--text-muted);
      font-size: 12.5px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }}
    .stat-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 14px;
    }}
    .stat-label {{
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}
    .stat-val {{
      font-size: 22px;
      font-weight: 700;
    }}
    .stat-val.ok {{ color: var(--ok-text); }}
    .stat-val.warn {{ color: var(--warn-text); }}
    .stat-val.err {{ color: var(--err-text); }}
    .controls-panel {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 14px 18px;
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .control-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }}
    .control-label {{
      font-weight: 600;
      font-size: 12.5px;
      color: var(--text-muted);
      min-width: 115px;
    }}
    input[type="search"] {{
      flex: 1;
      min-width: 260px;
      padding: 7px 11px;
      border: 1px solid var(--border);
      border-radius: 4px;
      font-size: 13.5px;
    }}
    button.filter-btn, button.stage-btn {{
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 5px 11px;
      font-size: 12.5px;
      cursor: pointer;
      color: var(--text);
      font-weight: 500;
    }}
    button.filter-btn.active, button.stage-btn.active {{
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }}
    .stage-banner {{
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1e3a8a;
      padding: 8px 12px;
      border-radius: 4px;
      font-size: 12.5px;
    }}
    details.qa-summary {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 16px;
      margin-bottom: 16px;
    }}
    details.qa-summary summary {{
      cursor: pointer;
      font-weight: 600;
      font-size: 13.5px;
    }}
    details.qa-summary ul {{
      margin: 10px 0 4px 0;
      padding-left: 20px;
    }}
    details.qa-summary li {{
      margin-bottom: 6px;
    }}
    .issue-code {{
      font-family: monospace;
      background: var(--warn-bg);
      padding: 1px 5px;
      border-radius: 3px;
      font-size: 12px;
    }}
    .table-container {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border-light);
      text-align: left;
      vertical-align: top;
      word-wrap: break-word;
    }}
    th {{
      background: #f1f5f9;
      font-size: 12.5px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--text-muted);
      border-bottom: 2px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 1;
    }}
    th.col-num, td.col-num {{ width: 56px; font-variant-numeric: tabular-nums; font-weight: 600; color: var(--text-muted); }}
    th.col-word, td.col-word {{ width: 210px; }}
    th.col-pos, td.col-pos {{ width: 155px; }}
    th.col-ru, td.col-ru {{ width: 215px; }}
    th.col-en, td.col-en {{ width: auto; }}
    tr.row-review_pending {{ background: #fffbeb; }}
    tr.row-error {{ background: #fef2f2; }}
    tr.row-excluded {{ background: #f8fafc; opacity: 0.9; }}
    tr:hover {{ background: #f8fafc; }}
    tr.row-review_pending:hover {{ background: #fef3c7; }}
    .word-main {{ font-weight: 700; font-size: 14.5px; color: #0f172a; }}
    .word-meta {{ margin-top: 3px; font-size: 11px; color: var(--text-muted); display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }}
    .stage-trace {{ margin-top: 2px; font-size: 11px; color: #64748b; font-family: monospace; }}
    .badge {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 3px;
      font-size: 11px;
      font-weight: 600;
    }}
    .badge-validated {{ background: var(--ok-bg); color: var(--ok-text); border: 1px solid var(--ok-border); }}
    .badge-review {{ background: var(--warn-bg); color: var(--warn-text); border: 1px solid var(--warn-border); }}
    .badge-excluded {{ background: #e2e8f0; color: #475569; border: 1px solid #cbd5e1; }}
    .badge-error {{ background: var(--err-bg); color: var(--err-text); border: 1px solid var(--err-border); }}
    .badge-pending {{ background: var(--pending-bg); color: var(--pending-text); border: 1px solid var(--border); font-style: italic; }}
    .status-wrap {{ margin-top: 4px; }}
    .wc-badge {{
      display: inline-block;
      font-size: 11px;
      color: var(--text-muted);
      background: #f1f5f9;
      border: 1px solid var(--border-light);
      padding: 0 5px;
      border-radius: 3px;
      margin-left: 4px;
    }}
    .tag {{
      display: inline-block;
      padding: 1px 5px;
      border-radius: 3px;
      font-size: 10.5px;
      font-weight: 600;
    }}
    .tag-homograph {{ background: #e0e7ff; color: #3730a3; }}
    .tag-phrasal {{ background: #fae8ff; color: #86198f; }}
    .tag-spelling {{ background: #f1f5f9; color: #334155; }}
    .tag-preset {{ background: #e0e7ff; color: #3730a3; }}
    .tag-diff-easy {{ background: #dcfce7; color: #166534; }}
    .tag-diff-medium {{ background: #fef9c3; color: #854d0e; }}
    .tag-diff-hard {{ background: #fee2e2; color: #991b1b; }}
    .tag-eligible {{ background: #dcfce7; color: #15803d; }}
    .tag-blocked {{ background: #fee2e2; color: #b91c1c; }}
    .review-note {{
      margin-top: 6px;
      padding: 6px 8px;
      background: var(--warn-bg);
      border-left: 3px solid #eab308;
      font-size: 12px;
      color: var(--warn-text);
      border-radius: 2px;
    }}
    .error-note {{
      margin-top: 6px;
      padding: 6px 8px;
      background: var(--err-bg);
      border-left: 3px solid #ef4444;
      font-size: 12px;
      color: var(--err-text);
      border-radius: 2px;
    }}
    .cell-ru-val {{ font-weight: 600; font-size: 14px; }}
    .showing-bar {{
      font-size: 12.5px;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
  </style>
</head>
<body>
  <header>
    <h1>justprepy Vocabulary Parsing Pipeline — QA &amp; Backtesting Review Interface</h1>
    <div class="header-meta">
      <span><strong>Source:</strong> <code>{html.escape(pf_doc["source_file"])}</code> (SHA-256: <code>{pf_doc["source_sha256"][:16]}...</code>)</span>
      <span><strong>Canonical Dataset:</strong> <code>{PRE_FINAL_OUTPUT_REL_PATH}</code> (SHA-256: <code>{sha256_file(pf_path)[:16]}...</code>)</span>
      <span><strong>Difficulty Stage (Easy / Medium / Hard):</strong> <code>Architecturally Prepared — Unset (null)</code></span>
    </div>
  </header>

  <section class="stats-grid" aria-label="Dataset summary metrics">
    <div class="stat-card">
      <div class="stat-label">Total Records</div>
      <div class="stat-val" id="stat-total">{total_count}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Validated Records</div>
      <div class="stat-val ok" id="stat-validated">{validated_count}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Requires Review</div>
      <div class="stat-val warn" id="stat-review">{review_count}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Unresolved Errors</div>
      <div class="stat-val err" id="stat-errors">{error_count}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Verbs / Adjectives</div>
      <div class="stat-val">{verbs_count} / {adjectives_count}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Max Russian Words</div>
      <div class="stat-val ok">&le; 2 ({two_word_ru_count} 2w)</div>
    </div>
  </section>

  <details class="qa-summary" open>
    <summary>Active Stage Review Findings ({review_count} Review Pending, {error_count} Blocking Errors, {homograph_count} Cross-Section Homograph Records)</summary>
    <ul>
      {"".join(review_items_html)}
    </ul>
  </details>

  <section class="controls-panel" aria-label="Inspection filters and stage switcher">
    <div class="control-row">
      <span class="control-label">Pipeline Stage View:</span>
      <button type="button" class="stage-btn active" data-stage="pre_final" onclick="setStageView('pre_final', this)">PRE-FINAL / Validated (413)</button>
      <button type="button" class="stage-btn" data-stage="enriched" onclick="setStageView('enriched', this)">Enriched Stage (413)</button>
      <button type="button" class="stage-btn" data-stage="clean" onclick="setStageView('clean', this)">CLEAN Stage (Pre-Enrichment)</button>
      <button type="button" class="stage-btn" data-stage="raw" onclick="setStageView('raw', this)">RAW Stage (Source Spans Only)</button>
    </div>
    <div id="stage-banner" class="stage-banner">
      <strong>Viewing Stage: PRE-FINAL / Validated (`data/pre_final/vocabulary.json`)</strong> — Showing full validated records with Russian translations (&le;2 words), English explanations, and QA review status.
    </div>
    <div class="control-row">
      <span class="control-label">Status Filter:</span>
      <button type="button" class="filter-btn active" data-filter-status="all" onclick="setStatusFilter('all', this)">All ({total_count})</button>
      <button type="button" class="filter-btn" data-filter-status="validated" onclick="setStatusFilter('validated', this)">Validated ({validated_count})</button>
      <button type="button" class="filter-btn" data-filter-status="review_pending" onclick="setStatusFilter('review_pending', this)">Requires Review ({review_count})</button>
      <button type="button" class="filter-btn" data-filter-status="excluded" onclick="setStatusFilter('excluded', this)">Excluded A1/A2 ({excluded_count})</button>
      <button type="button" class="filter-btn" data-filter-status="error" onclick="setStatusFilter('error', this)">Unresolved Errors ({error_count})</button>
      <button type="button" class="filter-btn" data-filter-status="homograph" onclick="setStatusFilter('homograph', this)">Cross-Section Homographs ({homograph_count})</button>
      <button type="button" class="filter-btn" data-filter-status="two_word_ru" onclick="setStatusFilter('two_word_ru', this)">2-Word Russian ({two_word_ru_count})</button>
    </div>
    <div class="control-row">
      <span class="control-label">Part of Speech:</span>
      <button type="button" class="filter-btn active" data-filter-sec="all" onclick="setSectionFilter('all', this)">All Sections ({total_count})</button>
      <button type="button" class="filter-btn" data-filter-sec="verb" onclick="setSectionFilter('verb', this)">233 Verbs ({verbs_count})</button>
      <button type="button" class="filter-btn" data-filter-sec="adjective" onclick="setSectionFilter('adjective', this)">180 Adjectives ({adjectives_count})</button>
    </div>
    <div class="control-row">
      <span class="control-label">Search Records:</span>
      <input type="search" id="search-input" placeholder="Search by record # (e.g. #2, #346), English word, Russian translation, or explanation..." oninput="applyFilters()" />
      <button type="button" class="filter-btn" onclick="resetFilters()">Reset Filters</button>
    </div>
    <div class="showing-bar">
      <span id="showing-count">Showing <strong>{total_count}</strong> of <strong>{total_count}</strong> records</span>
      <span>Difficulty Field across all 413 records: <code>null (Unimplemented by design)</code></span>
    </div>
  </section>

  <main class="table-container">
    <table id="vocab-table">
      <thead>
        <tr>
          <th class="col-num">#</th>
          <th class="col-word">Word</th>
          <th class="col-pos">Part of Speech</th>
          <th class="col-ru">Russian Translation</th>
          <th class="col-en">English Explanation</th>
        </tr>
      </thead>
      <tbody id="vocab-tbody">
        {"".join(table_rows_html)}
      </tbody>
    </table>
  </main>

  <script>
    let currentStatusFilter = 'all';
    let currentSectionFilter = 'all';
    let currentStageView = 'pre_final';

    function setStageView(stage, btn) {{
      currentStageView = stage;
      document.querySelectorAll('.stage-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const banner = document.getElementById('stage-banner');
      const rows = document.querySelectorAll('#vocab-tbody tr');

      if (stage === 'raw') {{
        banner.innerHTML = '<strong>Viewing Stage: RAW (`data/raw/justprepy_wordlist/entries.raw.json`)</strong> — Showing exact extracted tokens and file character spans. Linguistic enrichment fields are explicitly shown as <em>Pending Enrichment</em> (not yet available at RAW stage).';
      }} else if (stage === 'clean') {{
        banner.innerHTML = '<strong>Viewing Stage: CLEAN (`data/clean/justprepy_wordlist/entries.clean.json`)</strong> — Showing normalized headword lemmas, particles, and token-ledger verification. Russian translations and English explanations are explicitly <em>Pending Enrichment</em>.';
      }} else if (stage === 'enriched') {{
        banner.innerHTML = '<strong>Viewing Stage: ENRICHMENT (`data/enriched/justprepy_wordlist/entries.enriched.json`)</strong> — Showing populated Part of Speech, Russian Translation (&le;2 words), and English Explanation prior to PRE-FINAL admission.';
      }} else {{
        banner.innerHTML = '<strong>Viewing Stage: PRE-FINAL / Validated (`data/pre_final/vocabulary.json`)</strong> — Showing full validated records with Russian translations (&le;2 words), English explanations, and QA review status.';
      }}

      rows.forEach(row => {{
        const posCell = row.querySelector('.cell-pos-val');
        const ruCell = row.querySelector('.col-ru');
        const enCell = row.querySelector('.cell-en-val');

        if (stage === 'raw') {{
          posCell.textContent = row.dataset.posRaw;
          ruCell.innerHTML = '<span class="badge badge-pending">Pending (RAW stage)</span>';
          enCell.innerHTML = '<span class="badge badge-pending">Pending (RAW stage) — Span: ' + row.dataset.span + '</span>';
        }} else if (stage === 'clean') {{
          posCell.textContent = row.dataset.posClean;
          ruCell.innerHTML = '<span class="badge badge-pending">Pending (CLEAN stage)</span>';
          enCell.innerHTML = '<span class="badge badge-pending">Pending (CLEAN stage) — ' + row.dataset.cleanMeta + '</span>';
        }} else {{
          posCell.textContent = row.dataset.posFinal;
          ruCell.innerHTML = '<span class="cell-ru-val">' + row.dataset.ruFinal + '</span> <span class="wc-badge">' + row.dataset.ruWords + 'w</span>';
          enCell.textContent = row.dataset.enFinal;
        }}
      }});
    }}

    function setStatusFilter(status, btn) {{
      currentStatusFilter = status;
      document.querySelectorAll('[data-filter-status]').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyFilters();
    }}

    function setSectionFilter(sec, btn) {{
      currentSectionFilter = sec;
      document.querySelectorAll('[data-filter-sec]').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyFilters();
    }}

    function filterByNumber(num) {{
      document.getElementById('search-input').value = '#' + num;
      setStatusFilter('all', document.querySelector('[data-filter-status="all"]'));
      setSectionFilter('all', document.querySelector('[data-filter-sec="all"]'));
      applyFilters();
    }}

    function resetFilters() {{
      document.getElementById('search-input').value = '';
      setStatusFilter('all', document.querySelector('[data-filter-status="all"]'));
      setSectionFilter('all', document.querySelector('[data-filter-sec="all"]'));
      setStageView('pre_final', document.querySelector('[data-stage="pre_final"]'));
      applyFilters();
    }}

    function applyFilters() {{
      const query = document.getElementById('search-input').value.trim().toLowerCase();
      const rows = document.querySelectorAll('#vocab-tbody tr');
      let visible = 0;

      rows.forEach(row => {{
        let matchStatus = true;
        if (currentStatusFilter === 'validated') matchStatus = row.dataset.status === 'validated';
        else if (currentStatusFilter === 'review_pending') matchStatus = row.dataset.status === 'review_pending';
        else if (currentStatusFilter === 'excluded') matchStatus = row.dataset.status === 'excluded';
        else if (currentStatusFilter === 'error') matchStatus = row.dataset.status === 'error';
        else if (currentStatusFilter === 'homograph') matchStatus = row.dataset.homograph === 'true';
        else if (currentStatusFilter === 'two_word_ru') matchStatus = row.dataset.ruWords === '2';

        let matchSec = true;
        if (currentSectionFilter !== 'all') {{
          matchSec = row.dataset.section === currentSectionFilter;
        }}

        let matchQuery = true;
        if (query) {{
          if (query.startsWith('#')) {{
            matchQuery = ('#' + row.dataset.number) === query;
          }} else {{
            const text = row.textContent.toLowerCase();
            matchQuery = text.includes(query);
          }}
        }}

        if (matchStatus && matchSec && matchQuery) {{
          row.style.display = '';
          visible++;
        }} else {{
          row.style.display = 'none';
        }}
      }});

      document.getElementById('showing-count').innerHTML =
        'Showing <strong>' + visible + '</strong> of <strong>{total_count}</strong> records';
    }}
  </script>
</body>
</html>
"""

    out_path = repo_root / HTML_REVIEW_REL_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_doc, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    p = generate_html_review()
    print(f"Generated HTML review interface at: {p}")
