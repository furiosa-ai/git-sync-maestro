from typing import Any, Dict

from ..exceptions import PluginExecutionError
from .register_plugin import PluginRegistry


class PluginExecutor:
    def __init__(self, context):
        self.context = context

    def __call__(self, action_type: str, action_config: dict, action_name: str, action_line: int):
        plugin_class = PluginRegistry.get(action_type)
        if plugin_class:
            try:
                plugin = plugin_class(self.context)
                resolved_config = plugin.resolve_config(action_config)
                plugin.validate_config(resolved_config)
                return plugin.run(**resolved_config)
            except Exception as e:
                raise PluginExecutionError(action_name, action_line, e)
        else:
            raise PluginExecutionError(
                action_name, action_line, ValueError(f"Plugin '{action_type}' not found")
            )
