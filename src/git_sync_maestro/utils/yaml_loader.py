import yaml
from yaml.loader import SafeLoader


class LineNumberLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        # Add 1 to line number because line numbers start at 0
        mapping['__line__'] = str(node.start_mark.line + 1)
        return mapping


def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.load(file, Loader=LineNumberLoader)
