from typing import Dict, Type

from ..interface.base_plugin import BasePlugin


class PluginRegistry:
    _plugins: Dict[str, Type[BasePlugin]] = {}

    @classmethod
    def register(cls, name: str, plugin: Type[BasePlugin]):
        """
        Register a plugin with the given name.

        :param name: Name of the plugin
        :param plugin: Plugin class
        :raises ValueError: If a plugin with the same name is already registered
        """
        if name in cls._plugins:
            raise ValueError(f"Plugin '{name}' is already registered")
        cls._plugins[name] = plugin

    @classmethod
    def get(cls, name: str) -> Type[BasePlugin]:
        """
        Get a plugin by name.

        :param name: Name of the plugin
        :return: Plugin class
        :raises KeyError: If the plugin is not found
        """
        if name not in cls._plugins:
            raise KeyError(f"Plugin '{name}' is not registered")
        return cls._plugins[name]

    @classmethod
    def list(cls) -> Dict[str, Type[BasePlugin]]:
        """
        Get a dictionary of all registered plugins.

        :return: Dictionary of plugin names and their classes
        """
        return cls._plugins.copy()


def register_plugin(name: str):
    def decorator(cls):
        if not issubclass(cls, BasePlugin):
            raise TypeError(f"Plugin class {cls.__name__} must inherit from BasePlugin")
        PluginRegistry.register(name, cls)
        return cls

    return decorator
