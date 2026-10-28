"""Architectural contract for the future Vocabulary Difficulty Classification stage.

DO NOT implement heuristic or automated difficulty classification here until authorized.
"""

from __future__ import annotations

from typing import Any, Final

STAGE_NAME: Final[str] = "DIFFICULTY"
STAGE_IMPLEMENTED: Final[bool] = False
ALLOWED_DIFFICULTY_LABELS: Final[tuple[str, str, str]] = ("Easy", "Medium", "Hard")

EXPECTED_INPUT_PATH: Final[str] = "data/enriched/justprepy_wordlist/entries.enriched.json"
EXPECTED_OUTPUT_PATH: Final[str] = "data/difficulty/justprepy_wordlist/entries.difficulty.json"
EXPECTED_VALIDATION_PATH: Final[str] = "data/difficulty/justprepy_wordlist/validation.json"


def assert_difficulty_unset(record: dict[str, Any]) -> None:
    """Verify that the reserved 'difficulty' field remains explicitly unset (None/null)."""
    if "difficulty" not in record:
        raise KeyError(f"Record {record.get('id')} is missing the reserved 'difficulty' field.")
    if record["difficulty"] is not None:
        raise ValueError(
            f"Record {record.get('id')} has difficulty={record['difficulty']!r}, "
            "but Difficulty Classification is NOT implemented yet and must remain null."
        )


def run_difficulty_classification(*_args: Any, **_kwargs: Any) -> None:
    """Guard ensuring Difficulty Classification is never executed prematurely."""
    raise NotImplementedError(
        "Vocabulary Difficulty Classification (Easy / Medium / Hard) is architecturally prepared "
        "only and is intentionally NOT implemented yet."
    )
