"""
Check that config loading and parsing for black works correctly.
"""

import pathlib
import textwrap

import pytest

from pyls_black_macchiato import plugin


def test_load_config(tmp_path: pathlib.Path):
    config_file = tmp_path / "pyproject.toml"
    src_path = tmp_path / "some" / "package"
    with config_file.open(mode="w") as fp:
        fp.write(
            textwrap.dedent(
                """
            [tool.black]
            line_length = 100
            skip_string_normalization = true
            """
            )
        )

    mode, fast = plugin.load_config(str(src_path))
    assert mode.line_length == 100
    assert mode.string_normalization is False


@pytest.mark.parametrize(
    "key_name, value, expected_fast",
    [
        ("fast", True, True),
        ("fast", False, False),
        ("slow", True, False),
        ("slow", False, True),
    ],
)
def test_load_config_fast_slow(
    tmp_path: pathlib.Path, key_name: str, value: bool, expected_fast: bool
):
    config_file = tmp_path / "pyproject.toml"
    with config_file.open(mode="w") as fp:
        fp.write(f"[tool.black]\n{key_name} = {str(value).lower()}")

    _, fast = plugin.load_config(str(tmp_path))
    assert fast is expected_fast
