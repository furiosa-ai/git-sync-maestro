import logging
import sys

from .interface.context import ContextManager
from .utils.yaml_loader import load_config
from .workflow_runner import WorkflowContext, WorkflowRunner

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main(config_file):
    config = load_config(config_file)

    with ContextManager(WorkflowContext(config, inputs={})) as context:
        workflow_runner = WorkflowRunner.from_config(context, config)
        workflow_runner.run(config)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])
