"""Persistent SQLite-backed translation cache."""

from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path
from typing import Optional


class TranslationCache:
    """Simple persistent cache mapping (engine, src, dst, text) to translation."""

    def __init__(self, path: Path):
        self.path = path.expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS translations (
                    engine TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    text TEXT NOT NULL,
                    translated_text TEXT,
                    metadata TEXT,
                    updated_at REAL NOT NULL,
                    PRIMARY KEY (engine, source_lang, target_lang, text)
                )
                """
            )

    def get(self, engine: str, source_lang: str, target_lang: str, text: str) -> Optional[tuple[str, Optional[str]]]:
        """Return cached translation and metadata, if present."""
        with self._lock, self._conn:  # type: ignore[call-arg]
            row = self._conn.execute(
                """
                SELECT translated_text, metadata
                FROM translations
                WHERE engine=? AND source_lang=? AND target_lang=? AND text=?
                """,
                (engine, source_lang, target_lang, text),
            ).fetchone()
        return row if row else None

    def set(
        self,
        engine: str,
        source_lang: str,
        target_lang: str,
        text: str,
        translated_text: Optional[str],
        metadata: Optional[str] = None,
    ) -> None:
        """Persist a translation result."""
        with self._lock, self._conn:  # type: ignore[call-arg]
            self._conn.execute(
                """
                INSERT OR REPLACE INTO translations
                (engine, source_lang, target_lang, text, translated_text, metadata, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (engine, source_lang, target_lang, text, translated_text, metadata, time.time()),
            )

    def close(self) -> None:
        """Close the underlying sqlite connection."""
        self._conn.close()


