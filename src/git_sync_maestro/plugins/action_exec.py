# src/git_sync_maestro/plugins/action_exec.py

from typing import Any, Dict

from ..core import BaseExecutor, register_plugin
from ..exceptions import ActionExecutionError
from ..interface.context import ContextManager
from ..utils.yaml_loader import load_config
from ..workflow_runner import WorkflowContext, WorkflowRunner


@register_plugin("workflow")
class ActionExecutor(BaseExecutor):
    def validate_config(self, config: Dict[str, Any]):
        if not isinstance(config, dict):
            raise ValueError("Use configuration must be a dictionary")
        if 'use' not in config:
            raise ValueError("Use configuration must include a 'use' key")

    def get_config_param_key(self) -> str:
        return "use"

    def execute(self, **kwargs):
        workflow_path = kwargs[self.get_config_param_key()]
        inputs = kwargs.get('inputs', {})

        self.logger.info(f"Executing workflow: {workflow_path}")
        self.logger.debug(f"Workflow inputs: {inputs}")

        try:
            # Create a new context for this workflow execution
            config = load_config(workflow_path)
            with ContextManager(WorkflowContext(config, self.context)) as context:
                # Create a new WorkflowRunner with the workflow context
                runner = WorkflowRunner(context, inputs=inputs)

                # Run the workflow
                result = runner.run(config)

                self.logger.info(f"Workflow execution completed successfully")
                return result

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {str(e)}")
            raise ActionExecutionError(f"Failed to execute workflow: {str(e)}")

        finally:
            # Make sure to pop the context even if an exception occurs
            self.context.pop()

    def resolve_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        resolved_config = super().resolve_config(config)

        # Resolve the workflow path
        workflow_path = resolved_config[self.get_config_param_key()]
        resolved_config[self.get_config_param_key()] = self.context.resolve_value(workflow_path)

        # Resolve input values
        if 'inputs' in resolved_config:
            resolved_config['inputs'] = self.context.resolve_value(resolved_config['inputs'])

        return resolved_config
