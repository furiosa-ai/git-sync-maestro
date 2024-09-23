# src/git_sync_maestro/plugins/bash_command.py

import os
import subprocess

from ..core import BasePlugin, register_plugin


@register_plugin("sh")
class BashCommandPlugin(BasePlugin):
    def validate_config(self, config):
        if isinstance(config, dict):
            if self.get_plugin_param_key() not in config:
                raise ValueError(
                    f"Missing required configuration key: '{self.get_plugin_param_key()}'"
                )
        else:
            raise ValueError("Invalid configuration type for sh plugin")

    def get_plugin_param_key(self) -> str:
        return "command"

    def do_action(self, **kwargs):
        command = kwargs[self.get_plugin_param_key()]
        working_dir = kwargs.get('working_dir', os.getcwd())

        env = os.environ.copy()

        # Add context variables to environment
        for key, value in self.context._resources.items():
            if isinstance(value, dict) and 'path' in value:
                env[f"CONTEXT_{key.upper()}_PATH"] = value['path']

        self.logger.info(f"Executing command: {command}")
        self.logger.info(f"Working directory: {working_dir}")

        try:
            result = subprocess.run(
                command,
                shell=True,
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

            # Optionally, you can store the output in the context for later use
            self.context.set_resource('last_command_output', result.stdout)

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with exit code {e.returncode}")
            self.logger.error("Command output:")
            self.logger.error(e.output)
            if e.stderr:
                self.logger.error("Command error output:")
                self.logger.error(e.stderr)
            raise
