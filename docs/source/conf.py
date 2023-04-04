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

def get_plugin_list(local: str):
    if not local:
        url = "https://raw.githubusercontent.com/papercast-dev/papercast-community/main/plugins.jsonc"
        response = requests.get(url)
        if response.status_code == 200:
            return json5.loads(response.text)
        else:
            return []
    else: 
        return [
                {
                    "id": "papercast-arxiv",
                    "name": "ArXiV",
                    "author": "papercast-dev",
                    "description": "Collect papers from ArXiV",
                    "type": "collector",
                    "repo": "papercast-dev/papercast-arxiv",
                    "local": "/Users/gabe/papercast_all/_plugin_collectors/papercast-arxiv"
                }
            ]

def clone_plugin(repo_url, target_folder) -> bool:
    try:
        subprocess.check_call(['git', 'clone', repo_url, target_folder])
        print(f"Successfully cloned {repo_url} into {target_folder}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone {repo_url}. Error: {e}")
        return False

def install_plugin(plugin_path) -> bool:
    try:
        os.chdir(plugin_path)
        subprocess.check_call(['pip', 'install', '.'])
        os.chdir(os.path.dirname(plugin_path))
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install plugin from {plugin_path}. Error: {e}")
        return False

def get_plugin_classes(plugin_folder) -> Dict[str, List[str]]:
    setup_cfg_path = Path(plugin_folder) / "setup.cfg"

    out = defaultdict(list)

    config = setuptools.config.read_configuration(setup_cfg_path)
    for k, v in config["options"]["entry_points"].items():
        for v_item in v:
            out[k].append(v_item.split("=")[0].strip())
    
    return out

local = True
plugins = get_plugin_list(local=True)

docs_path = Path(__file__).parent 
plugin_docs_path = docs_path / 'plugins'

collectors = []
processors = []
publishers = []

for plugin in plugins:
    plugin_repo = f"https://github.com/{plugin['repo']}.git"
    plugin_path = plugin_docs_path / plugin['id']

    if not plugin_path.exists(): 
        if local:
            os.symlink(plugin["local"], plugin_path)
        else:
            clone_plugin(plugin_repo, str(plugin_path))

    install_plugin(str(plugin_path))
    
    plugin_classes = get_plugin_classes(str(plugin_path))
    collectors.extend(plugin_classes["papercast.collectors"])
    

rst_path= docs_path / "api_reference" / "collectors.rst"
rst_path.parent.mkdir(parents=True, exist_ok=True)

rst_content = textwrap.dedent("""
    Collectors
    ==========

    .. toctree::
        :maxdepth: 2
        :glob: 

        collectors/* 
    """
    )

with open(rst_path, "w") as f:
    f.write(rst_content)

for collector in collectors:
    rst_content = textwrap.dedent(f"""
        {collector}
        {"=" * len(collector)}

        .. autoclass:: papercast.collectors.{collector}
            :members:
            :undoc-members:

        """
    )

    rst_path= docs_path / "api_reference" / "collectors"
    with (rst_path / (collector.lower() + ".rst")).open("w") as f:
        f.write(rst_content)


# sys.path.insert(0, os.path.abspath("/Users/gabe/papercast_all/papercast/docs/source/plugins/papercast-arxiv/papercast_arxiv"))
# sys.path.insert(0, os.path.abspath("/Users/gabe/papercast_all/papercast/docs/source/plugins/papercast-arxiv/papercast_arxiv/papercast_arxiv.py"))
# sys.path.insert(0, os.path.abspath("/Users/gabe/papercast_all/papercast/docs/source/plugins/papercast-arxiv/"))