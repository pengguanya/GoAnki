"""Google Translate engine implementation."""

from __future__ import annotations

from typing import Optional

from bs4 import BeautifulSoup

from .base import HTTPTranslator, TranslationResult, ensure_language
from .registry import register


@register
class GoogleTranslator(HTTPTranslator):
    """Fetch translations from the public Google Translate mobile endpoint."""

    name = "google"
    base_url = "https://translate.google.com/m"

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        text = text.strip()
        params = {
            "sl": ensure_language(source_lang),
            "tl": ensure_language(target_lang),
            "q": text,
            "ie": "UTF-8",
        }
        response = self.request("GET", self.base_url, params=params)
        translated_text = self._parse_response(response.text)
        return TranslationResult(
            engine=self.name,
            source_lang=params["sl"],
            target_lang=params["tl"],
            text=text,
            translated_text=translated_text,
            metadata={"url": str(response.url)},
        )

    def _parse_response(self, html: str) -> Optional[str]:
        soup = BeautifulSoup(html, "lxml")
