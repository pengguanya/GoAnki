"""Input parsing helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

from goanki.translators.base import deduplicate_preserve_order

DATE_REGEX = re.compile(r"\d{2}\.\d{2}\.\d{4}")

