import os
import sys
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv not installed. Skipping loading .env file.")

sys.path.insert(0, os.path.abspath("."))
from docs_utils import (  # type: ignore
    get_plugin_list,
    clone_plugin,
    install_plugin,
    make_child_rst,
    make_parent_rst,
    PLUGIN_DOCS_PATH,
)


DOCS_ENV = os.getenv("DOCS_ENV", "rtd")
FORCE_CLONE = os.getenv("FORCE_CLONE", True)

sys.path.insert(0, os.path.abspath("../.."))

project = "Papercast"
copyright = "2023, Gabriel Simmons"
author = "Gabriel Simmons"

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_book_theme"
html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/g-simmons/papercast",
    "use_repository_button": True,
}

html_context = {
    "display_github": True,
    "github_user": "g-simmons",
    "github_repo": "papercast",
    "github_version": "master",
    "conf_py_path": "/docs/source/",
    "default_mode": "light",
}

html_static_path = ["_static"]
myst_enable_extensions = ["colon_fence"]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

plugins = get_plugin_list(docs_env=DOCS_ENV)

contribs = {}
if plugins is not None:
    for plugin in plugins:
        plugin_repo = f"https://github.com/{plugin.repo}.git"
        plugin_path = PLUGIN_DOCS_PATH / plugin.id

        if not plugin_path.exists() or FORCE_CLONE:
            if DOCS_ENV == "local":
                os.symlink(plugin.local, plugin_path)
            else:
                clone_plugin(plugin_repo, str(plugin_path))

        install_plugin(str(plugin_path))

        if plugin.contributes is not None:
            contribs.update(plugin.contributes)

make_parent_rst()
make_child_rst(contribs)
