# src/git_sync_maestro/plugins/bash_command.py
import io
import os
import shlex
import subprocess
from typing import Any, Dict

from ..core import BaseExecutor, register_plugin
from ..utils.pretty_print import pretty_print_env


@register_plugin("sh")
class BashCommandExecutor(BaseExecutor):
    def validate_config(self, config: Dict[str, Any]):
        if isinstance(config, dict):
            if self.get_config_param_key() not in config:
                raise ValueError(
                    f"Missing required configuration key: '{self.get_config_param_key()}'"
                )
            if 'shell' in config and not isinstance(config['shell'], str):
                raise ValueError("'shell' option must be a string")
        elif isinstance(config, str):
            # If config is a string, it's assumed to be the command itself
            pass
        else:
            raise ValueError("Invalid configuration type for run plugin")

    def get_config_param_key(self) -> str:
        return "run"

    def execute(self, **kwargs):
        command = kwargs[self.get_config_param_key()]
        working_dir = kwargs.get('working_dir', os.getcwd())
        shell = kwargs.get('shell', '/bin/bash')  # Default to /bin/sh if not specified

        env = os.environ.copy()
        env.update(self.context.get_accumulated_env())
        env.update(kwargs.get('envs', {}))

        # output = io.StringIO()
        # pretty_print_env(env, print_func=output.write, exclude_keys=["SECRET_KEY", "PASSWORD"])
        # self.logger.debug(f"Current environment:\n{output.getvalue()}")

        # Add context variables to environment
        for key, value in self.context.get_root()._resources.items():
            if isinstance(value, dict) and 'path' in value:
                env[f"CONTEXT_{key.upper()}_PATH"] = value['path']

        self.logger.info(f"Executing command: {command}")
        self.logger.info(f"Working directory: {working_dir}")
        self.logger.info(f"Using shell: {shell}")

        try:
            if kwargs.get('shell', True):  # Use shell by default
                # If shell is True, we pass the command as a string
                cmd = command
            else:
                # If shell is False, we need to split the command into a list
                cmd = shlex.split(command)

            result = subprocess.run(
                cmd,
                shell=kwargs.get('shell', True),
                executable=shell,
                check=True,
                cwd=working_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            self.logger.debug("Command output:")
            self.logger.debug(result.stdout)
            if result.stderr:
                self.logger.warning("Command error output:")
                self.logger.warning(result.stderr)

            # Store the output in the context for later use
            self.context.set_resource('last_command_output', result.stdout)
            self.context.set_resource('last_command_exit_code', result.returncode)

            return result.stdout

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with exit code {e.returncode}")
            self.logger.error("Command output:")
            self.logger.error(e.output)
            if e.stderr:
                self.logger.error("Command error output:")
                self.logger.error(e.stderr)

            # Store the error output and exit code in the context
            self.context.set_resource('last_command_error', e.stderr)
            self.context.set_resource('last_command_exit_code', e.returncode)

            raise

    def resolve_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(config, str):
            return {self.get_config_param_key(): self.context.resolve_value(config)}
        return super().resolve_config(config)
