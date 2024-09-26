from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, Union

from .context import BaseContext, ContextManager


class BaseExecutor(ABC):
    def __init__(self, context: BaseContext):
        self.context = context
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

    def resolve_config(self, config: Union[Dict[str, Any], str]) -> Union[Dict[str, Any], str]:
        if isinstance(config, str):
            key = self.get_config_param_key()
            return {key: self.context.resolve_value(config)}
        return {k: self.context.resolve_value(v) for k, v in config.items()}

    def validate_config(self, config: Dict[str, Any]):
        # Implement default validation logic here
        pass

    def get_config_param_key(self) -> str:
        # Implement logic to get the main parameter key for this executor
        pass

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
                context.plugin_executor(plugin_name, plugin_config)

    def run(self, **config) -> Any:
        self.execute_hooks('pre', config)
        result = self.execute(**config)
        self.execute_hooks('post', config)
        return result
