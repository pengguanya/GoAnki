"""Translator registry for pluggable engines."""

from __future__ import annotations

from typing import Dict, Iterable, Type

from .base import Translator


class TranslatorRegistry:
    """Registry of available translator classes."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Translator]] = {}

    def register(self, translator_cls: Type[Translator]) -> None:
        """Register a translator class by its `name` attribute."""
        name = getattr(translator_cls, "name", None)
        if not name:
            raise ValueError("Translator classes must define a non-empty `name` attribute.")
        key = name.lower()
        if key in self._registry:
            raise ValueError(f"Translator '{name}' is already registered.")
        self._registry[key] = translator_cls
