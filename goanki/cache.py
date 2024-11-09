"""Persistent SQLite-backed translation cache."""

from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path
from typing import Optional

