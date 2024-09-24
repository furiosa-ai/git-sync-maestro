from typing import Any, Dict

from ..exceptions import ExecutionError
from ..interface.context import BaseContext
from .register_plugin import PluginRegistry


class ExecutorFactory:
    def __init__(self, context: BaseContext):
        self.context = context

    def __call__(self, action_type: str, action_config: dict):
        plugin_class = PluginRegistry.get(action_type)
        action_name, action_line = self.context.get_action_info()
        if plugin_class:
            try:
                plugin = plugin_class(self.context)
                resolved_config = plugin.resolve_config(action_config)
                self.context.set_action_args(resolved_config)
                plugin.validate_config(resolved_config)
                return plugin.run(**resolved_config)
            except Exception as e:
                raise ExecutionError(action_name, action_line, e)
        else:
            raise ExecutionError(
                action_name, action_line, ValueError(f"Plugin '{action_type}' not found")
            )
