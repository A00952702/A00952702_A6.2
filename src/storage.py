"""
storage.py
Simple JSON storage helpers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json_list(path: str) -> list[dict[str, Any]]:
    """Read a JSON file that must contain a list. Returns empty list if file is empty."""
    file_path = Path(path)

    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8").strip()
    if not content:
        return []

    data = json.loads(content)
    if not isinstance(data, list):
        raise ValueError("JSON root must be a list.")
    return data


def write_json_list(path: str, items: list[dict[str, Any]]) -> None:
    """Write a list of dicts to a JSON file (pretty formatted)."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps(items, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )