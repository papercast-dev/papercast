import os
from collections import defaultdict
import setuptools
import sys
import requests
import json5
import os
from typing import Any, Dict, List, Optional
import textwrap
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

PLUGINS_LIST_URL = "https://raw.githubusercontent.com/papercast-dev/papercast-community/main/plugins.jsonc"


DOCS_PATH = Path(__file__).parent
PLUGIN_DOCS_PATH = DOCS_PATH / "plugins"


@dataclass
class PluginContrib:
    icon: str
    short_description: str
    input_types: Dict[str, str]
    output_types: Dict[str, str]


@dataclass
class Plugin:
    id: str
    name: str
    author: str
    description: str
    type: str
    repo: str
    local: str
    contributes: Dict[str, PluginContrib]


def get_plugin_list(docs_env: str) -> Optional[List[Plugin]]:
    if docs_env == "rtd":
        response = requests.get(PLUGINS_LIST_URL)
        if response.status_code == 200:
            plugins = json5.loads(response.text)
            if not isinstance(plugins, list):
                raise ValueError(f"Failed to get plugin list from {PLUGINS_LIST_URL}.")
            return [Plugin(**x) for x in json5.loads(response.text)]  # type: ignore
        else:
            raise ValueError(
                f"Failed to get plugin list from {PLUGINS_LIST_URL}. Status code: {response.status_code}"
            )

    elif docs_env == "local":
        from .local_docs_list import local_docs

        return [Plugin(**x) for x in local_docs]


def clone_plugin(repo_url, target_folder) -> bool:
    try:
        subprocess.check_call(["git", "clone", repo_url, target_folder])
        print(f"Successfully cloned {repo_url} into {target_folder}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone {repo_url}. Error: {e}")
        return False


def install_plugin(plugin_path) -> bool:
    try:
        os.chdir(plugin_path)
        subprocess.check_call(["pip", "install", "."])
        os.chdir(os.path.dirname(plugin_path))
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install plugin from {plugin_path}. Error: {e}")
        return False


# def get_plugin_classes(plugin_folder) -> Dict[str, List[str]]:
#     setup_cfg_path = Path(plugin_folder) / "setup.cfg"

#     out = defaultdict(list)

#     config = setuptools.config.read_configuration(setup_cfg_path)
#     for k, v in config["options"]["entry_points"].items():
#         for v_item in v:
#             out[k].append(v_item.split("=")[0].strip())

#     return out


def make_parent_rst():
    for contrib_type in ["subscribers", "processors", "publishers", "types"]:
        rst_path = DOCS_PATH / "api_reference" / "{contrib_type}.rst"
        rst_path.parent.mkdir(parents=True, exist_ok=True)

        rst_content = textwrap.dedent(
            f"""
            {contrib_type.title()}
            ==========

            .. toctree::
                :maxdepth: 2
                :glob: 

                contrib_type/* 
            """
        )

        with open(rst_path, "w") as f:
            f.write(rst_content)


def make_child_rst(contribs: Dict[str, PluginContrib]):
    for contrib_name, contrib in contribs.items():
        contrib_type = contrib_name.split(".")[1]
        contrib_name_only = contrib_name.split(".")[-1]

        rst_content = textwrap.dedent(
            f"""
            {contrib_name_only}
            {"=" * len(contrib_name_only)}

            .. autoclass:: {contrib_name}
                :members:
                :undoc-members:

            """
        )

        rst_path = DOCS_PATH / "api_reference" / contrib_type
        with (rst_path / (contrib_name_only.lower() + ".rst")).open("w") as f:
            f.write(rst_content)
