"""Contract and mappings for the CEFR-based Vocabulary Difficulty Classification stage."""

from __future__ import annotations

from typing import Any, Final

STAGE_NAME: Final[str] = "DIFFICULTY"
STAGE_IMPLEMENTED: Final[bool] = True

ALLOWED_DIFFICULTY_LABELS: Final[tuple[str, str, str]] = ("Easy", "Medium", "Hard")

CEFR_TO_DIFFICULTY: Final[dict[str, str]] = {
    "A1": "Easy",
    "A2": "Easy",
    "B1": "Easy",
    "B2": "Medium",
    "C1": "Hard",
    "C2": "Hard",
}

# Preset contract: schema default is null; explicit assignment for currently existing records is "Basics"
PRESET_SCHEMA_DEFAULT: Final[str | None] = None
CURRENT_DATASET_PRESET: Final[str] = "Basics"

EXPECTED_INPUT_PATH: Final[str] = "data/enriched/justprepy_wordlist/entries.enriched.json"
EXPECTED_OUTPUT_PATH: Final[str] = "data/difficulty/justprepy_wordlist/entries.difficulty.json"
EXPECTED_VALIDATION_PATH: Final[str] = "data/difficulty/justprepy_wordlist/validation.json"


def cefr_to_difficulty(cefr_level: str | None) -> str | None:
    """Map a CEFR level (A1..C2) to platform difficulty ('Easy', 'Medium', 'Hard')."""
    if not cefr_level:
        return None
    normalized = cefr_level.strip().upper()
    return CEFR_TO_DIFFICULTY.get(normalized)


def assert_difficulty_unset(record: dict[str, Any]) -> None:
    """Verify that the reserved 'difficulty' field remains explicitly unset (None/null) in early stages."""
    if "difficulty" not in record:
        raise KeyError(f"Record {record.get('id')} is missing the 'difficulty' field.")
    if record["difficulty"] is not None:
        raise ValueError(
            f"Record {record.get('id')} has difficulty={record['difficulty']!r}, "
            "but early stages (RAW/CLEAN) must maintain difficulty as null."
        )


def assert_difficulty_valid(record: dict[str, Any]) -> None:
    """Verify that difficulty in post-classification stages is valid."""
    if "difficulty" not in record:
        raise KeyError(f"Record {record.get('id')} is missing the 'difficulty' field.")
    diff = record["difficulty"]
    if diff is not None and diff not in ALLOWED_DIFFICULTY_LABELS:
        raise ValueError(
            f"Record {record.get('id')} has invalid difficulty={diff!r}. "
            f"Must be one of {ALLOWED_DIFFICULTY_LABELS} or None."
        )
