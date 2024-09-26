# src/git_sync_maestro/main.py

import argparse
import logging

from .interface.context import ContextManager
from .utils.yaml_loader import load_config
from .workflow_runner import WorkflowContext, WorkflowRunner

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_input(s):
    if '=' in s:
        key, value = s.split('=', 1)
        return key, value
    else:
        raise argparse.ArgumentTypeError('Input must be in the format KEY=VALUE')


def parse_arguments():
    parser = argparse.ArgumentParser(description="Git Sync Maestro Workflow Runner")
    parser.add_argument("config_file", help="Path to the workflow configuration file")
    parser.add_argument(
        "--input",
        action="append",
        type=parse_input,
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
