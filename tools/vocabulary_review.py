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
            from processors.difficulty.contract import cefr_to_difficulty

            matches.append({
                "cefr_level": ex_info["level"],
                "declared_section_pos": pos_label,
                "difficulty": cefr_to_difficulty(ex_info["level"]),
                "english_explanation": en_expl,
                "exclusion_reason": "elementary_a1_a2",
                "final_output_eligible": False,
                "headword_lemma": q_norm,
                "id": f"benchmark_{q_norm}",
                "is_cross_section_homograph": False,
                "linguistic_evidence": ex_info["reason"],
                "number": 0,
                "parenthetical_modifier": None,
                "part_of_speech": pos_label,
                "preset": "Basics",
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
        iss_path = repo_root / f"qa/sources/{source_id}/{stage_name}_ISSUES.md"
        if not iss_path.exists():
            iss_path = repo_root / "qa" / f"{stage_name}_ISSUES.md"
        if iss_path.exists():
            text = iss_path.read_text(encoding="utf-8")
            # Look for record references like `#<num>` or `_vocab_<num>`
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
    """Generate a dedicated self-contained HTML backtesting report with Area A website preview and Area B metadata."""
    out_dir = repo_root / "inspections" / "review"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(query)
    out_file = out_dir / f"backtest_{source_id}_{slug}.html"

    from processors.rendering import evaluate_rendering_eligibility, render_backtest_page_html

    records_data: list[tuple[dict[str, Any], bool, str | None, dict[str, Any] | None]] = []
    for pf_rec in matches:
        num = pf_rec.get("number", 0)
        stages = load_stage_data_for_record(num, source_id, repo_root)
        is_eligible, reason = evaluate_rendering_eligibility(pf_rec)
        records_data.append((pf_rec, is_eligible, reason, stages))

    html_content = render_backtest_page_html(query, records_data, source_id)
    out_file.write_text(html_content, encoding="utf-8")
    return out_file


def print_cli_summary(query: str, matches: list[dict[str, Any]], source_id: str, html_path: Path) -> None:
    """Print clean terminal summary for PowerShell / CLI users."""
    from processors.rendering import evaluate_rendering_eligibility

    print("=" * 78)
    print(f"VOCABULARY PIPELINE & RENDERING BACKTEST: '{query}' (Source: {source_id})")
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
        rec_type = rec.get("type") or "null (Standard Vocabulary)"
        rec_preset = rec.get("preset", "Basics")
        rec_diff = rec.get("difficulty") or "Unset"
        rec_cefr = rec.get("cefr_level") or "N/A"
        is_elig, reason = evaluate_rendering_eligibility(rec)
        elig_str = "ELIGIBLE" if is_elig else f"BLOCKED ({status})"
        render_str = "ADMITTED (Website flashcard ready)" if is_elig else f"BLOCKED ({reason})"

        print(f"\n[#{num}] {w} ({rid}) — STATUS: {status}")
        print(f"  • Preset:       {rec_preset}")
        print(f"  • Difficulty:   {rec_diff} (CEFR: {rec_cefr})")
        print(f"  • Final Output: {elig_str}")
        print(f"  • Rendering:    {render_str}")
        print(f"  • Type:         {rec_type}")
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
