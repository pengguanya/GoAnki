"""Shared translator abstractions and utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
import time
from typing import Any, Dict, Iterable, Optional, Protocol

import requests


class TranslatorError(RuntimeError):
    """Raised when a translator fails permanently."""


@dataclass(slots=True)
class TranslationResult:
    """Container for a single translation."""

    engine: str
    source_lang: str
    target_lang: str
    text: str
    translated_text: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class Translator(Protocol):
    """Protocol implemented by all translator engines."""

    name: str

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate text from source_lang to target_lang."""


class HTTPTranslator:
    """Base class providing HTTP utilities with retries and logging."""

    name = "base"
    default_timeout = 10
    max_retries = 2
    backoff_factor = 0.5
    user_agent = "GoAnkiBot/0.1 (+https://github.com/pengg3/goanki)"

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
        self.session.headers.setdefault("User-Agent", self.user_agent)
        self.log = logging.getLogger(f"goanki.translators.{self.name}")

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> requests.Response:
        """Perform an HTTP request with retries and exponential backoff."""
        timeout = timeout or self.default_timeout
        attempt = 0
        while True:
            try:
                response = self.session.request(method, url, params=params, timeout=timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as exc:  # pragma: no cover - network failure path
                if attempt >= self.max_retries:
                    self.log.error("Translator %s failed: %s", self.name, exc)
                    raise TranslatorError(str(exc)) from exc
                sleep_for = self.backoff_factor * (2**attempt)
                self.log.warning(
                    "Request failed for %s (attempt %s/%s): %s. Retrying in %.2fs",
                    self.name,
                    attempt + 1,
                    self.max_retries + 1,
                    exc,
                    sleep_for,
                )
                time.sleep(sleep_for)
                attempt += 1

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        raise NotImplementedError


def ensure_language(lang: str) -> str:
