# Black-macchiato plugin for the Python Language Server (pyls)

To use the [black] code formatter with [pyls], in most cases you can just use the [pyls-black]
plugin. This plugin serves as an alternative if you need the ability to do range formatting.

Such functionality is provided by [black-macchiato], while `black` only formats complete documents
(see the `black-macchiato` readme for more background).

This plugin works similarly to `pyls-black`, but it uses the wrapping functionality from
`black-macchiato` to enable formatting of (mostly) arbitrary ranges. Currently it vendors
`macchiato.py` from my [fork of black-macchiato][black-macchiato-fork], which has been refactored to
better expose the bits that are needed here.

[black]: https://black.readthedocs.io/en/stable/
[pyls]: https://github.com/palantir/python-language-server
[pyls-black]: https://github.com/rupert/pyls-black
[black-macchiato]: https://github.com/wbolster/black-macchiato
[black-macchiato-fork]: https://github.com/alex-lee/black-macchiato

## Configuration

Install this plugin into the same virtualenv as `pyls`. For example, on my system I am using
[vim-lsp] and [vim-lsp-settings], so I do the following:

```
$ ~/.local/share/vim-lsp-settings/servers/pyls/venv/bin/pip install pyls-black-macchiato
```

When formatting, the plugin will use logic similar to what's in `black` and `pyls-black` to search
for a `pyproject.toml` and load its settings from there.

[vim-lsp]: https://github.com/prabirshrestha/vim-lsp
[vim-lsp-settings]: https://github.com/mattn/vim-lsp-settings
