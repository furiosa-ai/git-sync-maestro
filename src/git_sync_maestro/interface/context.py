import logging
import os
import re
from typing import Any, Dict, List, Optional


class BaseContext:
    def __init__(self, config: Dict[str, Any], parent: Optional['BaseContext'] = None):
        self._config = config
        self._env: Dict[str, str] = {}
        self._process_env_vars()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.parent = parent
        self.action_name: Optional[str] = None
        self.action_line: Optional[int] = None
        if parent is None:
            # Only root context has _resources
            self._resources: Dict[str, Any] = {}

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def get_root(self) -> 'BaseContext':
        current = self
        while current.parent:
            current = current.parent
        return current

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _process_env_vars(self):
        for item in self._config.get('env', []):
            for key, value in item.items():
                if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                    env_var = value[2:-1]
                    default_value = None
                    if ':-' in env_var:
                        env_var, default_value = env_var.split(':-')
                    self._env[key] = os.environ.get(env_var, default_value)
                else:
                    self._env[key] = value

    def _resolve_env_var(self, value):
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            default_value = None
            if ':-' in env_var:
                env_var, default_value = env_var.split(':-')
            return os.environ.get(env_var, default_value)
        return value

    def resolve_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self._resolve_string(value)
        elif isinstance(value, dict):
            return self._resolve_dict(value)
        elif isinstance(value, list):
            return self._resolve_list(value)
        else:
            return value

    def _resolve_string(self, value: str) -> str:
        old_value = value

        # Resolve environment variables
        value = re.sub(
            r'\$\[([^]\s]+)\]', lambda m: self.get_env(m.group(1), default=m.group(0)), value
        )

        # Resolve context variables
        match = re.match(r'\$\[context\.([^]\s]+)\]', value)
        if match:
            value = self.get_resource(match.group(1), match.group(0))

        if value != old_value:
            self.logger.debug(f"Resolved string: '{old_value}' => '{value}'")

        return value

    def _resolve_dict(self, value: Dict[Any, Any]) -> Dict[Any, Any]:
        resolved_dict = {}
        for k, v in value.items():
            resolved_value = self.resolve_value(v)
            resolved_dict[k] = resolved_value
            if v != resolved_value:
                self.logger.debug(f"Resolved dict item: {{{k}: {v}}} => {{{k}: {resolved_value}}}")
        return resolved_dict

    def _resolve_list(self, value: List[Any]) -> List[Any]:
        resolved_list = []
        for item in value:
            resolved_item = self.resolve_value(item)
            resolved_list.append(resolved_item)
            if item != resolved_item:
                self.logger.debug(f"Resolved list item: {item} => {resolved_item}")
        return resolved_list

    def get_config(self, key: str, default: Any = None) -> Any:
        value = self._config.get(key, None)
        if value is None and self.parent:
            return self.parent.get_config(key, default)
        return value if value is not None else default

    def get_env(self, key: str, default: str = None) -> str:
        value = self._env.get(key, None)
        if value is None and self.parent:
            return self.parent.get_env(key, default)
        return value if value is not None else default

    def get_resource(self, key: str, default: Any = None) -> Any:
        root = self.get_root()
        return root._resources.get(key, default)

    def set_resource(self, key: str, value: Any):
        root = self.get_root()
        root._resources[key] = value

    def set_action_info(self, name: str, line: int):
        self.action_name = name
        self.action_line = line

    def get_action_info(self) -> tuple:
        return self.action_name, self.action_line

    def push(self, config: Dict[str, Any]) -> 'BaseContext':
        return BaseContext(config, self)

    def pop(self) -> Optional['BaseContext']:
        return self.parent


class ContextManager:
    def __init__(self, context: BaseContext):
        self.context = context

    def __enter__(self) -> BaseContext:
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.context.parent:
            self.context = self.context.parent
