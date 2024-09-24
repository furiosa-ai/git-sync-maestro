from typing import Any, Dict

from .base_executor import BaseExecutor
from .context import BaseContext


class Workflow:
    def __init__(self, context: BaseContext):
        self.context = context

    def run_steps(self, config: Dict[Any, Any]):
        steps = config.get("steps", [])
        for step in steps:
            name = step.get('name', 'Unnamed step')
            print(f"Executing step: {name}")
            result = self.executor.execute_step(step)
            print(f"Step result: {result}")
