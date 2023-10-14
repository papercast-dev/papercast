from papercast.plugin_utils import load_plugins
from papercast.subscribers import *  # type: ignore

_installed_plugins = load_plugins("subscribers")

for name, plugin in _installed_plugins.items():
    globals()[name] = plugin
