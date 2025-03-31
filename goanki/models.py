"""Shared data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .translators.base import TranslationResult


@dataclass(slots=True)
class FlashcardRecord:
