"""
Python Language Server plugin to provide formatting via black-macchiato.
"""

from typing import List

import macchiato

from pyls import hookimpl
from pyls.workspace import Document

from pyls_black_macchiato.lsp import Range, TextEdit


@hookimpl(tryfirst=True)
def pyls_format_document(document: Document) -> List[TextEdit]:
    try:
        lines = _macchiato_format(document.lines)
    except ValueError:
        return []

    range: Range = {
        "start": {"line": 0, "character": 0,},
        "end": {"line": len(document.lines), "character": 0,},
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
        lines = _macchiato_format(lines)
    except ValueError:
        return []

    edit: TextEdit = {"range": range, "newText": "".join(lines)}
    return [edit]


def _macchiato_format(lines: List[str]) -> List[str]:
    lines, wrap_info = macchiato.wrap_lines(lines)
    try:
        lines = macchiato.format_lines(lines)
    except RuntimeError:
        raise ValueError
    return macchiato.unwrap_lines(lines, wrap_info)
