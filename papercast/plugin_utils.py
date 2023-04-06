from papercast.base import BasePipelineComponent
import importlib.metadata
from importlib import import_module
from papercast.plugin_utils import validate_base_pipeline_component, validate_output_types

def validate_base_pipeline_component(plugin_module):
    if not issubclass(plugin_module, BasePipelineComponent):
        raise TypeError(f"Plugin {plugin_module.__name__} should be aa subclass of papercast.base.BasePipelineComponent")
    
def validate_input_types(plugin_module):
    if not hasattr(plugin_module, 'input_types'):
        raise TypeError(f"Plugin {plugin_module.__name__} should have an input_types property")

def validate_output_types(plugin_module):
    if not hasattr(plugin_module, 'output_types'):
        raise TypeError(f"Plugin {plugin_module.__name__} should have an output_types property")

def validate_process_method(plugin_module):
    if not hasattr(plugin_module, 'process'):
        raise TypeError(f"Plugin {plugin_module.__name__} should have a process method")

def load_plugins(plugin_type: str):
    plugins = {}
    for entry_point in importlib.metadata.entry_points().get(f'papercast.{plugin_type}', []):
        plugin_module = entry_point.load()

        if plugin_type == "collectors":
            validate_process_method(plugin_module)
            validate_output_types(plugin_module)

        elif plugin_type == "subscribers":
            validate_base_pipeline_component(plugin_module)
            validate_output_types(plugin_module)

        elif plugin_type == "publishers":
            validate_base_pipeline_component(plugin_module)
            validate_input_types(plugin_module)

        elif plugin_type == "processors":
            validate_base_pipeline_component(plugin_module)
            validate_input_types(plugin_module)
            validate_output_types(plugin_module)

        plugins[entry_point.name] = plugin_module

    return plugins