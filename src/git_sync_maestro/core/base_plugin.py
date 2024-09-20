from abc import ABC, abstractmethod
from typing import Any, Dict

from ..context import Context


class BasePlugin(ABC):
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def do_action(self, context: Context, **kwargs):
        """
        Abstract method that all plugins must implement.
        This method should contain the main logic for the synchronization task.

        :param kwargs: Keyword arguments specific to the plugin
        """
        pass

    def resolve_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {k: self.context.resolve_value(v) for k, v in config.items()}

    def validate_config(self, config):
        """
        Optional method to validate the configuration for this plugin.
        Subclasses can override this method to add custom validation logic.

        :param config: Configuration dictionary for the plugin
        :raises ValueError: If the configuration is invalid
        """
        pass

    def pre_action(self, **kwargs):
        """
        Optional method to perform any setup before the sync operation.
        Subclasses can override this method if needed.

        :param kwargs: Keyword arguments specific to the plugin
        """
        pass

    def post_action(self, **kwargs):
        """
        Optional method to perform any cleanup after the sync operation.
        Subclasses can override this method if needed.

        :param kwargs: Keyword arguments specific to the plugin
        """
        pass
