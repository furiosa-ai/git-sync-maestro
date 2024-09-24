# src/git_sync_maestro/plugins/python_script.py

from io import StringIO
import os
import sys
import tempfile
from typing import Any, Dict

from ..core import BaseExecutor, register_plugin


@register_plugin("python")
class PythonExecutor(BaseExecutor):
    def validate_config(self, config: Dict[str, Any]):
        if isinstance(config, dict):
            if self.get_config_param_key() not in config:
                raise ValueError(
                    f"Missing required configuration key: '{self.get_config_param_key()}'"
                )
        elif isinstance(config, str):
            # If config is a string, it's assumed to be the Python script itself
            pass
        else:
            raise ValueError("Invalid configuration type for python plugin")

    def get_config_param_key(self) -> str:
        return "python"

    def execute(self, **kwargs):
        script = kwargs[self.get_config_param_key()]
        working_dir = kwargs.get('working_dir', os.getcwd())

        env = os.environ.copy()
        env.update(self.context.get_accumulated_env())
        env.update(kwargs.get('envs', {}))

        # Add context variables to environment
        for key, value in self.context.get_root()._resources.items():
            if isinstance(value, dict) and 'path' in value:
                env[f"CONTEXT_{key.upper()}_PATH"] = value['path']

        self.logger.info(f"Executing Python script")
        self.logger.info(f"Working directory: {working_dir}")

        try:
            # Create a temporary file to store the script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(script)
                temp_file_path = temp_file.name
                self.logger.debug(f"create python tempfile: {temp_file_path}")

            # Change the working directory
            original_dir = os.getcwd()
            self.logger.debug(f"set working dir: {working_dir}")
            os.chdir(working_dir)

            # Execute the script
            try:
                output = self._execute_script(temp_file_path, env)
                self.logger.debug("Script output:")
                self.logger.debug(output)

                # Store the output in the context for later use
                self.context.set_resource('last_python_output', output)
                self.context.set_resource('last_python_exit_code', 0)

                return output

            finally:
                # Change back to the original directory
                self.logger.debug(f"restored original dir: {original_dir}")
                os.chdir(original_dir)
                # Remove the temporary file
                self.logger.debug(f"deleted python tempfile: {temp_file_path}")
                os.unlink(temp_file_path)

        except Exception as e:
            self.logger.error(f"Python script execution failed: {str(e)}")

            # Store the error output and exit code in the context
            self.context.set_resource('last_python_error', str(e))
            self.context.set_resource('last_python_exit_code', 1)

            raise

    def _execute_script(self, script_path: str, env: Dict[str, str]) -> str:
        # Redirect stdout and stderr to capture output
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = sys.stderr = output = StringIO()

        try:
            # Execute the script
            with open(script_path, 'r') as file:
                exec(file.read(), {'__name__': '__main__'}, env)
            return output.getvalue()
        finally:
            # Restore original stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    def resolve_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(config, str):
            return {self.get_config_param_key(): self.context.resolve_value(config)}
        return super().resolve_config(config)
