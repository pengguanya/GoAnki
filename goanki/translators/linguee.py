"""Linguee translator implementation."""

from __future__ import annotations

from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import HTTPTranslator, TranslationResult, ensure_language
from .registry import register

