"""High-level translation orchestration."""

from __future__ import annotations

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

try:  # pragma: no cover - tqdm is optional at runtime, covered via dependency
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

from goanki.cache import TranslationCache
