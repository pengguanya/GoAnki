from types import SimpleNamespace
from pathlib import Path

from goanki import cli
from goanki.io.config import AppConfig, TargetSpec


def test_parse_secrets_accepts_multiple_entries():
    secrets = cli.parse_secrets(["deepl=DEEPL_KEY", "custom=MY_ENV"])
    assert secrets["deepl"] == "DEEPL_KEY"
    assert secrets["custom"] == "MY_ENV"


def test_resolve_output_path_defaults(tmp_path: Path):
    config = AppConfig()
    config.output_path = None
