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
    args = SimpleNamespace(output=None)
    input_path = tmp_path / "vocab.txt"
    resolved = cli.resolve_output_path(args, config, input_path)
    assert resolved.name == "vocab_GoAnki.csv"


def test_build_target_specs_sets_prompt_flag():
    args = SimpleNamespace(
