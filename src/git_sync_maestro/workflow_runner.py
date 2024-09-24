import importlib
import logging
import sys
from typing import Any, Dict

from .core import BaseContext, ExecutorFactory
from .core.action_context import ActionContext
from .exceptions import ExecutionError
from .interface.context import ContextManager


class WorkflowContext(BaseContext):
    pass


class WorkflowRunner:
    def __init__(self, context: WorkflowContext, inputs: Dict[str, Any] = {}):
        self.context = context
        self.inputs = inputs
        self.logger = logging.getLogger(self.__class__.__name__)

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
        self.context.set_inputs(self.inputs)
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
                    # Optionally, you can choose to exit here if you want to stop on first error
                    sys.exit(1)

    def _determine_action_type(self, step: Dict[str, Any]) -> str:
        if 'run' in step:
            return 'sh'
        elif 'python' in step:
            return 'python'
        elif 'use' in step:
            return 'workflow'
        else:
            raise ValueError("Step must contain either 'run', 'python', or 'use'")
