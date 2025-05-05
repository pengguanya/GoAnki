"""Linguee translator implementation."""

from __future__ import annotations

from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import HTTPTranslator, TranslationResult, ensure_language
from .registry import register


@register
class LingueeTranslator(HTTPTranslator):
    """Scrape Linguee dictionary entries."""

    name = "linguee"
    base_url = "https://www.linguee.com/"
    gender_map = {
        "masculine": "der",
        "feminine": "die",
        "neuter": "das",
        "plural": "die",
    }

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        text = text.strip()
        src = ensure_language(source_lang)
        tgt = ensure_language(target_lang)
