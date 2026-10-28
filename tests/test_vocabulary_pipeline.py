"""Automated verification and backtesting suite for the justprepy Vocabulary Parsing Pipeline.

Follows testing-validation-expectations:
- Source-span reconstruction (exact character and line slices)
- Adjacent-entry (N-1 / N+1) non-contamination
- Non-whitespace token ledger conservation (RAW -> CLEAN)
- Field quality validation (<=2-word Cyrillic Russian translation, non-circular English explanation)
- Negative controls proving validators fail on synthetic defects
- Architectural contract verification for the unimplemented Difficulty stage (Easy/Medium/Hard)
- Stage QA artifact pair existence (<STAGE>_BACKTESTING.md and <STAGE>_ISSUES.md)
- Local HTML backtesting review interface verification
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from processors.difficulty.contract import (
    ALLOWED_DIFFICULTY_LABELS,
    assert_difficulty_unset,
    run_difficulty_classification,
)
from processors.normalization.cleaner import verify_token_ledger
from processors.provenance import sha256_file
from processors.validation.validator import (
    parse_russian_translation_alternatives,
    validate_record_quality,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = REPO_ROOT / "acquisition" / "local" / "justprepy_vocabulary_list.txt"


def _load_json(rel_path: str) -> dict:
    path = REPO_ROOT / rel_path
    assert path.exists(), f"Expected artifact missing: {rel_path}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_stage1_acquisition_manifest_and_hash() -> None:
    manifest = _load_json("acquisition/manifest.json")
    assert len(manifest["sources"]) >= 1
    src = manifest["sources"][0]
    assert src["document_id"] == "justprepy_vocabulary_list_v1"
    actual_sha = sha256_file(SOURCE_PATH)
    assert src["sha256"] == actual_sha
    assert src["size_bytes"] > 0


def test_stage2_inspection_profile_counts_and_anomalies() -> None:
    profile = _load_json("data/inspection/profile.json")
    assert profile["total_extracted_items"] == 413
    assert profile["total_declared_items"] == 413
    assert len(profile["sections"]) == 2
    assert profile["sections"][0]["declared_count"] == 233
    assert profile["sections"][0]["actual_count"] == 233
    assert profile["sections"][1]["declared_count"] == 180
    assert profile["sections"][1]["actual_count"] == 180

    anomalies = profile["anomalies_and_characteristics"]
    homographs = set(anomalies["cross_section_homographs"].keys())
    assert homographs == {"present", "separate"}
    assert anomalies["parenthetical_tokens"] == ["account (for)"]
    assert anomalies["hyphenated_tokens"] == ["so-called"]
    assert sorted(anomalies["modal_auxiliaries"]) == ["can", "may", "should"]


def test_stage3_raw_source_span_reconstruction_and_neighbor_boundaries() -> None:
    raw_payload = _load_json("data/raw/justprepy_wordlist/entries.raw.json")
    records = raw_payload["records"]
    assert len(records) == 413

    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    source_lines = source_text.splitlines()
    expected_sha = sha256_file(SOURCE_PATH)
    assert raw_payload["source_sha256"] == expected_sha

    for idx, rec in enumerate(records):
        assert rec["number"] == idx + 1
        assert rec["source_sha256"] == expected_sha
        spans = rec["source_spans"]
        char_slice = source_text[spans["file_char_start"] : spans["file_char_end"]]
        line_slice = source_lines[spans["line_number"] - 1][spans["line_char_start"] : spans["line_char_end"]]
        assert char_slice == rec["raw_text"]
        assert line_slice == rec["raw_text"]

        # Neighbor boundary check (N-1 / N+1)
        if idx > 0:
            prev_rec = records[idx - 1]
            prev_spans = prev_rec["source_spans"]
            assert spans["file_char_start"] > prev_spans["file_char_end"]
            if spans["line_number"] == prev_spans["line_number"]:
                assert spans["line_char_start"] > prev_spans["line_char_end"]


def test_stage4_clean_token_ledger_and_difficulty_placeholder() -> None:
    raw_records = _load_json("data/raw/justprepy_wordlist/entries.raw.json")["records"]
    clean_records = _load_json("data/clean/justprepy_wordlist/entries.clean.json")["records"]
    assert len(clean_records) == 413

    for raw_rec, clean_rec in zip(raw_records, clean_records, strict=True):
        assert clean_rec["id"] == raw_rec["id"]
        assert clean_rec["word"] == raw_rec["raw_text"]
        ledger_ok, raw_tokens, clean_tokens = verify_token_ledger(raw_rec["raw_text"], clean_rec["word"])
        assert ledger_ok, f"Token ledger mismatch: {raw_tokens} != {clean_tokens}"
        assert clean_rec["difficulty"] is None
        assert_difficulty_unset(clean_rec)


def test_stage5_and_6_enrichment_and_prefinal_contract() -> None:
    prefinal = _load_json("data/pre_final/vocabulary.json")
    assert prefinal["record_count"] == 413
    assert prefinal["summary"]["total_records"] == 413
    assert prefinal["summary"]["validated_count"] == 379
    assert prefinal["summary"]["excluded_count"] == 29
    assert prefinal["summary"]["review_pending_count"] == 5
    assert prefinal["summary"]["error_count"] == 0
    assert prefinal["summary"]["eligible_records"] == 384

    records = prefinal["records"]
    assert len(records) == 413

    seen_numbers = set()
    for rec in records:
        seen_numbers.add(rec["number"])
        assert isinstance(rec["word"], str) and rec["word"].strip()
        assert rec["part_of_speech"] in {"verb", "verb (modal)", "verb (phrasal)", "adjective"}
        alts = parse_russian_translation_alternatives(rec["russian_translation"])
        assert 1 <= len(alts) <= 2
        assert len(rec["english_explanation"].strip()) >= 15
        assert rec["difficulty"] is None

        errs = validate_record_quality(rec)
        assert errs == [], f"Unexpected quality errors on #{rec['number']} {rec['word']}: {errs}"

    assert seen_numbers == set(range(1, 414))


def test_negative_controls_detect_synthetic_defects() -> None:
    prefinal_rec = _load_json("data/pre_final/vocabulary.json")["records"][0]

    # 1. Russian translation > 2 alternatives must fail
    bad_ru_alts = copy.deepcopy(prefinal_rec)
    bad_ru_alts["russian_translation"] = "взлетать; снимать одежду; отправляться"
    errs = validate_record_quality(bad_ru_alts)
    assert any(e["code"] == "russian_translation_exceeds_two_alternatives" for e in errs)

    # 1b. Multi-word Russian translation alternatives (up to 2 alternatives) must PASS
    multiword_rec = copy.deepcopy(prefinal_rec)
    multiword_rec["russian_translation"] = "взлетать; снимать одежду"
    assert validate_record_quality(multiword_rec) == []

    multiword_phrase = copy.deepcopy(prefinal_rec)
    multiword_phrase["russian_translation"] = "в отличие от"
    assert validate_record_quality(multiword_phrase) == []

    # 2. Non-Cyrillic Russian translation must fail
    bad_ru_script = copy.deepcopy(prefinal_rec)
    bad_ru_script["russian_translation"] = "abandon"
    errs = validate_record_quality(bad_ru_script)
    assert any(e["code"] == "russian_translation_not_cyrillic" for e in errs)

    # 3. Circular English explanation must fail
    bad_circular = copy.deepcopy(prefinal_rec)
    bad_circular["english_explanation"] = f"To {prefinal_rec['headword_lemma']} something completely and permanently."
    errs = validate_record_quality(bad_circular)
    assert any(e["code"] == "circular_english_explanation" for e in errs)

    # 4. Prematurely populated difficulty must fail
    bad_diff = copy.deepcopy(prefinal_rec)
    bad_diff["difficulty"] = "Easy"
    errs = validate_record_quality(bad_diff)
    assert any(e["code"] == "difficulty_prematurely_populated_or_missing" for e in errs)


def test_future_difficulty_stage_contract_raises_not_implemented() -> None:
    assert ALLOWED_DIFFICULTY_LABELS == ("Easy", "Medium", "Hard")
    with pytest.raises(NotImplementedError, match="NOT implemented yet"):
        run_difficulty_classification([])


def test_stage_qa_artifact_pairs_exist() -> None:
    stages = ["ACQUISITION", "INSPECTION", "RAW", "CLEAN", "ENRICHMENT", "VALIDATION"]
    for stage in stages:
        bt = REPO_ROOT / "qa" / f"{stage}_BACKTESTING.md"
        iss = REPO_ROOT / "qa" / f"{stage}_ISSUES.md"
        assert bt.exists(), f"Missing backtesting artifact: {bt}"
        assert iss.exists(), f"Missing issues artifact: {iss}"
        bt_text = bt.read_text(encoding="utf-8")
        iss_text = iss.read_text(encoding="utf-8")
        assert "## 1. Stage Execution Summary" in bt_text
        assert ("## 1. Issue Summary by Error Category" in iss_text or "ISSUE SUMMARY" in iss_text or "## 1. Overview & Counts" in iss_text)


def test_vocabulary_review_tool_and_linguistic_rules() -> None:
    from tools.vocabulary_review import find_records_for_query

    # 1. 'different from' multiword resolution
    diff_records = find_records_for_query("different from", "uclouvain")
    assert len(diff_records) >= 1
    assert diff_records[0]["word"] == "different"
    assert diff_records[0]["russian_alternatives"] == ["отличающийся", "непохожий на"]

    # 2. 'account for' phrasal resolution
    acct_records = find_records_for_query("account for", "uclouvain")
    assert len(acct_records) == 1
    assert acct_records[0]["word"] == "account (for)"
    assert acct_records[0]["russian_alternatives"] == ["объяснять", "являться причиной"]

    # 3. 'constitute' multiword alternative
    const_records = find_records_for_query("constitute", "uclouvain")
    assert len(const_records) == 1
    assert const_records[0]["russian_alternatives"] == ["составлять часть чего-то"]

    # 4. 'particular / specific' slash resolution
    slash_records = find_records_for_query("particular / specific", "uclouvain")
    words = {r["word"] for r in slash_records}
    assert "particular" in words and "specific" in words

    # 5. 'sure' elementary A1/A2 exclusion resolution
    sure_records = find_records_for_query("sure", "uclouvain")
    assert len(sure_records) >= 1
    assert any(r["status"] == "excluded" and r["exclusion_reason"] == "elementary_a1_a2" for r in sure_records)


def test_html_backtesting_interface_exists_and_contains_all_records() -> None:
    html_path = REPO_ROOT / "inspections" / "review" / "vocabulary_review.html"
    assert html_path.exists()
    html_text = html_path.read_text(encoding="utf-8")
    assert "justprepy Vocabulary Parsing Pipeline — QA &amp; Backtesting Review Interface" in html_text
    assert 'data-status="validated"' in html_text
    assert 'data-status="review_pending"' in html_text
    assert html_text.count('data-status="') == 413
