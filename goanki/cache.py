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
