# src/git_sync_maestro/plugins/bash_command.py

import os
import subprocess

from ..core import BasePlugin, register_plugin


@register_plugin("sh")
class BashCommandPlugin(BasePlugin):
    def validate_config(self, config):
        if 'command' not in config:
            raise ValueError("Missing required configuration key: 'command'")

    def do_action(self, **kwargs):
        resolved_kwargs = self.resolve_config(kwargs)
        command = resolved_kwargs['command']
        working_dir = resolved_kwargs.get('working_dir', os.getcwd())
        env = os.environ.copy()

        # Add context variables to environment
        for key, value in self.context._resources.items():
            if isinstance(value, dict) and 'path' in value:
                env[f"CONTEXT_{key.upper()}_PATH"] = value['path']

        print(f"Executing command: {command}")
        print(f"Working directory: {working_dir}")

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
            print("Command output:")
            print(result.stdout)
            if result.stderr:
                print("Command error output:")
                print(result.stderr)

            # Optionally, you can store the output in the context for later use
            self.context.set_resource('last_command_output', result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print("Command output:")
            print(e.output)
            if e.stderr:
                print("Command error output:")
                print(e.stderr)
            raise
