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
        path = "/".join((f"{src}-{tgt}", "search"))
        url = urljoin(self.base_url, path)
        params = {"query": text, "source": "auto"}
        response = self.request("GET", url, params=params)
        soup = BeautifulSoup(response.text, "lxml")
        translated_text = self._extract_translation(soup)
        formatted_source = self._format_source_word(soup, text)
        metadata = {
            "url": str(response.url),
            "formatted_source": formatted_source,
            "word_type": self._extract_type(soup),
        }
        return TranslationResult(
            engine=self.name,
            source_lang=src,
            target_lang=tgt,
            text=text,
            translated_text=translated_text,
            metadata=metadata,
        )

    def _extract_translation(self, soup: BeautifulSoup) -> Optional[str]:
        answer_tag_list = soup.find_all("a", class_="dictLink")
        if len(answer_tag_list) > 1:
            short_list = answer_tag_list[:2]
            joint = "; ".join(tag.text.strip() for tag in short_list if tag.text)
            return joint or None
        if answer_tag_list:
            tag = answer_tag_list[0]
            return tag.text.strip() if tag.text else None
        return None

    def _format_source_word(self, soup: BeautifulSoup, fallback: str) -> str:
        word = self._extract_word(soup) or fallback
        word_type = self._extract_type(soup)
        if word_type and "noun" in word_type.lower():
            segments = [segment.strip() for segment in word_type.split(",")]
            noun_gender = segments[-1].lower() if segments else ""
            article = self.gender_map.get(noun_gender, "")
            descriptor = segments[0] if segments else word_type
            noun_repr = f"{article} {word}".strip()
            return f"{noun_repr} ({descriptor})"
        if word_type and "," in word_type:
            descriptor = word_type.split(",")[0].strip()
            return f"{word} ({descriptor})"
        if word_type:
            return f"{word} ({word_type})"
        return word

    @staticmethod
    def _extract_word(soup: BeautifulSoup) -> Optional[str]:
        span = soup.find("span", class_="dictTerm")
        if span and span.text:
            return span.text.strip()
        return None

    @staticmethod
    def _extract_type(soup: BeautifulSoup) -> Optional[str]:
        span = soup.find("span", class_="tag_wordtype")
        if span and span.text:
            return span.text.strip()
        return None


