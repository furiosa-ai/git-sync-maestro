# Git Sync Maestro

Git Sync Maestro is a powerful Python tool designed for efficient file and directory synchronization between multiple Git repositories. This project is maintained by Furiosa.ai.

## Key Features

- Synchronize files and directories across multiple Git repositories
- Support for glob patterns for fine-grained file selection
- File exclusion capabilities
- Custom command execution before and after synchronization
- Easy configuration using YAML

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

1. Create a YAML configuration file. Note that all paths in the YAML file are relative to the root of the cloned project:

```yaml
syncs:
  - repo1: "https://github.com/user/repo1.git"
    repo2: "https://github.com/user/repo2.git"
    pre: "echo 'Starting sync' && git checkout main"
    directories:
      - src: "src"
        dst: "dest/src"
        glob_pattern: "*.py"
        exclude_pattern: "test_*.py"
    files:
      - src: "config.toml"
        dst: "config/config.toml"
    post: "echo 'Sync completed' && npm run build"
```

2. Run the synchronization:

```bash
python -m git_sync_maestro path/to/your/config.yaml
```

## Configuration Options

All paths in the configuration are relative to the root of the cloned project.

- `repo1`, `repo2`: URLs of source and target Git repositories
- `pre`: Command to execute before synchronization (executed in the root of the cloned project)
- `directories`: List of directories to synchronize
  - `src`: Source directory path (relative to the root of repo1)
  - `dst`: Target directory path (relative to the root of repo2)
  - `glob_pattern`: Pattern for files to include
  - `exclude_pattern`: Pattern for files to exclude
- `files`: List of individual files to synchronize
  - `src`: Source file path (relative to the root of repo1)
  - `dst`: Target file path (relative to the root of repo2)
- `post`: Command to execute after synchronization (executed in the root of the cloned project)

## Example

Let's say you have the following structure in your source repository (repo1):

```
/
├── src/
│   ├── main.py
│   └── utils.py
├── config.toml
└── README.md
```

And you want to synchronize it with a target repository (repo2) with a different structure:

```
/
├── dest/
│   └── src/
├── config/
└── docs/
```

Your configuration might look like this:

```yaml
syncs:
  - repo1: "https://github.com/user/source-repo.git"
    repo2: "https://github.com/user/target-repo.git"
    directories:
      - src: "src"
        dst: "dest/src"
        glob_pattern: "*.py"
    files:
      - src: "config.toml"
        dst: "config/config.toml"
      - src: "README.md"
        dst: "docs/README.md"
```

This configuration will:
1. Synchronize all .py files from the `src` directory in repo1 to the `dest/src` directory in repo2.
2. Copy `config.toml` from the root of repo1 to the `config` directory in repo2.
3. Copy `README.md` from the root of repo1 to the `docs` directory in repo2.

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