"""Output serialization helpers."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List

from goanki.models import FlashcardRecord

from .config import TargetSpec

