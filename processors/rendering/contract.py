"""Contract and admission invariants for the Vocabulary Rendering Stage."""

from __future__ import annotations

from typing import Any

STAGE_NAME = "Vocabulary Rendering"
STAGE_VERSION = "1.0.0"

ALLOWED_DIFFICULTY_LABELS = ("Easy", "Medium", "Hard")


def evaluate_rendering_eligibility(record: dict[str, Any]) -> tuple[bool, str | None]:
    """Evaluate whether a vocabulary record satisfies the ZERO UNRESOLVED ISSUES admission rule.

    Returns (is_eligible, rejection_reason).
    """
    word = record.get("word", "")
    val_status = record.get("validation_status") or record.get("status")
    final_eligible = record.get("final_output_eligible")
    review_note = record.get("quality_and_review_notes") or record.get("enrichment_provenance", {}).get("review_note")
    val_errors = record.get("validation_errors") or []
    exclusion_reason = record.get("exclusion_reason")

    # 1. Verification of upstream validation status
    if val_status != "validated":
        if val_status == "excluded" or exclusion_reason is not None:
            return False, f"Record is policy-excluded ({exclusion_reason or 'elementary CEFR exclusion'})."
        if val_status == "review_pending" or review_note is not None:
            return False, f"Record has Pending Review status ({review_note or 'curriculum note unresolved'})."
        if val_status == "error":
            return False, "Record has outstanding validation errors."
        return False, f"Unverified validation status: {val_status!r}."

    # 2. Strict final output eligibility check
    if not final_eligible:
        return False, "Record flagged final_output_eligible=False."

    # 3. Check for any unresolved errors
    if val_errors:
        err_msg = "; ".join(e.get("message", str(e)) for e in val_errors)
        return False, f"Record carries active validation errors: {err_msg}."

    # 4. Check for review notes
    if review_note:
        return False, f"Record has unresolved review note: {review_note}."

    # 5. Check required content fields
    if not word or not isinstance(word, str) or not word.strip():
        return False, "Missing or empty English headword."

    pos = record.get("part_of_speech")
    if not pos or not isinstance(pos, str) or not pos.strip():
        return False, "Missing or empty part of speech."

    ru = record.get("russian_translation")
    alts = record.get("russian_alternatives") or []
    if not ru and not alts:
        return False, "Missing Russian translation."

    en = record.get("english_explanation")
    if not en or not isinstance(en, str) or len(en.strip()) < 15:
        return False, "Missing or insufficient English explanation (<15 chars)."

    diff = record.get("difficulty")
    if diff not in ALLOWED_DIFFICULTY_LABELS:
        return False, f"Invalid or unset difficulty level: {diff!r}."

    preset = record.get("preset")
    if not preset or not isinstance(preset, str) or not preset.strip():
        return False, "Missing or unset preset classification."

    return True, None
