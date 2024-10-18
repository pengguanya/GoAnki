from types import SimpleNamespace
from pathlib import Path

from goanki import cli
from goanki.io.config import AppConfig, TargetSpec


def test_parse_secrets_accepts_multiple_entries():
