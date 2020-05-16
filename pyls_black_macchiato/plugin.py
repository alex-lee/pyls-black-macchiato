"""
Python Language Server plugin to provide formatting via black-macchiato.
"""

import logging
from typing import List, Tuple

import attr
import black
import toml

import macchiato
from pyls import hookimpl
from pyls.workspace import Document

from pyls_black_macchiato.lsp import Range, TextEdit


log = logging.getLogger(__name__)


@hookimpl(tryfirst=True)
def pyls_format_document(document: Document) -> List[TextEdit]:
    try:
        lines = macchiato_format(document.path, document.lines)
    except black.NothingChanged:
        return []

    range: Range = {
        "start": {"line": 0, "character": 0},
        "end": {"line": len(document.lines), "character": 0},
    }

    edit: TextEdit = {"range": range, "newText": "".join(lines)}
    return [edit]


@hookimpl(tryfirst=True)
def pyls_format_range(document: Document, range: Range) -> List[TextEdit]:
    range["start"]["character"] = 0
    range["end"]["line"] += 1
    range["end"]["character"] = 0

    l_start = range["start"]["line"]
    l_end = range["end"]["line"]

    lines = document.lines[l_start:l_end]

    try:
        lines = macchiato_format(document.path, lines)
    except black.NothingChanged:
        return []

    edit: TextEdit = {"range": range, "newText": "".join(lines)}
    return [edit]


def macchiato_format(src_path: str, lines: List[str]) -> List[str]:
    mode, fast = load_config(src_path)
    lines, wrap_info = macchiato.wrap_lines(lines)
    text = black.format_file_contents("".join(lines), fast=fast, mode=mode)
    lines = text.splitlines(True)
    return macchiato.unwrap_lines(lines, wrap_info)


def load_config(src_path: str) -> Tuple[black.FileMode, bool]:
    """Load black configuration from ``pyproject.toml``."""

    mode = black.FileMode()
    fast = False

    root = black.find_project_root((src_path,))
    config_path = root / "pyproject.toml"
    if not config_path.is_file():
        return mode, fast

    try:
        parsed_toml = toml.load(str(config_path))
    except (toml.TomlDecodeError, OSError) as e:
        log.warning("Could not parse config: %s: %s", config_path, e)
        return mode, fast

    config = parsed_toml.get("tool", {}).get("black", {})
    if not config:
        return mode, fast

    # Normalize config.
    config = {k.replace("--", "").replace("-", "_"): v for k, v in config.items()}
    if "skip_string_normalization" in config:
        config["string_normalization"] = not config.pop("skip_string_normalization")

    if "fast" in config:
        fast = config.pop("fast")
    if "slow" in config:
        fast = not config.pop("slow")

    # Convert to a black.FileMode.
    config_fields = [f.name for f in attr.fields(black.FileMode)]
    config = {k: v for k, v in config.items() if k in config_fields}
    logging.info("Loaded config: %s", config)  # TODO debug

    return black.FileMode(**config), fast
