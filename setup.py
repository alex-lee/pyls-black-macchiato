import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyls-black-macchiato",
    version="0.1.2",
    author="Alex Lee",
    author_email="alex@collat.io",
    description="Black-macchiato plugin for the Python Language Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex-lee/pyls-black-macchiato",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["black-macchiato>=1.3.0", "python-language-server", "typing-extensions"],
    extras_require={"dev": ["flake8", "mypy", "pytest"]},
    entry_points={"pyls": ["pyls_black_macchiato = pyls_black_macchiato.plugin"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
