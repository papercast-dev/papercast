# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Papercast"
copyright = "2023, Gabriel Simmons"
author = "Gabriel Simmons"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/g-simmons/papercast",
    "use_repository_button": True,
}

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "g-simmons",  # Username
    "github_repo": "papercast",  # Repo name
    "github_version": "master",  # Version
    "conf_py_path": "/docs/source/",  # Path in the checkout to the docs root
}


html_static_path = ["_static"]
myst_enable_extensions = ["colon_fence"]
