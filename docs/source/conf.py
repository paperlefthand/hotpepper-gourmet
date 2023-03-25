import os
import sys

sys.path.insert(0, os.path.abspath("../../"))
# autodoc_mock_imports = ["pygourmet"]


project = "hotpepper-gourmet"
copyright = "2023, Miura Kosuke"
author = "Miura Kosuke"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "ja"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "pyramid"

html_static_path = ["_static"]
