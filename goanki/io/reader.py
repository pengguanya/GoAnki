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
