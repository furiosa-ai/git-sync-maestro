# Git Sync Maestro

Git Sync Maestro is a powerful and flexible workflow automation tool designed to synchronize and manage Git repositories. It allows you to define complex workflows using a simple YAML configuration, making it easy to automate your Git-related tasks.

## Features

- **Workflow-based Execution**: Define your tasks in YAML format for easy understanding and maintenance.
- **Plugin System**: Extend functionality with custom plugins.
- **Flexible Input Handling**: Pass inputs to your workflows for dynamic execution.
- **Bash and Python Script Support**: Run both shell commands and Python scripts within your workflows.
- **Nested Workflow Execution**: Call other workflows from within a workflow.
- **Robust Error Handling**: Comprehensive error catching and reporting.

## Installation

To install Git Sync Maestro, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/git-sync-maestro.git
   ```

2. Navigate to the project directory:
   ```
   cd git-sync-maestro
   ```

3. Install the package:
   ```
   pip install .
   ```

## Usage

1. Create a YAML file defining your workflow. For example, `my_workflow.yaml`:

   ```yaml
   plugins:
     - git_sync_maestro.plugins.bash_command.BashCommandExecutor
     - git_sync_maestro.plugins.python_exec.PythonExecutor

   inputs:
     - REPO_URL
     - BRANCH_NAME

   steps:
     - name: "Clone repository"
       run: git clone $[inputs.REPO_URL] repo

     - name: "Checkout branch"
       run: |
         cd repo
         git checkout $[inputs.BRANCH_NAME]

     - name: "Run Python script"
       python: |
         import os
         print(f"Current directory: {os.getcwd()}")
         print(f"Files in repo: {os.listdir('repo')}")
   ```

2. Run the workflow using the command-line interface:

   ```
   git-sync-maestro run my_workflow.yaml --input REPO_URL=https://github.com/example/repo.git --input BRANCH_NAME=main --input VAR1="this is var1"
   ```

## Creating Custom Plugins

You can extend Git Sync Maestro's functionality by creating custom plugins. Here's a basic example:

```python
from git_sync_maestro.core import BaseExecutor, register_plugin

@register_plugin("my_custom_action")
class MyCustomExecutor(BaseExecutor):
    def execute(self, **kwargs):
        # Your custom logic here
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.