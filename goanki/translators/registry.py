"""Translator registry for pluggable engines."""

from __future__ import annotations

from typing import Dict, Iterable, Type

from .base import Translator


class TranslatorRegistry:
    """Registry of available translator classes."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Translator]] = {}

    def register(self, translator_cls: Type[Translator]) -> None:
