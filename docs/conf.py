"""Sphinx configuration."""
project = "sendlive"
author = "Liam Brenner"
copyright = "2023, Liam Brenner"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
