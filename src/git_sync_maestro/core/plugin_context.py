from typing import Any, Dict

from ..interface.context import BaseContext
from .plugin_executor import PluginExecutor


class PluginContext(BaseContext):
    def __init__(self, config: Dict[str, Any]):
        self.plugin_executor = PluginExecutor(self)
        super().__init__(config)
