from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, Union

from .context import BaseContext, ContextManager


class BasePlugin(ABC):
    def __init__(self, context: BaseContext):
        self.context = context
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def do_action(self, **kwargs):
        """
        Abstract method that all plugins must implement.
        This method should contain the main logic for the synchronization task.

        :param kwargs: Keyword arguments specific to the plugin
        """
        pass

    def get_plugin_param_key(self) -> str:
        pass

    def resolve_config(self, config: Union[Dict[str, Any], str]) -> Union[Dict[str, Any], str]:
        if isinstance(config, str):
            key = self.get_plugin_param_key()
            return {key: self.context.resolve_value(config)}
        return {k: self.context.resolve_value(v) for k, v in config.items()}

    def validate_config(self, config):
        """
        Optional method to validate the configuration for this plugin.
        Subclasses can override this method to add custom validation logic.

        :param config: Configuration dictionary for the plugin
        :raises ValueError: If the configuration is invalid
        """

    def execute_hooks(self, hook_type: str, config: Dict[str, Any]):
        hooks = config.get(hook_type, [])
        if not isinstance(hooks, list):
            hooks = [hooks]

        for index, hook in enumerate(hooks, start=1):
            plugin_name, plugin_config = next(iter(hook.items()))
            with ContextManager(self.context) as context:
                hook_name = hook.get('name', f'Hook-{index}')
                hook_line = hook.get('__line__', 'Unknown')
                context.set_action_info(hook_name, hook_line)
                context.plugin_executor(plugin_name, plugin_config, hook_name, hook_line)

    # def call_plugin(self, plugin_name: str, plugin_config: Dict[str, Any]):
    #    plugin_class = self.context.get_plugin(plugin_name)
    #    if plugin_class:
    #        plugin = plugin_class(self.context)
    #        resolved_config = plugin.resolve_config(plugin_config)
    #        plugin.validate_config(resolved_config)
    #        plugin.do_action(**resolved_config)
    #    else:
    #        self.logger.error(f"Plugin '{plugin_name}' not found")

    def run(self, **config: Dict[str, Any]):
        self.execute_hooks('pre', config)
        self.do_action(**config)
        self.execute_hooks('post', config)
