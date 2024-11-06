"""Translator registry for pluggable engines."""

from __future__ import annotations

from typing import Dict, Iterable, Type

from .base import Translator


class TranslatorRegistry:
    """Registry of available translator classes."""

