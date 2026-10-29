"""Vocabulary Rendering stage package."""

from __future__ import annotations

from processors.rendering.contract import (
    ALLOWED_DIFFICULTY_LABELS,
    STAGE_NAME,
    STAGE_VERSION,
    evaluate_rendering_eligibility,
)
from processors.rendering.renderer import (
    audit_and_render_all,
    audit_dataset_records,
    render_record,
    render_source_dataset,
)
from processors.rendering.template import (
    BOOKMARK_SVG,
    SHARED_STYLES,
    format_russian_for_card,
    render_backtest_page_html,
    render_record_block,
    render_vocabulary_page,
)

__all__ = [
    "ALLOWED_DIFFICULTY_LABELS",
    "BOOKMARK_SVG",
    "SHARED_STYLES",
    "STAGE_NAME",
    "STAGE_VERSION",
    "audit_and_render_all",
    "audit_dataset_records",
    "evaluate_rendering_eligibility",
    "format_russian_for_card",
    "render_backtest_page_html",
    "render_record",
    "render_record_block",
    "render_source_dataset",
    "render_vocabulary_page",
]
