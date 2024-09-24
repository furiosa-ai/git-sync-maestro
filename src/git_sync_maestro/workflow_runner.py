import importlib
import logging
import sys
from typing import Any, Dict, List, Optional

from .core import BaseContext, ExecutorFactory
from .core.action_context import ActionContext
from .exceptions import ExecutionError, WorkflowValidationError
from .interface.context import ContextManager


class WorkflowContext(BaseContext):
    def __init__(
        self, config: Dict[str, Any], inputs: Dict[str, Any], parent: Optional['BaseContext'] = None
    ):
        super().__init__(config, parent)
        self.set_inputs(inputs)


class WorkflowRunner:
    logger = logging.getLogger(__name__)

    def __init__(self, context: WorkflowContext):
        self.context = context
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def from_config(context: WorkflowContext, config: Dict[Any, Any]) -> 'WorkflowRunner':
        WorkflowRunner.validate_inputs(context, config.get("inputs", []))
        runner = WorkflowRunner(context)
        runner.logger = WorkflowRunner.logger
        return runner

    @staticmethod
    def validate_inputs(context, required_inputs):
        provided_inputs = context.get_inputs()

        missing_inputs = [
            input_name for input_name in required_inputs if input_name not in provided_inputs
        ]

        if missing_inputs:
            raise WorkflowValidationError(f"Missing required inputs: {', '.join(missing_inputs)}")

        WorkflowRunner.logger.info(
            f"Inputs validated successfully. Required inputs: {required_inputs}"
        )
        WorkflowRunner.logger.debug(f"Provided inputs: {provided_inputs}")

    def load_plugins(self, plugins):
        for plugin in plugins:
            try:
                module_name, class_name = plugin.rsplit('.', 1)
                print(f"load plugin: from {module_name} import {class_name}")
                module = importlib.import_module(module_name)

                getattr(module, class_name)  # This will trigger the decorator
            except (ImportError, AttributeError) as e:
                print(f"Error loading plugin {plugin}: {str(e)}")

    def run(self, config: Dict[Any, Any]):
        self.load_plugins(config.get('plugins', []))
        self.run_steps(config)

    def run_steps(self, config: Dict[Any, Any]):
        steps = config.get("steps", [])
        for index, action in enumerate(steps):
            with ContextManager(ActionContext(action, self.context)) as context:
                action_name = action.get('name', f"Action-{index}")
                action_line = action.get('__line__', 'Unknown')
                context.set_action_info(action_name, action_line)

                print(f"Executing step: {action_name}@{action_line}")
                action_type = self._determine_action_type(action)
                executor = ExecutorFactory(context)
                try:
                    result = executor(action_type, action)
                    self.logger.info(f"Completed {action_name} (line {action_line})")
                except ExecutionError as e:
                    self.logger.exception(
                        f"Error in {e.action_name} (line {e.action_line}): {str(e.original_error)}"
                    )
                    # Consider making this configurable
                    raise  # Re-raise the exception instead of calling sys.exit()

    def _determine_action_type(self, step: Dict[str, Any]) -> str:
        if 'run' in step:
            return 'sh'
        elif 'python' in step:
            return 'python'
        elif 'use' in step:
            return 'workflow'
        else:
            raise ValueError("Step must contain either 'run', 'python', or 'use'")
