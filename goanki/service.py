"""High-level translation orchestration."""

from __future__ import annotations

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

try:  # pragma: no cover - tqdm is optional at runtime, covered via dependency
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

from goanki.cache import TranslationCache
from goanki.io.config import AppConfig, TargetSpec
from goanki.models import FlashcardRecord
from goanki.translators import TranslationResult, TranslatorError, registry


@dataclass(slots=True)
class TranslationTask:
    word: str


class TranslationService:
    """Translate batches of words using configured engines."""

    def __init__(
        self,
        config: AppConfig,
        *,
        cache: TranslationCache | None = None,
    ) -> None:
        self.config = config
        self.cache = cache
        self.log = logging.getLogger("goanki.service")
        self._translators: Dict[str, object] = {}

    def translate_words(self, words: Sequence[str]) -> List[FlashcardRecord]:
        if not words:
            return []
        tasks = [TranslationTask(word=word) for word in words]
        iterator: Iterable[TranslationTask] = tasks
        if self.config.progress and tqdm:  # pragma: no branch - depends on availability
