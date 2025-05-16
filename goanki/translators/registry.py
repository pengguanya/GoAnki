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

    def create(self, name: str, **kwargs) -> Translator:
        """Instantiate a translator by name."""
        key = name.lower()
        translator_cls = self._registry.get(key)
        if not translator_cls:
            available = ", ".join(sorted(self._registry))
            raise KeyError(f"Translator '{name}' is not registered. Available: {available or 'none'}.")
        return translator_cls(**kwargs)

    def names(self) -> Iterable[str]:
        """Return registered names."""
        return sorted(self._registry)


registry = TranslatorRegistry()


def register(translator_cls: Type[Translator]) -> Type[Translator]:
    """Class decorator to register translators."""
    registry.register(translator_cls)
    return translator_cls


