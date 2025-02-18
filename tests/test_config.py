from pathlib import Path
import textwrap

from goanki.io.config import (
    AppConfig,
    TargetSpec,
    config_from_mapping,
    load_config,
    override_config,
    parse_target_option,
)


def test_parse_target_option_supports_engine_flag():
    spec = parse_target_option("en:linguee", use_as_prompt=True)
    assert spec.lang == "en"
    assert spec.engine == "linguee"
    assert spec.use_as_prompt is True


def test_load_config_yaml(tmp_path: Path):
