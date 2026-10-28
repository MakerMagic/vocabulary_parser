"""Provenance, deterministic hashing, and JSON pointer utilities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def sha256_bytes(data: bytes) -> str:
    """Compute hex SHA-256 of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    """Compute hex SHA-256 of a file on disk."""
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(obj: Any) -> bytes:
    """Serialize object to deterministic UTF-8 JSON bytes (sorted keys, 2-space indent)."""
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return text.encode("utf-8")


def write_canonical_json(path: Path, obj: Any) -> str:
    """Write deterministic UTF-8 JSON and return its SHA-256 hex digest."""
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_json_bytes(obj)
    path.write_bytes(raw)
    return sha256_bytes(raw)


def compute_content_hash(obj: Any) -> str:
    """Compute deterministic SHA-256 content hash for a dictionary or value."""
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def resolve_json_pointer(doc: Any, pointer: str) -> Any:
    """Resolve an RFC 6901 JSON pointer against a loaded JSON document."""
    if pointer == "" or pointer == "#":
        return doc
    if not pointer.startswith("/"):
        raise ValueError(f"Invalid JSON pointer (must start with '/'): {pointer!r}")
    parts = pointer.lstrip("/").split("/")
    current = doc
    for raw_part in parts:
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            idx = int(part)
            current = current[idx]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(f"Cannot traverse {part!r} in non-container at pointer {pointer!r}")
    return current
