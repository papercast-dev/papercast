import importlib.metadata
from importlib import import_module
from papercast.base import BasePipelineComponent

def load_plugins():
    plugins = {}
    for entry_point in importlib.metadata.entry_points().get('papercast.processors', []):
        plugin_module = entry_point.load()

        if not issubclass(plugin_module, BasePipelineComponent):
            raise TypeError(f"Plugin {entry_point.name} should be aa subclass of papercast.base.BasePipelineComponent")
        
        if not hasattr(plugin_module, 'input_types'):
            raise TypeError(f"Plugin {entry_point.name} should have an input_types method")
        
        if not hasattr(plugin_module, 'process'):
            raise TypeError(f"Plugin {entry_point.name} should have a process method")

        plugins[entry_point.name] = plugin_module
    return plugins

_installed_plugins = load_plugins()

for name, plugin in _installed_plugins.items():
    globals()[name] = plugin
