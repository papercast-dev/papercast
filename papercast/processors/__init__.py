from papercast.plugin_utils import load_plugins
from papercast.processors import *

_installed_plugins = load_plugins("processors")

for name, plugin in _installed_plugins.items():
    globals()[name] = plugin
