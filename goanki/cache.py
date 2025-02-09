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
