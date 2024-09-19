import subprocess
import sys
from typing import Dict

import yaml

from .sync.repository import sync_repositories


def run_command(repo_path: str, command: str, command_type: str):
    """주어진 명령어를 실행합니다."""
    try:
        result = subprocess.run(
            command, shell=True, cwd=repo_path, check=True, capture_output=True, text=True
        )
        print(f"{command_type} 명령어 실행 완료: {command}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"{command_type} 명령어 실행 실패: {command}")
        print(e.stderr)


def load_sync_config(config_file: str) -> Dict:
    """YAML 설정 파일을 로드합니다."""
    with open(config_file, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m git_sync_maestro <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_sync_config(config_file)
    sync_repositories(config)


if __name__ == "__main__":
    main()
