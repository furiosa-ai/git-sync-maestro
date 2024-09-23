import importlib
import logging
import sys

import yaml
from yaml.loader import SafeLoader

from .context import Context
from .core import PluginRegistry

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LineNumberLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        # Add 1 to line number because line numbers start at 0
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.load(file, Loader=LineNumberLoader)


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
        for index, action in enumerate(config.get('body', []), start=1):
            action_name = action.get('name', f"Action-{index}")
            action_line = action.get('__line__', 'Unknown')
            action_type, action_config = next(iter(action.items()))
            if action_type == 'name':
                action_type, action_config = next(iter(action_config.items()))

            logger.info(f"Executing {action_name} (line {action_line}): {action_type}")
            try:
                plugin_class = PluginRegistry.get(action_type)
                if plugin_class:
                    breakpoint()
                    plugin = plugin_class(context)
                    resolved_config = plugin.resolve_config(action_config)
                    plugin.validate_config(resolved_config)
                    plugin.run(**resolved_config)
                else:
                    logger.error(
                        f"{action_name} (line {action_line}): Plugin '{action_type}' not found"
                    )
            except Exception as e:
                logger.exception(f"Error in {action_name} (line {action_line}): {str(e)}")
                # Optionally, you can choose to exit here if you want to stop on first error
                sys.exit(1)
            logger.info(f"Completed {action_name} (line {action_line})")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])
