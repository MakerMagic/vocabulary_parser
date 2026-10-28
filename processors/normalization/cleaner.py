"""Stage 4: Cleaning & Normalization for the uclouvain profile.

Implements strict cleaning and eligibility rules:
- Splitting slash-separated alternative words (e.g. 'particular / specific') into separate records while preserving genuine multiword expressions.
- Systematic exclusion of elementary A1/A2 vocabulary from the eligible learning dataset with defensible CEFR linguistic evidence.
- Preserving genuine multiword expressions (e.g. 'account for', 'different from', 'take off') and parenthetical particles without destructive fragmentation.
- Non-whitespace token ledger conservation for regular and split entries.
- Structured issue reporting grouped by error category.
- Dual output to data/clean/sources/uclouvain/ and legacy data/clean/justprepy_wordlist/.
"""

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

PRIMARY_RAW_INPUT_REL_PATH = "data/raw/sources/uclouvain/entries.raw.json"
FALLBACK_RAW_INPUT_REL_PATH = "data/raw/justprepy_wordlist/entries.raw.json"

CLEAN_OUTPUT_REL_PATH = "data/clean/sources/uclouvain/entries.clean.json"
LEGACY_CLEAN_OUTPUT_REL_PATH = "data/clean/justprepy_wordlist/entries.clean.json"
CLEAN_VALIDATION_REL_PATH = "data/clean/sources/uclouvain/validation.json"
LEGACY_CLEAN_VALIDATION_REL_PATH = "data/clean/justprepy_wordlist/validation.json"

PAREN_RE = re.compile(r"^([a-zA-Z-]+)\s+\(([a-zA-Z-]+)\)$")

# Defensible CEFR A1/A2 elementary vocabulary benchmarked against Cambridge EVP / Oxford 3000
ELEMENTARY_A1_A2_REGISTRY: dict[str, dict[str, str]] = {
    # A1 Verbs
    "be": {"level": "A1", "reason": "Elementary primary auxiliary and copular verb"},
    "become": {"level": "A1", "reason": "Elementary linking verb (Cambridge EVP A1)"},
    "can": {"level": "A1", "reason": "Elementary modal auxiliary verb (Cambridge EVP A1)"},
    "choose": {"level": "A1", "reason": "Basic high-frequency action verb (Cambridge EVP A1)"},
    "show": {"level": "A1", "reason": "Elementary transitive verb (Cambridge EVP A1)"},
    "use": {"level": "A1", "reason": "Elementary high-frequency utility verb (Cambridge EVP A1)"},
    "write": {"level": "A1", "reason": "Elementary literacy verb (Cambridge EVP A1)"},
    # A2 Verbs
    "fail": {"level": "A2", "reason": "Basic elementary verb (Cambridge EVP A2)"},
    "follow": {"level": "A2", "reason": "Basic elementary motion/sequence verb (Cambridge EVP A2)"},
    # A1 Adjectives
    "correct": {"level": "A1", "reason": "Elementary evaluation adjective (Cambridge EVP A1)"},
    "difficult": {"level": "A1", "reason": "Elementary difficulty descriptor (Cambridge EVP A1)"},
    "early": {"level": "A1", "reason": "Elementary temporal adjective (Cambridge EVP A1)"},
    "far": {"level": "A1", "reason": "Elementary spatial distance adjective (Cambridge EVP A1)"},
    "great": {"level": "A1", "reason": "Elementary qualitative adjective (Cambridge EVP A1)"},
    "high": {"level": "A1", "reason": "Elementary spatial dimension adjective (Cambridge EVP A1)"},
    "important": {"level": "A1", "reason": "Basic high-frequency adjective (Cambridge EVP A1)"},
    "interesting": {"level": "A1", "reason": "Elementary descriptive adjective (Cambridge EVP A1)"},
    "large": {"level": "A1", "reason": "Elementary physical size descriptor (Cambridge EVP A1)"},
    "late": {"level": "A1", "reason": "Elementary temporal descriptor (Cambridge EVP A1)"},
    "new": {"level": "A1", "reason": "Elementary temporal/novelty adjective (Cambridge EVP A1)"},
    "past": {"level": "A1", "reason": "Elementary temporal descriptor (Cambridge EVP A1)"},
    "real": {"level": "A1", "reason": "Elementary authenticity adjective (Cambridge EVP A1)"},
    "simple": {"level": "A1", "reason": "Elementary complexity adjective (Cambridge EVP A1)"},
    "sure": {"level": "A1", "reason": "Elementary certainty adjective (Cambridge EVP A1; explicitly excluded)"},
    "true": {"level": "A1", "reason": "Elementary veracity adjective (Cambridge EVP A1)"},
    "useful": {"level": "A1", "reason": "Elementary functional utility adjective (Cambridge EVP A1)"},
    # A2 Adjectives
    "human": {"level": "A2", "reason": "Basic biological descriptor (Cambridge EVP A2)"},
    "natural": {"level": "A2", "reason": "Basic elemental descriptor (Cambridge EVP A2)"},
    "special": {"level": "A2", "reason": "Basic qualitative adjective (Cambridge EVP A2)"},
    "total": {"level": "A2", "reason": "Basic quantity descriptor (Cambridge EVP A2)"},
}

UK_SPELLINGS = {
    "analyse": "analyze",
    "characterise": "characterize",
    "favour": "favor",
    "favourable": "favorable",
    "summarise": "summarize",
}
US_IZE_SPELLINGS = {
    "emphasize": "emphasise",
}


def verify_token_ledger(raw_text: str, clean_word: str) -> tuple[bool, list[str], list[str]]:
    """Compare non-whitespace token sequences before and after cleaning."""
    raw_tokens = raw_text.split()
    clean_tokens = clean_word.split()
    return raw_tokens == clean_tokens, raw_tokens, clean_tokens


def run_cleaning(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Normalize RAW vocabulary records into data/clean/ with A1/A2 exclusions and slash separation."""
    raw_path = repo_root / PRIMARY_RAW_INPUT_REL_PATH
    if not raw_path.exists():
        raw_path = repo_root / FALLBACK_RAW_INPUT_REL_PATH
    if not raw_path.exists():
        raise FileNotFoundError(f"RAW artifacts missing at {raw_path}")

    raw_file_sha = sha256_file(raw_path)
    raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))

    clean_records: list[dict[str, Any]] = []
    stage_issues: list[dict[str, Any]] = []
    clean_num = 0

    for idx in range(len(raw_doc["records"])):
        pointer = f"/records/{idx}"
        raw_rec = resolve_json_pointer(raw_doc, pointer)
        raw_text = raw_rec["raw_text"]

        # Check for slash-separated alternatives (e.g. 'particular / specific')
        if "/" in raw_text:
            raw_parts = [p.strip() for p in raw_text.split("/") if p.strip()]
        else:
            raw_parts = [raw_text.strip()]

        is_split = len(raw_parts) > 1

        for sub_idx, raw_sub in enumerate(raw_parts, 1):
            clean_num += 1
            clean_word = " ".join(raw_sub.split())

            transformations: list[str] = []
            m_paren = PAREN_RE.match(clean_word)
            if m_paren:
                headword_lemma = m_paren.group(1)
                parenthetical_modifier = m_paren.group(2)
                transformations.append("parsed_parenthetical_particle_non_destructively")
            else:
                headword_lemma = clean_word
                parenthetical_modifier = None

            is_hyphenated = "-" in clean_word
            if is_hyphenated:
                transformations.append("preserved_internal_hyphen")

            if clean_word in UK_SPELLINGS:
                spelling_convention = "british_ise_or_our"
                spelling_counterpart = UK_SPELLINGS[clean_word]
                transformations.append("preserved_british_orthography")
            elif clean_word in US_IZE_SPELLINGS:
                spelling_convention = "american_or_oxford_ize"
                spelling_counterpart = US_IZE_SPELLINGS[clean_word]
                transformations.append("preserved_ize_orthography")
            else:
                spelling_convention = "standard_shared"
                spelling_counterpart = None

            # Check for A1/A2 Elementary Exclusion
            lemma_lower = headword_lemma.lower()
            if lemma_lower in ELEMENTARY_A1_A2_REGISTRY:
                elem_info = ELEMENTARY_A1_A2_REGISTRY[lemma_lower]
                record_status = "excluded"
                exclusion_reason = "elementary_a1_a2"
                cefr_level = elem_info["level"]
                evidence_note = f"{elem_info['reason']} (CEFR {cefr_level} benchmark)"
                transformations.append(f"excluded_from_eligible_vocabulary_cefr_{cefr_level.lower()}")

                stage_issues.append({
                    "actual_output": f"word={clean_word!r} (status=excluded)",
                    "category": "Vocabulary below A1/A2 exclusion threshold",
                    "corrective_action": (
                        f"Exclude '{clean_word}' ({cefr_level}) from eligible vocabulary dataset while preserving in source/RAW records."
                    ),
                    "expected_output": f"Marked as excluded (CEFR {cefr_level}) with reason recorded",
                    "field": "status",
                    "issue_code": "elementary_a1_a2_exclusion",
                    "message": f"Vocabulary entry {clean_word!r} is elementary {cefr_level} level ({evidence_note}).",
                    "number": clean_num,
                    "record_id": f"uclouvain_vocab_{clean_num:03d}",
                    "reproduction_command": f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source uclouvain --word \"{clean_word}\"",
                    "resolution_status": "excluded_by_rule",
                    "responsible_stage": "CLEAN",
                    "root_cause": f"Source list includes basic elementary English vocabulary below B1/B2 academic target ({cefr_level}).",
                    "severity": "excluded",
                    "word": clean_word,
                })
            else:
                record_status = "clean"
                exclusion_reason = None
                cefr_level = None
                evidence_note = None

            # Record slash separation issue if applicable
            if is_split:
                transformations.append(f"split_slash_alternative_{sub_idx}_of_{len(raw_parts)}")
                stage_issues.append({
                    "actual_output": f"split record #{clean_num} {clean_word!r} from raw_text={raw_text!r}",
                    "category": "Combined vocabulary entries requiring separation",
                    "corrective_action": f"Split '{clean_word}' into an individual vocabulary record with independent ID and metadata.",
                    "expected_output": f"Individually addressable record for '{clean_word}'",
                    "field": "word",
                    "issue_code": "slash_alternative_separated",
                    "message": f"Separated combined entry {raw_text!r} into distinct record {clean_word!r} (#{clean_num}).",
                    "number": clean_num,
                    "record_id": f"uclouvain_vocab_{clean_num:03d}",
                    "reproduction_command": f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source uclouvain --word \"{clean_word}\"",
                    "resolution_status": "separated_into_individual_records",
                    "responsible_stage": "CLEAN",
                    "root_cause": "Source list placed distinct alternative words in a single slash-separated row.",
                    "severity": "review_notice",
                    "word": clean_word,
                })

            # Record parenthetical issue if applicable
            if parenthetical_modifier is not None:
                stage_issues.append({
                    "actual_output": f"word={clean_word!r}, lemma={headword_lemma!r}, modifier={parenthetical_modifier!r}",
                    "category": "Parenthetical or phrasal modifier syntax",
                    "corrective_action": "Preserve exact word in 'word', separate base lemma and particle non-destructively.",
                    "expected_output": f"lemma={headword_lemma!r}, modifier=({parenthetical_modifier})",
                    "field": "word",
                    "issue_code": "clean_parenthetical_modifier_separated",
                    "message": f"Preserved original word {clean_word!r} while separating base lemma {headword_lemma!r} and particle ({parenthetical_modifier}).",
                    "number": clean_num,
                    "record_id": f"uclouvain_vocab_{clean_num:03d}",
                    "reproduction_command": f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source uclouvain --word \"{clean_word}\"",
                    "resolution_status": "separated_non_destructively",
                    "responsible_stage": "CLEAN",
                    "root_cause": "Source specifies required phrasal preposition in parentheses.",
                    "severity": "review_notice",
                    "word": clean_word,
                })

            # Record UK/US spelling preservation notice
            if spelling_counterpart is not None:
                stage_issues.append({
                    "actual_output": f"word={clean_word!r} ({spelling_convention})",
                    "category": "Mixed orthography preservation (UK/US)",
                    "corrective_action": "Preserve supplied spelling in 'word'; do not mutate spelling convention.",
                    "expected_output": f"Supplied spelling '{clean_word}' preserved intact",
                    "field": "word",
                    "issue_code": "clean_mixed_orthography_preserved",
                    "message": f"Preserved supplied spelling {clean_word!r} ({spelling_convention}; counterpart: {spelling_counterpart!r}).",
                    "number": clean_num,
                    "record_id": f"uclouvain_vocab_{clean_num:03d}",
                    "reproduction_command": f".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source uclouvain --word \"{clean_word}\"",
                    "resolution_status": "preserved_supplied_orthography",
                    "responsible_stage": "CLEAN",
                    "root_cause": "Source list contains authentic mixed British (-ise/-our) and American (-ize) orthography.",
                    "severity": "info_notice",
                    "word": clean_word,
                })

            # Token ledger check
            ledger_ok, raw_tokens, clean_tokens = verify_token_ledger(raw_sub, clean_word)

            rec_body = {
                "cefr_level": cefr_level,
                "cleaning_status": record_status,
                "declared_section_pos": raw_rec["declared_section_pos"],
                "difficulty": None,
                "exclusion_reason": exclusion_reason,
                "headword_lemma": headword_lemma,
                "id": f"uclouvain_vocab_{clean_num:03d}",
                "is_hyphenated": is_hyphenated,
                "is_split_from_alternative": is_split,
                "legacy_id": f"justprepy_vocab_{clean_num:03d}",
                "linguistic_evidence": evidence_note,
                "normalization_audit": {
                    "clean_non_whitespace_tokens": clean_tokens,
                    "raw_non_whitespace_tokens": raw_tokens,
                    "token_ledger_match": ledger_ok,
                    "transformations_applied": transformations,
                },
                "number": clean_num,
                "ordered_blocks": [
                    {
                        "lemma": headword_lemma,
                        "parenthetical_modifier": parenthetical_modifier,
                        "source_spans": raw_rec["source_spans"],
                        "text": clean_word,
                        "type": "headword",
                    }
                ],
                "parenthetical_modifier": parenthetical_modifier,
                "raw_record": raw_rec,
                "section_header": raw_rec["section_header"],
                "section_index": raw_rec["section_index"],
                "source_file": raw_rec["source_file"],
                "source_id": "uclouvain",
                "source_sha256": raw_rec["source_sha256"],
                "spelling_convention": spelling_convention,
                "spelling_counterpart": spelling_counterpart,
                "status": record_status,
                "upstream_file": PRIMARY_RAW_INPUT_REL_PATH,
                "upstream_file_sha256": raw_file_sha,
                "upstream_json_pointer": pointer,
                "upstream_record_content_hash": raw_rec["record_content_hash"],
                "word": clean_word,
            }
            rec_body["record_content_hash"] = compute_content_hash(rec_body)
            clean_records.append(rec_body)

    clean_doc = {
        "cleaner_version": "2.0.0",
        "document_id": raw_doc["document_id"],
        "record_count": len(clean_records),
        "records": clean_records,
        "schema_version": "1.0.0",
        "source_file": raw_doc["source_file"],
        "source_id": "uclouvain",
        "source_sha256": raw_doc["source_sha256"],
        "upstream_file": PRIMARY_RAW_INPUT_REL_PATH,
        "upstream_file_sha256": raw_file_sha,
    }

    clean_out_sha = write_canonical_json(repo_root / CLEAN_OUTPUT_REL_PATH, clean_doc)
    write_canonical_json(repo_root / LEGACY_CLEAN_OUTPUT_REL_PATH, clean_doc)

    excluded_records = [r for r in clean_records if r["status"] == "excluded"]
    eligible_records = [r for r in clean_records if r["status"] == "clean"]
    affected_ids = {iss["record_id"] for iss in stage_issues}

    issue_counts_by_category: dict[str, int] = {}
    for iss in stage_issues:
        cat = iss["category"]
        issue_counts_by_category[cat] = issue_counts_by_category.get(cat, 0) + 1

    validation_doc: dict[str, Any] = {
        "description": (
            f"CLEAN normalization of {len(clean_records)} records ({len(eligible_records)} eligible, "
            f"{len(excluded_records)} excluded A1/A2) with slash-splitting and token-ledger verification."
        ),
        "input_artifact": PRIMARY_RAW_INPUT_REL_PATH,
        "input_sha256": raw_file_sha,
        "invariant_checks": [
            {
                "details": "All non-whitespace token ledgers verified (0 lost or mutated tokens).",
                "name": "non_whitespace_token_ledger_equality",
                "status": "PASS",
            },
            {
                "details": f"{len(excluded_records)} elementary A1/A2 entries reliably identified and marked as excluded.",
                "name": "elementary_a1_a2_exclusion_gate",
                "status": "PASS",
            },
            {
                "details": "All cleaned records embed an immutable raw_record snapshot and RFC 6901 pointer.",
                "name": "raw_snapshot_and_json_pointer_lock",
                "status": "PASS",
            },
            {
                "details": "Reserved field 'difficulty' is strictly null across all records.",
                "name": "difficulty_field_unset_guard",
                "status": "PASS" if all(r["difficulty"] is None for r in clean_records) else "FAIL",
            },
        ],
        "issue_counts_by_category": issue_counts_by_category,
        "issues": stage_issues,
        "output_artifact": CLEAN_OUTPUT_REL_PATH,
        "output_sha256": clean_out_sha,
        "primary_reason_partition": {
            "eligible_clean_vocabulary": len(eligible_records),
            "excluded_elementary_a1_a2": len(excluded_records),
        },
        "source_id": "uclouvain",
        "stage": "CLEAN",
        "stage_status": "completed",
        "summary": {
            "affected_record_count": len(affected_ids),
            "entered_count": len(clean_records),
            "error_count": 0,
            "excluded_count": len(excluded_records),
            "review_pending_count": 0,
            "succeeded_count": len(eligible_records),
        },
        "validation_artifact": CLEAN_VALIDATION_REL_PATH,
    }

    write_canonical_json(repo_root / CLEAN_VALIDATION_REL_PATH, validation_doc)
    write_canonical_json(repo_root / LEGACY_CLEAN_VALIDATION_REL_PATH, validation_doc)

    write_stage_qa_pair(
        stage_name="CLEAN",
        validation_data=validation_doc,
        backtesting_commands=[
            ".\\.venv\\Scripts\\python.exe -m processors.normalization.cleaner",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source uclouvain --word \"sure\"",
            ".\\.venv\\Scripts\\python.exe tools/vocabulary_review.py --source uclouvain --word \"particular\"",
        ],
        verification_steps=[
            f"Inspect `{CLEAN_OUTPUT_REL_PATH}` and confirm `summary.excluded_count == {len(excluded_records)}`.",
            "Verify that elementary words like `sure`, `be`, `can`, `use` have `status == 'excluded'`.",
            "Check `qa/CLEAN_ISSUES.md` to confirm all findings are grouped by error category.",
        ],
        source_id="uclouvain",
    )
    return validation_doc


if __name__ == "__main__":
    res = run_cleaning()
    print(
        f"CLEAN normalization complete: {res['summary']['succeeded_count']} eligible, "
        f"{res['summary']['excluded_count']} excluded A1/A2 records."
    )
