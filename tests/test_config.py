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
