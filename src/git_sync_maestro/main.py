import argparse
import logging
import sys

from .interface.context import ContextManager
from .utils.yaml_loader import load_config
from .workflow_runner import WorkflowContext, WorkflowRunner

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Git Sync Maestro Workflow Runner")
    parser.add_argument("config_file", help="Path to the workflow configuration file")
    parser.add_argument(
        "--input",
        action="append",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Input key-value pairs for the workflow. Can be used multiple times.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    config_file = args.config_file
    logger.info(f"Start Workflow: [{config_file}]")
    config = load_config(config_file)
    input_dict = dict(args.input or [])

    with ContextManager(WorkflowContext(config, inputs=input_dict)) as context:
        workflow_runner = WorkflowRunner.from_config(context, config)
        workflow_runner.run(config)

    logger.info(f"Finished Workflow: [{config_file}]")


if __name__ == "__main__":
    main()
