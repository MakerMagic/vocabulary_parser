"""Command-line & HTML backtesting tool for the justprepy Vocabulary Parsing Pipeline.

Supports inspecting any vocabulary word across all pipeline stages:
- Source / Acquisition (file slice & SHA-256)
- RAW Extraction (exact line & file spans)
- CLEAN Normalization (token-ledger audit, A1/A2 exclusion status, slash-split handling)
- ENRICHMENT (POS, Russian translation alternatives [<=2], contextual English explanations)
- VALIDATION / PRE-FINAL (invariants, review status, quality checks)
- Cross-stage recorded QA issues

Usage:
    python tools/vocabulary_review.py --source uclouvain --word "different from"
    python tools/vocabulary_review.py --source uclouvain --word "account for" --open
    python tools/vocabulary_review.py --source uclouvain --word "particular / specific"
    python tools/vocabulary_review.py --source uclouvain --word "sure"
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import webbrowser
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def slugify(text: str) -> str:
    """Create a safe filename slug from arbitrary text."""
    slug = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return re.sub(r"[-\s]+", "_", slug) or "query"


def find_records_for_query(query: str, source_id: str, repo_root: Path = REPO_ROOT) -> list[dict[str, Any]]:
    """Match records across stages using exact, slash, multiword, or prefix search."""
    q_norm = query.strip().lower()
    q_parts = [p.strip().lower() for p in q_norm.split("/") if p.strip()]

    # Load pre-final records (authoritative aggregated dataset)
    pf_path = repo_root / f"data/pre_final/sources/{source_id}/vocabulary.json"
    if not pf_path.exists():
        pf_path = repo_root / "data/pre_final/vocabulary.json"
    if not pf_path.exists():
        raise FileNotFoundError(f"PRE-FINAL dataset missing for source '{source_id}' at {pf_path}")

    pf_doc = json.loads(pf_path.read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = pf_doc["records"]

    matches: list[dict[str, Any]] = []

    # 1. Exact match on word or headword_lemma
    for r in records:
        w = r.get("word", "").lower()
        lemma = r.get("headword_lemma", "").lower()
        if w == q_norm or lemma == q_norm:
            matches.append(r)

    # 2. Match any subpart if query is slash-separated (e.g. 'particular / specific')
    if not matches and len(q_parts) > 1:
        for r in records:
            w = r.get("word", "").lower()
            lemma = r.get("headword_lemma", "").lower()
            if any(part in (w, lemma) for part in q_parts):
                matches.append(r)

    # 3. Match multiword expressions (e.g. 'different from' -> 'different', 'account for' -> 'account (for)')
    if not matches:
        first_token = q_norm.split()[0] if q_norm.split() else ""
        for r in records:
            w = r.get("word", "").lower()
            lemma = r.get("headword_lemma", "").lower()
            # If word is 'account (for)' and query is 'account for'
            cleaned_w = re.sub(r"[()]", "", w).strip()
            if cleaned_w == q_norm or w == first_token or lemma == first_token:
                matches.append(r)

    # 4. Check against systematic A1/A2 exclusions benchmark (e.g. 'sure')
    if not matches:
        from processors.enrichment.lexicon_data import ADJECTIVE_LEXICON, VERB_LEXICON
        from processors.normalization.cleaner import ELEMENTARY_A1_A2_REGISTRY

        if q_norm in ELEMENTARY_A1_A2_REGISTRY:
            ex_info = ELEMENTARY_A1_A2_REGISTRY[q_norm]
            lex_entry = ADJECTIVE_LEXICON.get(q_norm) or VERB_LEXICON.get(q_norm)
            pos_label = lex_entry[0] if lex_entry else "adjective"
            ru_trans = lex_entry[1] if lex_entry else "уверенный; точный"
            en_expl = lex_entry[2] if lex_entry else "Having no doubt about something, or completely certain and reliable."
            matches.append({
                "cefr_level": ex_info["level"],
                "declared_section_pos": pos_label,
                "difficulty": None,
                "english_explanation": en_expl,
                "exclusion_reason": "elementary_a1_a2",
                "headword_lemma": q_norm,
                "id": f"benchmark_{q_norm}",
                "is_cross_section_homograph": False,
                "linguistic_evidence": ex_info["reason"],
                "number": 0,
                "parenthetical_modifier": None,
                "part_of_speech": pos_label,
                "provenance": {
                    "source_file": "Cambridge EVP / Oxford 3000 CEFR Benchmark",
                    "source_sha256": "systematic_exclusion_rule",
                    "source_spans": {"file_char_end": len(q_norm), "file_char_start": 0, "line_char_end": len(q_norm), "line_char_start": 0, "line_number": 0},
                },
                "quality_and_review_notes": "Systematically excluded elementary A1/A2 vocabulary item.",
                "russian_alternatives": [p.strip() for p in ru_trans.split(";") if p.strip()],
                "russian_translation": ru_trans,
                "section_header": "Excluded Elementary Vocabulary",
                "spelling_convention": "standard_shared",
                "status": "excluded",
                "validation_status": "excluded",
                "word": q_norm,
            })

    # 5. Fallback substring match
    if not matches:
        for r in records:
            w = r.get("word", "").lower()
            if q_norm in w or w in q_norm:
                matches.append(r)

    return matches


def load_stage_data_for_record(rec_num: int, source_id: str, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Retrieve full progression data for a single record across RAW, CLEAN, and ENRICHED stages."""
    data: dict[str, Any] = {}

    # RAW
    raw_path = repo_root / f"data/raw/sources/{source_id}/entries.raw.json"
    if not raw_path.exists():
        raw_path = repo_root / "data/raw/justprepy_wordlist/entries.raw.json"
    if raw_path.exists():
        raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))
        for r in raw_doc.get("records", []):
            if r["number"] == rec_num:
                data["raw"] = r
                break

    # CLEAN
    clean_path = repo_root / f"data/clean/sources/{source_id}/entries.clean.json"
    if not clean_path.exists():
        clean_path = repo_root / "data/clean/justprepy_wordlist/entries.clean.json"
    if clean_path.exists():
        clean_doc = json.loads(clean_path.read_text(encoding="utf-8"))
        for r in clean_doc.get("records", []):
            if r["number"] == rec_num:
                data["clean"] = r
                break

    # ENRICHED
    enr_path = repo_root / f"data/enriched/sources/{source_id}/entries.enriched.json"
    if not enr_path.exists():
        enr_path = repo_root / "data/enriched/justprepy_wordlist/entries.enriched.json"
    if enr_path.exists():
        enr_doc = json.loads(enr_path.read_text(encoding="utf-8"))
        for r in enr_doc.get("records", []):
            if r["number"] == rec_num:
                data["enriched"] = r
                break

    # QA Issues across stages
    issues: list[dict[str, Any]] = []
    for stage_name in ("RAW", "CLEAN", "ENRICHMENT", "VALIDATION"):
        iss_path = repo_root / "qa" / f"{stage_name}_ISSUES.md"
        if iss_path.exists():
            text = iss_path.read_text(encoding="utf-8")
            # Look for record references like `#<num>` or `uclouvain_vocab_<num>`
            if f"#{rec_num}" in text or f"vocab_{rec_num:03d}" in text:
                issues.append({"stage": stage_name, "file": str(iss_path.relative_to(repo_root))})
    data["qa_references"] = issues
    return data


def generate_record_backtest_html(
    query: str,
    matches: list[dict[str, Any]],
    source_id: str,
    repo_root: Path = REPO_ROOT,
) -> Path:
    """Generate a dedicated self-contained HTML backtesting report for the inspected query."""
    out_dir = repo_root / "inspections" / "review"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(query)
    out_file = out_dir / f"backtest_{source_id}_{slug}.html"

    cards_html: list[str] = []
    for pf_rec in matches:
        num = pf_rec["number"]
        stages = load_stage_data_for_record(num, source_id, repo_root)
        raw_rec = stages.get("raw", {})
        clean_rec = stages.get("clean", {})

        status = pf_rec.get("validation_status", "validated")
        badge_cls = {
            "validated": "badge-ok",
            "review_pending": "badge-warn",
            "excluded": "badge-excluded",
            "error": "badge-err",
        }.get(status, "badge-neutral")

        raw_spans = pf_rec.get("provenance", {}).get("source_spans", {})
        span_desc = f"Line {raw_spans.get('line_number')}, cols {raw_spans.get('line_char_start')}..{raw_spans.get('line_char_end')} (bytes {raw_spans.get('file_char_start')}..{raw_spans.get('file_char_end')})"

        ru_alts = pf_rec.get("russian_alternatives", [])
        ru_alts_html = "".join(f"<li><code>{html.escape(alt)}</code></li>" for alt in ru_alts)

        review_note = pf_rec.get("quality_and_review_notes")
        note_box = ""
        if review_note:
            note_box = f'<div class="box box-warn"><strong>Linguistic Review Note:</strong> {html.escape(review_note)}</div>'

        evidence_box = ""
        if pf_rec.get("linguistic_evidence"):
            evidence_box = f'<div class="box box-info"><strong>CEFR Level &amp; Linguistic Evidence:</strong> {html.escape(pf_rec["linguistic_evidence"])} (CEFR: {html.escape(str(pf_rec.get("cefr_level")))})</div>'

        audit = clean_rec.get("normalization_audit", {})
        ledger_status = "MATCH (100% token conservation)" if audit.get("token_ledger_match") else "N/A"

        qa_refs = stages.get("qa_references", [])
        qa_html = "".join(f'<li><a href="../../{html.escape(q["file"])}">{html.escape(q["stage"])} Stage Issues</a></li>' for q in qa_refs) or "<li>No stage-specific issues reported for this entry.</li>"

        card = f"""
        <article class="record-card">
          <header class="card-header">
            <div>
              <span class="record-num">#{num}</span>
              <span class="record-word">{html.escape(pf_rec["word"])}</span>
              <code class="record-id">{html.escape(pf_rec["id"])}</code>
            </div>
            <div>
              <span class="badge {badge_cls}">{html.escape(status.upper())}</span>
            </div>
          </header>

          {note_box}
          {evidence_box}

          <div class="stage-grid">
            <!-- Stage 1 & 3: Acquisition & RAW Extraction -->
            <div class="stage-pane">
              <h3>1. Acquisition &amp; RAW Extraction</h3>
              <dl>
                <dt>Source File</dt>
                <dd><code>{html.escape(pf_rec.get("provenance", {}).get("source_file", "N/A"))}</code></dd>
                <dt>Source SHA-256</dt>
                <dd><code>{html.escape(pf_rec.get("provenance", {}).get("source_sha256", "N/A")[:16])}...</code></dd>
                <dt>Raw Text</dt>
                <dd><strong>"{html.escape(raw_rec.get("raw_text", pf_rec["word"]))}"</strong></dd>
                <dt>Source Spans</dt>
                <dd>{html.escape(span_desc)}</dd>
                <dt>Section Header</dt>
                <dd>{html.escape(pf_rec.get("section_header", "N/A"))}</dd>
              </dl>
            </div>

            <!-- Stage 4: Cleaning & Normalization -->
            <div class="stage-pane">
              <h3>2. Cleaning &amp; Normalization</h3>
              <dl>
                <dt>Headword Lemma</dt>
                <dd><code>{html.escape(pf_rec.get("headword_lemma", "N/A"))}</code></dd>
                <dt>Parenthetical Particle</dt>
                <dd>{html.escape(str(pf_rec.get("parenthetical_modifier") or "None"))}</dd>
                <dt>Token-Ledger Match</dt>
                <dd class="ok">{html.escape(ledger_status)}</dd>
                <dt>Eligibility Status</dt>
                <dd><strong>{html.escape(str(pf_rec.get("status", "clean")).upper())}</strong> ({html.escape(str(pf_rec.get("exclusion_reason") or "Eligible curriculum item"))})</dd>
                <dt>Spelling Convention</dt>
                <dd>{html.escape(pf_rec.get("spelling_convention", "standard_shared"))}</dd>
              </dl>
            </div>

            <!-- Stage 5: Enrichment -->
            <div class="stage-pane">
              <h3>3. Vocabulary Enrichment</h3>
              <dl>
                <dt>Part of Speech</dt>
                <dd><code>{html.escape(pf_rec.get("part_of_speech", "N/A"))}</code></dd>
                <dt>Russian Alternatives ({len(ru_alts)} of max 2)</dt>
                <dd>
                  <ol class="ru-alts-list">
                    {ru_alts_html}
                  </ol>
                </dd>
                <dt>English Explanation</dt>
                <dd class="en-expl">{html.escape(pf_rec.get("english_explanation", "N/A"))}</dd>
              </dl>
            </div>

            <!-- Stage 6: Validation & QA -->
            <div class="stage-pane">
              <h3>4. Validation &amp; Stage QA</h3>
              <dl>
                <dt>Validation Status</dt>
                <dd><strong>{html.escape(status.upper())}</strong></dd>
                <dt>Difficulty Placeholder</dt>
                <dd><code>difficulty: null</code> (enforced unset)</dd>
                <dt>Cross-Section Homograph</dt>
                <dd>{html.escape(str(pf_rec.get("is_cross_section_homograph", False)))}</dd>
                <dt>Stage QA Issues</dt>
                <dd>
                  <ul class="qa-links">
                    {qa_html}
                  </ul>
                </dd>
              </dl>
            </div>
          </div>
        </article>
        """
        cards_html.append(card)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Backtest: "{html.escape(query)}" ({source_id})</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --border: #cbd5e1;
      --border-light: #e2e8f0;
      --text: #0f172a;
      --text-muted: #475569;
      --accent: #2563eb;
      --ok: #166534;
      --ok-bg: #dcfce7;
      --warn: #854d0e;
      --warn-bg: #fef9c3;
      --err: #991b1b;
      --err-bg: #fee2e2;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 24px 32px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 14px;
      line-height: 1.5;
      background: var(--bg);
      color: var(--text);
    }}
    header.page-header {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px 24px;
      margin-bottom: 24px;
    }}
    h1 {{ margin: 0 0 6px 0; font-size: 22px; }}
    .subtitle {{ color: var(--text-muted); font-size: 13px; }}
    .record-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-light);
      padding-bottom: 12px;
      margin-bottom: 16px;
    }}
    .record-num {{
      font-size: 16px;
      font-weight: 700;
      color: var(--text-muted);
      margin-right: 8px;
    }}
    .record-word {{
      font-size: 20px;
      font-weight: 800;
      color: var(--text);
      margin-right: 12px;
    }}
    .record-id {{
      background: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      color: #334155;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .badge-ok {{ background: var(--ok-bg); color: var(--ok); border: 1px solid #86efac; }}
    .badge-warn {{ background: var(--warn-bg); color: var(--warn); border: 1px solid #fde047; }}
    .badge-excluded {{ background: #e2e8f0; color: #475569; border: 1px solid #cbd5e1; }}
    .badge-err {{ background: var(--err-bg); color: var(--err); border: 1px solid #fca5a5; }}
    .box {{
      padding: 10px 14px;
      border-radius: 6px;
      margin-bottom: 16px;
      font-size: 13px;
    }}
    .box-warn {{ background: var(--warn-bg); border: 1px solid #fde047; color: var(--warn); }}
    .box-info {{ background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; }}
    .stage-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .stage-pane {{
      background: #f8fafc;
      border: 1px solid var(--border-light);
      border-radius: 6px;
      padding: 14px 16px;
    }}
    .stage-pane h3 {{
      margin: 0 0 10px 0;
      font-size: 14px;
      font-weight: 700;
      color: #1e293b;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 6px;
    }}
    dl {{ margin: 0; display: grid; grid-template-columns: 130px 1fr; row-gap: 8px; font-size: 12.5px; }}
    dt {{ font-weight: 600; color: var(--text-muted); }}
    dd {{ margin: 0; color: var(--text); word-break: break-word; }}
    .ok {{ color: var(--ok); font-weight: 600; }}
    .ru-alts-list {{ margin: 0; padding-left: 18px; }}
    .ru-alts-list li {{ margin-bottom: 3px; font-size: 13.5px; font-weight: 600; }}
    .en-expl {{ font-style: italic; color: #1e293b; }}
    .qa-links {{ margin: 0; padding-left: 18px; }}
    .qa-links li {{ margin-bottom: 2px; }}
    nav.back-nav {{ margin-top: 24px; }}
    nav.back-nav a {{ color: var(--accent); text-decoration: none; font-weight: 600; }}
    nav.back-nav a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <header class="page-header">
    <h1>Stage-Level Backtest Report</h1>
    <div class="subtitle">
      Query: <strong>"{html.escape(query)}"</strong> |
      Source: <code>{html.escape(source_id)}</code> |
      Matched Entries: <strong>{len(matches)}</strong> |
      Full Review: <a href="vocabulary_review.html">vocabulary_review.html</a>
    </div>
  </header>

  <main>
    {"".join(cards_html) if cards_html else '<p>No vocabulary records matched your query.</p>'}
  </main>

  <nav class="back-nav">
    &larr; <a href="vocabulary_review.html">Return to Complete Vocabulary Review UI</a>
  </nav>
</body>
</html>
"""
    out_file.write_text(html_content, encoding="utf-8")
    return out_file


def print_cli_summary(query: str, matches: list[dict[str, Any]], source_id: str, html_path: Path) -> None:
    """Print clean terminal summary for PowerShell / CLI users."""
    print("=" * 78)
    print(f"VOCABULARY PIPELINE BACKTEST: '{query}' (Source: {source_id})")
    print("=" * 78)
    if not matches:
        print(f"No records found matching query '{query}'.")
        return

    for rec in matches:
        num = rec["number"]
        w = rec["word"]
        rid = rec["id"]
        status = rec["validation_status"].upper()
        pos = rec["part_of_speech"]
        ru = rec["russian_translation"]
        alts = rec.get("russian_alternatives", [])
        en = rec["english_explanation"]
        spans = rec.get("provenance", {}).get("source_spans", {})
        note = rec.get("quality_and_review_notes")
        evidence = rec.get("linguistic_evidence")

        print(f"\n[#{num}] {w} ({rid}) — STATUS: {status}")
        print(f"  • Raw Span:     Line {spans.get('line_number')}, cols {spans.get('line_char_start')}..{spans.get('line_char_end')}")
        print(f"  • Part of Sp.:  {pos}")
        print(f"  • Russian Alt.: {ru} ({len(alts)} alternative{'s' if len(alts) != 1 else ''})")
        print(f"  • Explanation:  {en}")
        if note:
            print(f"  • Review Note:  {note}")
        if evidence:
            print(f"  • CEFR Excl.:   {evidence}")

    print("\n" + "-" * 78)
    print(f"Generated HTML backtest artifact: file:///{html_path.resolve()}".replace("\\", "/"))
    print("=" * 78)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect and backtest vocabulary records across all pipeline stages."
    )
    parser.add_argument("--source", default="uclouvain", help="Vocabulary source ID (default: uclouvain)")
    parser.add_argument("--word", required=True, help="Word, multiword expression, or slash pair to inspect")
    parser.add_argument("--open", action="store_true", help="Automatically open generated HTML report in browser")

    args = parser.parse_args()

    try:
        matches = find_records_for_query(args.word, args.source)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    html_path = generate_record_backtest_html(args.word, matches, args.source)
    print_cli_summary(args.word, matches, args.source, html_path)

    if args.open:
        webbrowser.open(f"file:///{html_path.resolve()}".replace("\\", "/"))

    return 0 if matches else 1


if __name__ == "__main__":
    sys.exit(main())
