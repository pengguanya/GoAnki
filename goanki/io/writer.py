"""Output serialization helpers."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List

from goanki.models import FlashcardRecord

from .config import TargetSpec


def write_records(
    records: Iterable[FlashcardRecord],
    *,
    target_specs: List[TargetSpec],
    output_format: str,
    output_path: Path,
) -> None:
    """Serialize flashcard records to disk."""
    output_format = output_format.lower()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "csv":
        _write_delimited(records, target_specs, output_path, delimiter=",")
