"""I/O utilities for GoAnki."""

from __future__ import annotations

from .config import AppConfig, TargetSpec, config_from_mapping, load_config, override_config, parse_target_option
from .reader import read_input_words
from .writer import write_records

__all__ = [
    "AppConfig",
    "TargetSpec",
    "config_from_mapping",
    "load_config",
    "override_config",
    "parse_target_option",
    "read_input_words",
    "write_records",
]


