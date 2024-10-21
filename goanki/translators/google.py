"""Google Translate engine implementation."""

from __future__ import annotations

from typing import Optional

from bs4 import BeautifulSoup

from .base import HTTPTranslator, TranslationResult, ensure_language
from .registry import register


@register
class GoogleTranslator(HTTPTranslator):
    """Fetch translations from the public Google Translate mobile endpoint."""

