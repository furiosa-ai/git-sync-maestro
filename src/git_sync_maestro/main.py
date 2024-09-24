import logging
import sys

import yaml
from yaml.loader import SafeLoader

from .interface.context import ContextManager
from .workflow_runner import WorkflowContext, WorkflowRunner

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LineNumberLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        # Add 1 to line number because line numbers start at 0
        mapping['__line__'] = str(node.start_mark.line + 1)
        return mapping


def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.load(file, Loader=LineNumberLoader)


def main(config_file):
    config = load_config(config_file)

    with ContextManager(WorkflowContext(config)) as context:
        workflow_runner = WorkflowRunner(context)
        workflow_runner.run(config)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])
