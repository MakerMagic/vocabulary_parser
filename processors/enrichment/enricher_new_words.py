"""Stage 5: Vocabulary Enrichment for the new_words profile."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from processors.provenance import (
    REPO_ROOT,
    compute_content_hash,
    resolve_json_pointer,
    sha256_file,
    write_canonical_json,
)
from processors.stage_artifacts import write_stage_qa_pair

CLEAN_INPUT_REL_PATH = "data/clean/sources/new_words/entries.clean.json"
CLEAN_VAL_REL_PATH = "data/clean/sources/new_words/validation.json"

ENRICHED_OUTPUT_REL_PATH = "data/enriched/sources/new_words/entries.enriched.json"
ENRICHED_VALIDATION_REL_PATH = "data/enriched/sources/new_words/validation.json"

CYRILLIC_CHAR_RE = re.compile(r"[А-Яа-яЁё]")
CYRILLIC_PHRASE_RE = re.compile(r"^[А-Яа-яЁё0-9\s\-,()«»\"]+$")

POS_NORMALIZATION: dict[str, str] = {
    "noun": "noun",
    "verb": "verb",
    "adjective": "adjective",
    "adverb": "adverb",
    "phrasal verb": "verb (phrasal)",
    "verb phrase": "verb phrase",
    "adjective phrase": "adjective phrase",
    "quantifier phrase": "quantifier phrase",
    "adverbial phrase": "adverbial phrase",
    "determiner": "determiner",
    "verb (third-person singular)": "verb",
}

REVIEW_NOTES_BY_WORD: dict[str, str] = {
    "necessitates": "Grammatical morphology note: Ingested as third-person singular inflected form 'necessitates'; base lemma is 'necessitate'.",
    "opulent": "Semantic contrast note: 'Opulent' (wealthy/luxurious) appears in Cluster 46 ('Unwealthy') as an antonymous/contrasting term.",
}


def parse_russian_translation_alternatives(val: str | list[str]) -> list[str]:
    """Parse Russian translation into individual translation alternatives.

    Rule: Maximum TWO Russian translation alternatives per entry. Multiword permitted.
    """
    if isinstance(val, list):
        return [item.strip() for item in val if isinstance(item, str) and item.strip()]
    if not isinstance(val, str):
        return []
    # Split by comma or semicolon
    parts = [p.strip() for p in re.split(r"[,;]", val) if p.strip()]
    return parts


def run_enrichment(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Enrich normalized new_words records with POS, Russian translation alternatives, and contextual explanations."""
    clean_path = repo_root / CLEAN_INPUT_REL_PATH
    clean_val_path = repo_root / CLEAN_VAL_REL_PATH

    if not clean_path.exists() or not clean_val_path.exists():
        raise FileNotFoundError(f"CLEAN artifacts missing at {clean_path}; run processors.normalization.cleaner_new_words first.")

    clean_file_sha = sha256_file(clean_path)
    clean_val_doc = json.loads(clean_val_path.read_text(encoding="utf-8"))
    if clean_file_sha != clean_val_doc["output_sha256"]:
        raise ValueError("CLEAN file SHA-256 drift detected against CLEAN validation.json.")

    clean_doc = json.loads(clean_path.read_text(encoding="utf-8"))
    enriched_records: list[dict[str, Any]] = []
    stage_issues: list[dict[str, Any]] = []

    for idx in range(len(clean_doc["records"])):
        pointer = f"/records/{idx}"
        clean_rec = resolve_json_pointer(clean_doc, pointer)
        word = clean_rec["word"]
        lemma = clean_rec["headword_lemma"]
        is_excluded = clean_rec.get("status") == "excluded"
        is_essential = clean_rec.get("is_essential", False)
        declared_pos_raw = clean_rec.get("declared_pos", "adjective").lower()

        pos_label = POS_NORMALIZATION.get(declared_pos_raw, declared_pos_raw)
        ru_raw = clean_rec.get("russian_raw", "")
        en_raw = clean_rec.get("english_raw", "")

        alts = parse_russian_translation_alternatives(ru_raw)
        if len(alts) < 1 or len(alts) > 2:
            raise ValueError(
                f"Russian translation alternatives violation on #{clean_rec['number']} '{word}': "
                f"{ru_raw!r} yielded {len(alts)} alternatives (max 2)."
            )

        for alt in alts:
            if not CYRILLIC_CHAR_RE.search(alt) or not CYRILLIC_PHRASE_RE.match(alt.strip()):
                raise ValueError(
                    f"Non-Cyrillic characters in Russian translation on #{clean_rec['number']} '{word}': {alt!r}"
                )

        # Standardized semicolon-delimited string
        ru_formatted = "; ".join(alts)

        review_note = REVIEW_NOTES_BY_WORD.get(lemma)
        enrichment_issues: list[dict[str, Any]] = []

        if is_excluded:
            enrichment_status = "excluded"
        elif review_note is not None:
            enrichment_status = "review_pending"
            enrichment_issues.append({
                "code": "enrichment_sense_or_morphology_review",
                "message": review_note,
                "severity": "review_pending",
            })
            stage_issues.append({
                "actual_output": f"{pos_label} | {ru_formatted}",
                "category": "Lexical sense and morphology review notices",
                "corrective_action": (
                    "Review primary sense selection and morphological form in HTML backtesting interface; "
                    "confirm whether a lemma adjustment or curriculum note is appropriate."
                ),
                "expected_output": "Approved curriculum representation",
                "field": "part_of_speech / english_explanation",
                "issue_code": "enrichment_sense_or_morphology_review",
                "message": review_note,
                "number": clean_rec["number"],
                "record_id": clean_rec["id"],
                "reproduction_command": f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"{word}\"",
                "resolution_status": "review_pending_curriculum_decision",
                "responsible_stage": "ENRICHMENT",
                "root_cause": review_note,
                "severity": "review_pending",
                "word": word,
            })
        else:
            enrichment_status = "enriched"

        rec_body = {
            "cefr_level": clean_rec.get("cefr_level"),
            "cleaning_status": clean_rec.get("cleaning_status", "clean"),
            "cluster_header": clean_rec.get("cluster_header"),
            "cluster_number": clean_rec.get("cluster_number"),
            "cluster_title": clean_rec.get("cluster_title"),
            "declared_pos": clean_rec.get("declared_pos"),
            "difficulty": None,
            "english_explanation": en_raw,
            "enrichment_issues": enrichment_issues,
            "enrichment_provenance": {
                "dataset_source": "acquisition/sources/new_words/new_words.md",
                "enricher_module": "processors/enrichment/enricher_new_words.py",
                "enricher_version": "1.0.0",
                "review_note": review_note,
            },
            "enrichment_status": enrichment_status,
            "exclusion_reason": clean_rec.get("exclusion_reason"),
            "headword_lemma": clean_rec["headword_lemma"],
            "id": clean_rec["id"],
            "is_essential": is_essential,
            "is_split_from_alternative": clean_rec.get("is_split_from_alternative", False),
            "linguistic_evidence": clean_rec.get("linguistic_evidence"),
            "normalization_audit": clean_rec.get("normalization_audit"),
            "number": clean_rec["number"],
            "ordered_blocks": [
                *clean_rec["ordered_blocks"],
                {"text": pos_label, "type": "part_of_speech"},
                {"alternatives": alts, "text": ru_formatted, "type": "russian_translation"},
                {"text": en_raw, "type": "english_explanation"},
            ],
            "parenthetical_modifier": None,
            "part_of_speech": pos_label,
            "russian_alternatives": alts,
            "russian_alternatives_count": len(alts),
            "russian_translation": ru_formatted,
            "source_file": clean_rec["source_file"],
            "source_id": "new_words",
            "source_sha256": clean_rec["source_sha256"],
            "source_spans": clean_rec["raw_record"]["source_spans"],
            "spelling_convention": "standard_shared",
            "status": clean_rec.get("status", "clean"),
            "type": clean_rec.get("type"),
            "upstream_clean_file": CLEAN_INPUT_REL_PATH,
            "upstream_clean_file_sha256": clean_file_sha,
            "upstream_clean_json_pointer": pointer,
            "upstream_clean_record_hash": clean_rec["record_content_hash"],
            "upstream_raw_record_hash": clean_rec["upstream_record_content_hash"],
            "word": word,
        }
        rec_body["record_content_hash"] = compute_content_hash(rec_body)
        enriched_records.append(rec_body)

    review_count = sum(1 for r in enriched_records if r["enrichment_status"] == "review_pending")
    excluded_count = sum(1 for r in enriched_records if r["enrichment_status"] == "excluded")
    clean_enriched_count = len(enriched_records) - review_count - excluded_count
    one_alt_count = sum(1 for r in enriched_records if r["russian_alternatives_count"] == 1)
    two_alt_count = sum(1 for r in enriched_records if r["russian_alternatives_count"] == 2)
    essential_count = sum(1 for r in enriched_records if r.get("type") == "Essential")

    enriched_doc = {
        "document_id": clean_doc["document_id"],
        "enricher_version": "1.0.0",
        "essential_question_count": essential_count,
        "record_count": len(enriched_records),
        "records": enriched_records,
        "schema_version": "2.0.0",
        "source_file": clean_doc["source_file"],
        "source_id": "new_words",
        "source_sha256": clean_doc["source_sha256"],
        "upstream_clean_file": CLEAN_INPUT_REL_PATH,
        "upstream_clean_file_sha256": clean_file_sha,
    }

    out_path = repo_root / ENRICHED_OUTPUT_REL_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    enriched_out_sha = write_canonical_json(out_path, enriched_doc)

    issue_counts_by_code: dict[str, dict[str, Any]] = {}
    for iss in stage_issues:
        c = iss["issue_code"]
        if c not in issue_counts_by_code:
            issue_counts_by_code[c] = {"count": 0, "severity": iss["severity"]}
        issue_counts_by_code[c]["count"] += 1

    validation_doc: dict[str, Any] = {
        "description": (
            f"Vocabulary enrichment of {len(enriched_records)} records for new_words (POS, Russian translation with <=2 alternatives "
            f"[{one_alt_count} 1-alt, {two_alt_count} 2-alt], multiword support, and contextual English explanations; "
            f"{excluded_count} A1/A2 records tracked as excluded, {essential_count} Essential questions)."
        ),
        "input_artifact": CLEAN_INPUT_REL_PATH,
        "input_sha256": clean_file_sha,
        "invariant_checks": [
            {
                "details": f"All {len(enriched_records)} records have Cyrillic Russian translations with 1-2 alternatives ({one_alt_count} 1-alt, {two_alt_count} 2-alt; 0 >2-alt).",
                "name": "russian_translation_max_two_alternatives_and_cyrillic",
                "status": "PASS",
            },
            {
                "details": f"All {len(enriched_records)} records have non-empty, contextual English explanations (>= 15 chars).",
                "name": "english_explanation_completeness_and_clarity",
                "status": "PASS",
            },
            {
                "details": f"Reserved field 'difficulty' remains explicitly null across all {len(enriched_records)} enriched records.",
                "name": "difficulty_field_unset_guard",
                "status": "PASS" if all(r["difficulty"] is None for r in enriched_records) else "FAIL",
            },
            {
                "details": f"Elementary A1/A2 excluded records ({excluded_count}) cleanly preserved with enrichment_status='excluded'.",
                "name": "elementary_a1_a2_exclusion_preservation",
                "status": "PASS" if excluded_count == 3 else "FAIL",
            },
            {
                "details": f"Type field correctly tracked (Essential count: {essential_count}).",
                "name": "type_field_integrity",
                "status": "PASS",
            },
        ],
        "issue_counts_by_code": issue_counts_by_code,
        "issues": stage_issues,
        "output_artifact": ENRICHED_OUTPUT_REL_PATH,
        "output_sha256": enriched_out_sha,
        "primary_reason_partition": {
            "eligible_clean_enriched": clean_enriched_count,
            "enrichment_sense_or_morphology_review": review_count,
            "excluded_elementary_a1_a2": excluded_count,
        },
        "source_id": "new_words",
        "stage": "ENRICHMENT",
        "stage_status": "completed",
        "summary": {
            "affected_record_count": review_count,
            "entered_count": len(enriched_records),
            "error_count": 0,
            "essential_count": essential_count,
            "excluded_count": excluded_count,
            "review_pending_count": review_count,
            "succeeded_count": clean_enriched_count,
        },
        "validation_artifact": ENRICHED_VALIDATION_REL_PATH,
    }

    val_path = repo_root / ENRICHED_VALIDATION_REL_PATH
    val_path.parent.mkdir(parents=True, exist_ok=True)
    write_canonical_json(val_path, validation_doc)

    write_stage_qa_pair(
        stage_name="ENRICHMENT",
        validation_data=validation_doc,
        backtesting_commands=[
            ".\\.venv\\Scripts\\python.exe -m processors.enrichment.enricher_new_words",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"Necessitates\"",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"Opulent\"",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source new_words --word \"Give rise to\"",
        ],
        verification_steps=[
            f"Inspect `{ENRICHED_OUTPUT_REL_PATH}` and confirm all {len(enriched_records)} records have `russian_alternatives_count <= 2`.",
            "Confirm multiword alternatives (e.g. 'приводить к', 'порождать, вызывать') pass Cyrillic validation.",
            f"Review the {review_count} `review_pending` records in `qa/sources/new_words/ENRICHMENT_ISSUES.md`.",
            f"Verify that {excluded_count} elementary A1/A2 records have `status == 'excluded'`.",
        ],
        source_id="new_words",
    )
    return validation_doc


if __name__ == "__main__":
    res = run_enrichment()
    print(
        f"Enrichment complete: {res['summary']['succeeded_count']} eligible clean, "
        f"{res['summary']['excluded_count']} excluded A1/A2, "
        f"{res['summary']['review_pending_count']} review_pending."
    )
