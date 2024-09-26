from typing import Any, Dict

from ..interface.context import BaseContext


class ActionContext(BaseContext):
    def __init__(self, config: Dict[str, Any], context: BaseContext):
        super().__init__(config, context)
