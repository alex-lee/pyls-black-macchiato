from setuptools import setup, find_packages

setup(
    name="pyls-black-macchiato",
    version="0.1",
    description="Black-macchiato plugin for the Python Language Server",
    url="https://github.com/alex-lee/pyls-black-macchiato",
    author="Alex Lee",
    author_email="alex@collat.io",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "python-language-server",
        (
            "black-macchiato @ "
            "git+https://github.com/alex-lee/black-macchiato.git@refactor-for-plugin-use"
        ),
        "typing-extensions",
    ],
    extras_require={"dev": ["flake8", "mypy", "pytest"]},
    entry_points={"pyls": ["pyls_black_macchiato = pyls_black_macchiato.plugin"]},
)
