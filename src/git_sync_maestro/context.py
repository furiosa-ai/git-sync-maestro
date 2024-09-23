import logging
import os
import re
from typing import Any, Dict


class Context:
    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._env: Dict[str, str] = {}
        self._resources: Dict[str, Any] = {}
        self._process_env_vars()
        self.logger = logging.getLogger(self.__class__.__name__)

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

    def resolve_value(self, value):
        if isinstance(value, str):
            # Resolve environment variables
            value = re.sub(r'\$\{([^}]+)\}', lambda m: self.get_env(m.group(1), m.group(0)), value)

            # Resolve context variables
            m = re.match(r'\$context\.([^}\s]+)', value)
            if m:
                value = self.get_resource(m.group(1), m.group(0))

        self.logger.debug(f"resolve_value: {value} => {value}")
        return value

    def get_config(self, key: str, default=None):
        return self._config.get(key, default)

    def get_env(self, key: str, default=None) -> str:
        return self._env.get(key, default)

    def set_resource(self, key: str, value: Any):
        self._resources[key] = value

    def get_resource(self, key: str, default=None):
        return self._resources.get(key, default)
