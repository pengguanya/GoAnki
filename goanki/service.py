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
            iterator = tqdm(tasks, desc="Translating", unit="card")
        records: List[FlashcardRecord] = []
        with ThreadPoolExecutor(max_workers=self.config.workers) as executor:
            for record in executor.map(self._translate_task, iterator):
                records.append(record)
        return records

    def _translate_task(self, task: TranslationTask) -> FlashcardRecord:
        original = task.word
        prompt = original
        translations: List[TranslationResult] = []
        for spec in self.config.targets:
            result = self._translate_with_spec(original, spec)
            translations.append(result)
            if spec.use_as_prompt:
                prompt = (
                    result.metadata.get("formatted_source")
                    or result.translated_text
                    or prompt
                )
        return FlashcardRecord(source=original, prompt=prompt, translations=translations)

    def _translate_with_spec(self, text: str, spec: TargetSpec) -> TranslationResult:
        engine_name = (spec.engine or "google").lower()
        translator = self._get_translator(engine_name)
        cached = self._fetch_cache(engine_name, self.config.source_lang, spec.lang, text)
        if cached:
            translated_text, metadata = cached
            metadata_obj = json.loads(metadata) if metadata else {}
            return TranslationResult(
                engine=engine_name,
                source_lang=self.config.source_lang,
                target_lang=spec.lang,
                text=text,
                translated_text=translated_text,
                metadata=metadata_obj,
            )
        try:
            result = translator.translate(text, self.config.source_lang, spec.lang)
        except TranslatorError as exc:
            self.log.error(
                "Translator '%s' failed for '%s' (%s->%s): %s",
                engine_name,
                text,
                self.config.source_lang,
                spec.lang,
                exc,
            )
            result = TranslationResult(
                engine=engine_name,
                source_lang=self.config.source_lang,
                target_lang=spec.lang,
                text=text,
                translated_text=None,
                metadata={"error": str(exc)},
            )
        self._store_cache(result)
        return result

    def _get_translator(self, name: str):
        if name not in self._translators:
            translator = registry.create(name)
            # Apply runtime overrides for retries/timeouts.
            if hasattr(translator, "max_retries"):
                setattr(translator, "max_retries", self.config.retries)
            if hasattr(translator, "default_timeout"):
                setattr(translator, "default_timeout", self.config.timeout)
            secret_env = self.config.secrets.get(name) if hasattr(self.config, "secrets") else None
            if secret_env:
                setattr(translator, "api_key", os.environ.get(secret_env))
            self._translators[name] = translator
        return self._translators[name]

    def _fetch_cache(
        self, engine: str, source_lang: str, target_lang: str, text: str
    ) -> tuple[str, str | None] | None:
        if not self.cache or not self.config.cache_enabled:
            return None
        return self.cache.get(engine, source_lang, target_lang, text)

    def _store_cache(self, result: TranslationResult) -> None:
        if not self.cache or not self.config.cache_enabled:
            return
        metadata = json.dumps(result.metadata, ensure_ascii=False) if result.metadata else None
        self.cache.set(
            result.engine,
            result.source_lang,
            result.target_lang,
            result.text,
            result.translated_text,
            metadata,
        )


