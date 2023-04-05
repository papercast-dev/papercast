import os
from collections import defaultdict
import setuptools
import sys
import requests
import json5
import os
from typing import Any, Dict, List
import textwrap
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

env = os.environ.get("PAPERCAST_DOCS_ENV", "rtd")

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

docs_path = Path(__file__).parent 
plugin_docs_path = docs_path / 'plugins'

def get_plugin_list() -> List[Dict[str, Any]]:
    if env == "rtd":
        url = "https://raw.githubusercontent.com/papercast-dev/papercast-community/main/plugins.jsonc"
        response = requests.get(url)
        if response.status_code == 200:
            return json5.loads(response.text) # type: ignore
        else:
            return []
    elif env == "local": 
        return [
                {
                    "id": "papercast-arxiv",
                    "name": "ArXiV",
                    "author": "papercast-dev",
                    "description": "Collect papers from ArXiV",
                    "type": "collector",
                    "repo": "papercast-dev/papercast-arxiv",
                    "local": Path(__file__).parent.parent.parent / "_plugin_collectors/papercast-arxiv"
                }
            ]
    else:
        raise ValueError(f"Unknown environment: {env}")

def clone_plugin(repo_url: str, download_path: Path) -> bool:
    if not download_path.exists(): 
        if env == "local":
            os.symlink(plugin["local"], download_path)
            return True

        elif env == "rtd":
            try:
                subprocess.check_call(['git', 'clone', repo_url, download_path])
                print(f"Successfully cloned {repo_url} into {download_path}")
                return True

            except subprocess.CalledProcessError as e:
                print(f"Failed to clone {repo_url}. Error: {e}")
                return False

        else:
            print(f"Unknown environment: {env}")
            return False
    else:
        print(f"Plugin already exists at {download_path}")
        return True

def install_plugin(download_path) -> bool:
    try:
        os.chdir(download_path)
        subprocess.check_call(['pip', 'install', '.'])
        os.chdir(os.path.dirname(download_path))
        return True

    except subprocess.CalledProcessError as e:
        print(f"Failed to install plugin from {download_path}. Error: {e}")
        return False

def get_plugin_classes(download_path) -> Dict[str, List[str]]:
    setup_cfg_path = Path(download_path) / "setup.cfg"

    out = defaultdict(list)

    config = setuptools.config.read_configuration(setup_cfg_path) # type: ignore

    for k, v in config["options"]["entry_points"].items():
        for v_item in v:
            out[k].append(v_item.split("=")[0].strip())
    
    return out

def make_plugin_type_rst(plugin_type: str):
    rst_path= docs_path / "api_reference" / f"{plugin_type}.rst"
    rst_path.parent.mkdir(parents=True, exist_ok=True)

    rst_content = textwrap.dedent(f"""
        {plugin_type.title()}
        ==========

        .. toctree::
            :maxdepth: 2
            :glob: 

            {plugin_type}/* 
        """
        )

    with open(rst_path, "w") as f:
        f.write(rst_content)
    
def make_plugin_class_rst(plugin_class_type: str, plugin_class_name: str):
    rst_content = textwrap.dedent(f"""
        {plugin_class_name}
        {"=" * len(plugin_class_name)}

        .. autoclass:: papercast.{plugin_class_type.replace("papercast.","")}.{plugin_class_name}
            :members:
            :undoc-members:

        """
    )

    rst_path = docs_path / f"api_reference/{plugin['type']}s/{plugin_class_name.lower()}.rst" 
    with rst_path.open("w") as f:
        f.write(rst_content)

plugins = get_plugin_list()

for plugin in plugins:
    plugin_repo = f"https://github.com/{plugin['repo']}.git"
    download_path = plugin_docs_path / plugin['id']
    clone_plugin(plugin_repo, download_path)
    install_plugin(str(download_path))
    plugin["classes"] = get_plugin_classes(str(download_path))
    
for plugin_type in ["collectors", "processors", "publishers"]:
    make_plugin_type_rst(plugin_type)

for plugin in plugins:
    for plugin_class_type, plugin_classes in plugin["classes"].items():
        for plugin_class in plugin_classes:
            print(plugin_class)
            make_plugin_class_rst(plugin_class_type, plugin_class)


# sys.path.insert(0, os.path.abspath("/Users/gabe/papercast_all/papercast/docs/source/plugins/papercast-arxiv/papercast_arxiv"))
# sys.path.insert(0, os.path.abspath("/Users/gabe/papercast_all/papercast/docs/source/plugins/papercast-arxiv/papercast_arxiv/papercast_arxiv.py"))
# sys.path.insert(0, os.path.abspath("/Users/gabe/papercast_all/papercast/docs/source/plugins/papercast-arxiv/"))