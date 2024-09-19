# Git Sync Maestro

Git Sync Maestro is a powerful Python tool designed for efficient file and directory synchronization between multiple Git repositories.

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
git clone https://github.com/furiosa.ai/git-sync-maestro.git
cd git-sync-maestro
pip install -e .
```

## Usage

1. Create a YAML configuration file:

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

- `repo1`, `repo2`: URLs of source and target Git repositories
- `pre`: Command to execute before synchronization
- `directories`: List of directories to synchronize
  - `src`: Source directory path
  - `dst`: Target directory path
  - `glob_pattern`: Pattern for files to include
  - `exclude_pattern`: Pattern for files to exclude
- `files`: List of individual files to synchronize
  - `src`: Source file path
  - `dst`: Target file path
- `post`: Command to execute after synchronization

## Contributing

Interested in contributing to the project? Great! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.


## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.