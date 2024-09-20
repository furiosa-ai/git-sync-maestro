import importlib
import sys

import yaml

from .context import Context
from .core import PluginRegistry


def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)


def load_plugins(plugins):
    for plugin in plugins:
        try:
            module_name, class_name = plugin.rsplit('.', 1)
            print(f"load plugin: from {module_name} import {class_name}")
            module = importlib.import_module(module_name)

            getattr(module, class_name)  # This will trigger the decorator
        except (ImportError, AttributeError) as e:
            print(f"Error loading plugin {plugin}: {str(e)}")


def main(config_file):
    config = load_config(config_file)

    load_plugins(config.get('plugins', []))

    with Context(config) as context:
        for sync_config in config.get('body', []):
            for plugin_name, plugin_config in sync_config.items():
                try:
                    plugin_class = PluginRegistry.get(plugin_name)
                    plugin = plugin_class(context)
                    plugin.validate_config(plugin_config)
                    plugin.do_action(**plugin_config)
                except Exception as e:
                    print(f"[{plugin_name}] Error: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])
