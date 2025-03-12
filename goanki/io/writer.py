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
    elif output_format == "tsv":
        _write_delimited(records, target_specs, output_path, delimiter="\t")
    elif output_format == "json":
        _write_json(records, target_specs, output_path)
    else:
        raise ValueError(f"Unknown output format '{output_format}'. Use csv, tsv, or json.")


def _write_delimited(
    records: Iterable[FlashcardRecord],
    target_specs: List[TargetSpec],
    output_path: Path,
    *,
    delimiter: str,
) -> None:
    columns = ["prompt"] + [column_label(spec) for spec in target_specs]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter=delimiter)
        writer.writeheader()
        for record in records:
            row = {"prompt": record.prompt}
            for spec in target_specs:
                result = _find_translation(record, spec)
                row[column_label(spec)] = result or ""
            writer.writerow(row)


def _write_json(
    records: Iterable[FlashcardRecord],
    target_specs: List[TargetSpec],
    output_path: Path,
) -> None:
    payload = []
    for record in records:
        payload.append(
            {
                "prompt": record.prompt,
                "source": record.source,
                "translations": [
                    {
                        "engine": result.engine,
                        "target_lang": result.target_lang,
                        "text": result.translated_text,
                        "metadata": result.metadata,
                    }
                    for result in record.translations
                ],
            }
        )
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


