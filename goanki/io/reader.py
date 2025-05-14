"""Input parsing helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

from goanki.translators.base import deduplicate_preserve_order

DATE_REGEX = re.compile(r"\d{2}\.\d{2}\.\d{4}")


def read_input_words(path: Path, *, deduplicate: bool = True) -> List[str]:
    """
    Read vocabulary terms from AutoNotes exports or plain text files.

    AutoNotes files contain a single line with a date field; plain text files
    contain one entry per line with optional blank lines and header rows.
    """
    path = path.expanduser()
    text = path.read_text(encoding="utf-8")
    if "_AutoNotes" in path.name:
        words = _parse_autonotes(text)
    else:
        words = _parse_plain_lines(text.splitlines())
    words = [word.strip() for word in words if word.strip()]
    if deduplicate:
        return deduplicate_preserve_order(words)
    return words


def _parse_autonotes(text: str) -> List[str]:
    first_line = text.splitlines()[0] if text else ""
    match = DATE_REGEX.search(first_line)
    if not match:
        raise ValueError("AutoNotes files must contain a date field (dd.mm.yyyy).")
    field_sep = match.group(0)
    parts = first_line.split(field_sep, maxsplit=1)
    if len(parts) < 2:
        return []
    tail = parts[1].replace("|", " ")
