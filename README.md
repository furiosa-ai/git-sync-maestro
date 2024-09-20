# Git Sync Maestro

Git Sync Maestro is a powerful tool designed for efficient file and directory synchronization between multiple Git repositories. This project is maintained by Furiosa.ai.

## Key Features

- Plugin-based architecture for flexible and extensible synchronization tasks
- Built-in plugins for common operations (e.g., repo sync, file sync)
- YAML-based configuration for easy orchestration of multiple synchronization actions
- Makefile-style environment variable support with default values
- Easy creation and integration of custom plugins

## Installation

To install Git Sync Maestro, run the following command:

```bash
pip install git-sync-maestro
```

For the development version:

```bash
git clone https://github.com/furiosa-ai/git-sync-maestro.git
cd git-sync-maestro
pip install -e .
```

## Usage

1. Create a YAML configuration file. This file orchestrates the execution of various plugins:

```yaml
env:
  GITHUB_TOKEN: ${GITHUB_TOKEN:-default_token}
  API_KEY: ${API_KEY:-default_key}
  DEBUG_MODE: ${DEBUG_MODE:-false}

syncs:
  - repo:
      src: "https://${GITHUB_TOKEN}@github.com/user/repo1.git"
      dst: "https://${GITHUB_TOKEN}@github.com/user/repo2.git"
      src_branch: main
      dst_branch: sync
  - file:
      src: "config.toml"
      dst: "config/config.toml"
      repo: "https://${GITHUB_TOKEN}@github.com/user/repo2.git"
```

2. (Optional) Set your environment variables:

```bash
export GITHUB_TOKEN=your_github_token
export API_KEY=your_api_key
export DEBUG_MODE=true
```

3. Run the synchronization:

```bash
python -m git_sync_maestro path/to/your/config.yaml
```

## Configuration Options

- `env`: Dictionary of environment variables with default values
  - `KEY: ${ENVIRONMENT_VARIABLE:-default_value}`
- `syncs`: List of synchronization actions to perform
  - Each action specifies a plugin to use and its parameters

## Built-in Plugins

### repo
Synchronizes two Git repositories.
Parameters:
- `src`: Source repository URL
- `dst`: Destination repository URL
- `src_branch`: Source branch (optional, default: main)
- `dst_branch`: Destination branch (optional, default: main)

### file
Synchronizes a single file between repositories.
Parameters:
- `src`: Source file path
- `dst`: Destination file path
- `repo`: Repository URL

## Creating Custom Plugins

To create a custom plugin for Git Sync Maestro:

1. Create a new Python file in the `plugins` directory (e.g., `custom_sync.py`).
2. Define a class that inherits from `BasePlugin`.
3. Implement the `sync` method.
4. Use the `@register_plugin` decorator to register your plugin.

Here's an example of a custom plugin:

```python
from git_sync_maestro.plugin import BasePlugin, register_plugin

@register_plugin("custom_sync")
class CustomSyncPlugin(BasePlugin):
    def sync(self, **kwargs):
        # Your custom synchronization logic here
        src = kwargs.get('src')
        dst = kwargs.get('dst')
        print(f"Performing custom sync from {src} to {dst}")
        # Implement your sync logic
```

## Using Custom Plugins

Once you've created a custom plugin, you can use it in your YAML configuration file:

```yaml
syncs:
  - custom_sync:
      src: "/path/to/source"
      dst: "/path/to/destination"
      custom_param: "value"
```

## Environment Variables

Environment variables in Git Sync Maestro are handled in a Makefile-like manner. You can specify default values in the configuration file, which will be used if the corresponding environment variable is not set.

The syntax for specifying an environment variable with a default value is:

```yaml
KEY: ${ENVIRONMENT_VARIABLE:-default_value}
```

This approach allows you to:
- Provide default values for all required variables
- Override these defaults by setting environment variables when needed
- Keep sensitive information out of your configuration files

## Example

Here's a comprehensive example using multiple plugins, including a custom one:

```yaml
env:
  GITHUB_TOKEN: ${GITHUB_TOKEN:-default_token}
  API_KEY: ${API_KEY:-default_key}
  DEBUG_MODE: ${DEBUG_MODE:-false}

syncs:
  - repo:
      src: "https://${GITHUB_TOKEN}@github.com/user/source-repo.git"
      dst: "https://${GITHUB_TOKEN}@github.com/user/target-repo.git"
      src_branch: develop
      dst_branch: sync-branch
  - file:
      src: "config.toml"
      dst: "config/production-config.toml"
      repo: "https://${GITHUB_TOKEN}@github.com/user/target-repo.git"
  - custom_sync:
      src: "/path/to/source"
      dst: "/path/to/destination"
      custom_param: "value"
```

This configuration demonstrates:
1. Using the `repo` plugin to synchronize entire repositories
2. Using the `file` plugin to sync a specific file
3. Using a custom `custom_sync` plugin, showing the extensibility of the system

## Contributing

Interested in contributing to the project? Great! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

For more details, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## About Furiosa.ai

Git Sync Maestro is maintained by [Furiosa.ai](https://furiosa.ai/), a leading AI semiconductor company. For more information about Furiosa.ai and our other projects, please visit our website.