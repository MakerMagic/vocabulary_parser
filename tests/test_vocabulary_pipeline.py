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
    CEFR_TO_DIFFICULTY,
    CURRENT_DATASET_PRESET,
    PRESET_SCHEMA_DEFAULT,
    assert_difficulty_unset,
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
        assert rec["difficulty"] in ALLOWED_DIFFICULTY_LABELS
        assert rec["preset"] == "Basics"
        assert rec["cefr_level"] in ("A1", "A2", "B1", "B2", "C1", "C2")
        if rec["validation_status"] == "validated":
            assert rec["final_output_eligible"] is True
        else:
            assert rec["final_output_eligible"] is False

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

    # 4. Invalid difficulty label must fail
    bad_diff = copy.deepcopy(prefinal_rec)
    bad_diff["difficulty"] = "InvalidTier"
    errs = validate_record_quality(bad_diff)
    assert any(e["code"] == "invalid_difficulty_classification" for e in errs)

    # 5. Early stages assert_difficulty_unset negative control
    with pytest.raises(ValueError, match="must maintain difficulty as null"):
        assert_difficulty_unset({"id": "test_rec", "difficulty": "Easy"})


def test_difficulty_stage_execution_and_contract() -> None:
    assert ALLOWED_DIFFICULTY_LABELS == ("Easy", "Medium", "Hard")
    assert CEFR_TO_DIFFICULTY["A1"] == "Easy"
    assert CEFR_TO_DIFFICULTY["A2"] == "Easy"
    assert CEFR_TO_DIFFICULTY["B1"] == "Easy"
    assert CEFR_TO_DIFFICULTY["B2"] == "Medium"
    assert CEFR_TO_DIFFICULTY["C1"] == "Hard"
    assert CEFR_TO_DIFFICULTY["C2"] == "Hard"

    # Schema default contract
    assert PRESET_SCHEMA_DEFAULT is None
    assert CURRENT_DATASET_PRESET == "Basics"

    # Verify UCL difficulty artifact
    ucl_diff = _load_json("data/difficulty/sources/uclouvain/entries.difficulty.json")
    assert ucl_diff["record_count"] == 413
    assert ucl_diff["summary"]["preset_assigned_count"] == 413
    assert ucl_diff["summary"]["eligible_for_final_output_count"] == 379
    assert ucl_diff["summary"]["blocked_from_final_output_count"] == 34
    assert ucl_diff["summary"]["difficulty_counts"] == {"Easy": 220, "Medium": 175, "Hard": 18, "Unset": 0}

    # Verify NW difficulty artifact
    nw_diff = _load_json("data/difficulty/sources/new_words/entries.difficulty.json")
    assert nw_diff["record_count"] == 159
    assert nw_diff["summary"]["preset_assigned_count"] == 159
    assert nw_diff["summary"]["eligible_for_final_output_count"] == 154
    assert nw_diff["summary"]["blocked_from_final_output_count"] == 5
    assert nw_diff["summary"]["difficulty_counts"] == {"Easy": 31, "Medium": 60, "Hard": 68, "Unset": 0}


def test_stage_qa_artifact_pairs_exist() -> None:
    stages = ["ACQUISITION", "INSPECTION", "RAW", "CLEAN", "ENRICHMENT", "DIFFICULTY", "VALIDATION"]
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


def test_new_words_pipeline_execution_and_contract() -> None:
    nw_doc = _load_json("data/pre_final/sources/new_words/vocabulary.json")
    assert nw_doc["record_count"] == 159
    assert nw_doc["summary"]["total_records"] == 159
    assert nw_doc["summary"]["validated_count"] == 154
    assert nw_doc["summary"]["review_pending_count"] == 2
    assert nw_doc["summary"]["excluded_count"] == 3
    assert nw_doc["summary"]["error_count"] == 0

    records = nw_doc["records"]
    assert len(records) == 159

    for r in records:
        assert isinstance(r["word"], str) and r["word"].strip()
        assert 1 <= len(r["russian_alternatives"]) <= 2
        assert len(r["english_explanation"].strip()) >= 15
        assert r["difficulty"] in ALLOWED_DIFFICULTY_LABELS
        assert r["preset"] == "Basics"
        assert r["cefr_level"] in ("A1", "A2", "B1", "B2", "C1", "C2")
        assert "type" in r
        if r["validation_status"] == "validated":
            assert r["final_output_eligible"] is True
        else:
            assert r["final_output_eligible"] is False

    # Excluded records check
    excluded_words = {r["word"] for r in records if r["validation_status"] == "excluded"}
    assert excluded_words == {"Repair", "Nearly", "Several"}

    # Review pending records check
    review_words = {r["word"] for r in records if r["validation_status"] == "review_pending"}
    assert review_words == {"Necessitates", "Opulent"}


def test_new_words_backtesting_tool_and_type_metadata() -> None:
    from tools.vocabulary_review import find_records_for_query

    # 1. Multiword expression 'Give rise to'
    gr_records = find_records_for_query("Give rise to", "new_words")
    assert len(gr_records) == 1
    assert gr_records[0]["word"] == "Give rise to"
    assert gr_records[0]["part_of_speech"] == "verb phrase"

    # 2. Excluded word 'Repair'
    rep_records = find_records_for_query("Repair", "new_words")
    assert len(rep_records) == 1
    assert rep_records[0]["validation_status"] == "excluded"
    assert rep_records[0]["cefr_level"] == "A2"

    # 3. Duplicate word 'negligible' across clusters
    neg_records = find_records_for_query("negligible", "new_words")
    assert len(neg_records) == 2
    clusters = {r["cluster_number"] for r in neg_records}
    assert clusters == {28, 36}

    # 4. Type field verification (schema extensibility)
    assert all("type" in r for r in gr_records)
    assert gr_records[0]["type"] is None or gr_records[0]["type"] == "Essential"


def test_nature_pipeline_execution_and_invariants() -> None:
    """Verify end-to-end invariants for the Nature dataset."""
    pf_doc = _load_json("data/pre_final/sources/nature/vocabulary.json")
    assert pf_doc["record_count"] == 169
    assert pf_doc["source_id"] == "nature"
    assert pf_doc["preset"] == "nature"

    records = pf_doc["records"]
    assert len(records) == 169

    # 1. 100% preset: 'nature'
    for r in records:
        assert r["preset"] == "nature", f"Record {r['word']} has invalid preset {r['preset']}"
        assert r["difficulty"] in ("Easy", "Medium", "Hard")
        assert len(r["russian_alternatives"]) in (1, 2)
        assert len(r["english_explanation"]) >= 15

    # 2. Eligibility partitioning: 142 eligible, 27 excluded
    eligible = [r for r in records if r["final_output_eligible"]]
    excluded = [r for r in records if not r["final_output_eligible"]]
    assert len(eligible) == 142
    assert len(excluded) == 27

    # 3. 12 explicitly restored A2 words verified eligible, Easy, and present
    restored_set = {
        "Wind", "Oil", "Lake", "Salt", "Whales", "Stomach",
        "Seed", "Bone", "Farming", "Roots", "Flies", "Bugs",
    }
    eligible_words = {r["word"] for r in eligible}
    assert restored_set.issubset(eligible_words), f"Missing restored words: {restored_set - eligible_words}"

    for r in eligible:
        if r["word"] in restored_set:
            assert r["difficulty"] == "Easy"
            assert r["cefr_level"] == "A2"
            assert r["preset"] == "nature"

    # 4. Whales translation rule: exactly one Russian translation ('киты')
    whales_rec = next(r for r in records if r["word"] == "Whales")
    assert whales_rec["russian_translation"] == "киты"
    assert whales_rec["russian_alternatives"] == ["киты"]

    # 5. Difficulty distribution (Easy: 82, Medium: 75, Hard: 12)
    from collections import Counter
    diff_counts = Counter(r["difficulty"] for r in records)
    assert diff_counts["Easy"] == 82
    assert diff_counts["Medium"] == 75
    assert diff_counts["Hard"] == 12

    # 6. Excluded words check (remaining elementary A1/A2 words)
    excluded_words = {r["word"] for r in excluded}
    assert "Food" in excluded_words
    assert "Sun" in excluded_words
    assert "Earth" in excluded_words
    assert "Natural" in excluded_words
    assert not any(w in excluded_words for w in restored_set)


def test_nature_backtesting_tool() -> None:
    from tools.vocabulary_review import find_records_for_query

    # 1. Eligible restored term 'Whales' with single translation
    whales_records = find_records_for_query("Whales", "nature")
    assert len(whales_records) == 1
    assert whales_records[0]["word"] == "Whales"
    assert whales_records[0]["preset"] == "nature"
    assert whales_records[0]["difficulty"] == "Easy"
    assert whales_records[0]["cefr_level"] == "A2"
    assert whales_records[0]["final_output_eligible"] is True
    assert whales_records[0]["russian_translation"] == "киты"

    # 2. Eligible term 'Ecosystem'
    eco_records = find_records_for_query("Ecosystem", "nature")
    assert len(eco_records) == 1
    assert eco_records[0]["word"] == "Ecosystem"
    assert eco_records[0]["preset"] == "nature"
    assert eco_records[0]["difficulty"] == "Medium"
    assert eco_records[0]["final_output_eligible"] is True

    # 3. Excluded term 'Food'
    food_records = find_records_for_query("Food", "nature")
    assert len(food_records) == 1
    assert food_records[0]["preset"] == "nature"
    assert food_records[0]["difficulty"] == "Easy"
    assert food_records[0]["cefr_level"] == "A1"
    assert food_records[0]["final_output_eligible"] is False

    # 4. Hard term 'Photosynthesis'
    photo_records = find_records_for_query("Photosynthesis", "nature")
    assert len(photo_records) == 1
    assert photo_records[0]["difficulty"] == "Hard"
    assert photo_records[0]["cefr_level"] == "C1"
    assert photo_records[0]["final_output_eligible"] is True


def test_rendering_eligibility_and_negative_controls() -> None:
    """Verify ZERO UNRESOLVED ISSUES admission gate and negative controls for Vocabulary Rendering."""
    from processors.rendering.contract import evaluate_rendering_eligibility

    valid_record = {
        "word": "abundant",
        "part_of_speech": "adjective",
        "russian_translation": "обильный",
        "russian_alternatives": ["обильный"],
        "english_explanation": "Existing or available in large quantities; more than enough.",
        "difficulty": "Medium",
        "preset": "Basics",
        "validation_status": "validated",
        "final_output_eligible": True,
        "validation_errors": [],
        "quality_and_review_notes": None,
    }

    # 1. Positive admission
    ok, reason = evaluate_rendering_eligibility(valid_record)
    assert ok is True
    assert reason is None

    # 2. Negative Control: review_pending
    rec_pending = copy.deepcopy(valid_record)
    rec_pending["validation_status"] = "review_pending"
    rec_pending["quality_and_review_notes"] = "Needs curriculum review"
    ok, reason = evaluate_rendering_eligibility(rec_pending)
    assert ok is False
    assert "Pending Review" in reason

    # 3. Negative Control: excluded
    rec_excluded = copy.deepcopy(valid_record)
    rec_excluded["validation_status"] = "excluded"
    rec_excluded["exclusion_reason"] = "elementary_a1_a2"
    ok, reason = evaluate_rendering_eligibility(rec_excluded)
    assert ok is False
    assert "policy-excluded" in reason

    # 4. Negative Control: validation error present
    rec_err = copy.deepcopy(valid_record)
    rec_err["validation_errors"] = [{"field": "word", "message": "Corrupted token"}]
    ok, reason = evaluate_rendering_eligibility(rec_err)
    assert ok is False
    assert "active validation errors" in reason

    # 5. Negative Control: final_output_eligible is False
    rec_not_final = copy.deepcopy(valid_record)
    rec_not_final["final_output_eligible"] = False
    ok, reason = evaluate_rendering_eligibility(rec_not_final)
    assert ok is False
    assert "final_output_eligible=False" in reason

    # 6. Negative Control: invalid difficulty
    rec_bad_diff = copy.deepcopy(valid_record)
    rec_bad_diff["difficulty"] = "SuperHard"
    ok, reason = evaluate_rendering_eligibility(rec_bad_diff)
    assert ok is False
    assert "Invalid or unset difficulty" in reason


def test_rendering_audit_across_all_datasets() -> None:
    """Verify read-only systematic rendering audit across all 741 records in repository."""
    from processors.rendering import audit_and_render_all

    res = audit_and_render_all(REPO_ROOT)
    assert res["total_repository_records"] == 741
    assert res["total_rendering_eligible"] == 675
    assert res["total_rendering_blocked"] == 66
    assert res["zero_unresolved_issues_gate_passed"] is True

    sources = res["source_breakdown"]
    assert set(sources.keys()) == {"nature", "new_words", "uclouvain"}

    # UCLouvain (413 total: 379 eligible, 34 blocked)
    ucl = sources["uclouvain"]
    assert ucl["total_records"] == 413
    assert ucl["admitted_eligible_count"] == 379
    assert ucl["blocked_ineligible_count"] == 34
    assert ucl["blocked_categories"]["policy_exclusion_a1_a2"] == 29
    assert ucl["blocked_categories"]["review_pending"] == 5
    assert ucl["blocked_categories"]["validation_errors"] == 0

    # New Words (159 total: 154 eligible, 5 blocked)
    nw = sources["new_words"]
    assert nw["total_records"] == 159
    assert nw["admitted_eligible_count"] == 154
    assert nw["blocked_ineligible_count"] == 5
    assert nw["blocked_categories"]["policy_exclusion_a1_a2"] == 3
    assert nw["blocked_categories"]["review_pending"] == 2
    assert nw["blocked_categories"]["validation_errors"] == 0

    # Nature (169 total: 142 eligible, 27 blocked)
    nat = sources["nature"]
    assert nat["total_records"] == 169
    assert nat["admitted_eligible_count"] == 142
    assert nat["blocked_ineligible_count"] == 27
    assert nat["blocked_categories"]["policy_exclusion_a1_a2"] == 27
    assert nat["blocked_categories"]["review_pending"] == 0
    assert nat["blocked_categories"]["validation_errors"] == 0


def test_rendering_card_and_diagnostic_html_templates() -> None:
    """Verify HTML template faithfully produces Area A (Website Card / Diagnostic) and Area B (Metadata)."""
    from processors.rendering import render_record

    # 1. Eligible record -> Area A website flashcard
    eligible_record = {
        "id": "test_001",
        "number": 1,
        "word": "lush",
        "part_of_speech": "adjective",
        "russian_translation": "пышный; буйный",
        "russian_alternatives": ["пышный", "буйный"],
        "english_explanation": "Growing thickly and strongly in a healthy way.",
        "difficulty": "Medium",
        "preset": "Basics",
        "validation_status": "validated",
        "final_output_eligible": True,
    }
    html_ok, is_elig, reason = render_record(eligible_record)
    assert is_elig is True
    assert reason is None
    assert "Area A &mdash; Website Display Preview (Flashcard)" in html_ok
    assert '<div class="website-card">' in html_ok
    assert '<span class="website-card__word">lush</span>' in html_ok
    assert '<span class="website-card__pos">adjective</span>' in html_ok
    assert "пышный, буйный" in html_ok
    assert "Growing thickly and strongly in a healthy way." in html_ok
    assert "Area B &mdash; Technical Quality Assurance &amp; Upstream Audit" in html_ok
    assert "ELIGIBLE FOR WEBSITE" in html_ok

    # 2. Ineligible record -> Area A diagnostic block
    blocked_record = {
        "id": "test_002",
        "number": 2,
        "word": "sun",
        "part_of_speech": "noun",
        "russian_translation": "солнце",
        "russian_alternatives": ["солнце"],
        "english_explanation": "The star around which the earth orbits.",
        "difficulty": "Easy",
        "preset": "nature",
        "validation_status": "excluded",
        "exclusion_reason": "elementary_a1_a2",
        "final_output_eligible": False,
    }
    html_blocked, is_elig_bl, reason_bl = render_record(blocked_record)
    assert is_elig_bl is False
    assert "policy-excluded" in reason_bl
    assert "NOT ELIGIBLE FOR WEBSITE DISPLAY" in html_blocked
    assert '<div class="ineligible-card">' in html_blocked
    assert '<div class="ineligible-reason-box">' in html_blocked
    assert "Area B &mdash; Technical Quality Assurance &amp; Upstream Audit" in html_blocked
    assert "BLOCKED (EXCLUDED)" in html_blocked



