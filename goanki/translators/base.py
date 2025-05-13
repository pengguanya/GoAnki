"""Shared translator abstractions and utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
import time
from typing import Any, Dict, Iterable, Optional, Protocol

import requests


class TranslatorError(RuntimeError):
    """Raised when a translator fails permanently."""


@dataclass(slots=True)
class TranslationResult:
    """Container for a single translation."""

    engine: str
    source_lang: str
    target_lang: str
    text: str
    translated_text: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


