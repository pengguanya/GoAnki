"""Translator package exports."""

from __future__ import annotations

from .base import HTTPTranslator, TranslationResult, Translator, TranslatorError
from .registry import register, registry

# Ensure built-in translators are registered at import time.
from . import google as _google  # noqa: F401
from . import linguee as _linguee  # noqa: F401

__all__ = [
    "HTTPTranslator",
    "TranslationResult",
    "Translator",
    "TranslatorError",
