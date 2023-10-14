from papercast.plugin_utils import load_plugins
from papercast.publishers import *

_installed_plugins = load_plugins("publishers")

for name, plugin in _installed_plugins.items():
    globals()[name] = plugin
