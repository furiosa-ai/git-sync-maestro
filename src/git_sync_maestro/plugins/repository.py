import os
import subprocess
from typing import Dict

from git import Repo

from .dir_sync import sync_directory
from .file_sync import sync_file


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


def clone_or_pull_repo(repo_url: str, local_path: str) -> Repo:
    """Git 저장소를 클론하거나 풀합니다."""
    if os.path.exists(local_path):
        repo = Repo(local_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        repo = Repo.clone_from(repo_url, local_path)
    return repo


def commit_and_push(repo: Repo, message: str):
    """변경사항을 커밋하고 푸시합니다."""
    repo.git.add(A=True)
    if repo.index.diff('HEAD'):
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        origin.push()
        print(f"변경사항 푸시 완료: {repo.working_dir}")
    else:
        print(f"변경사항 없음: {repo.working_dir}")


def sync_repositories(config: Dict):
    """설정에 따라 Git 저장소들을 동기화합니다."""
    for sync in config['syncs']:
        repo1_url = sync.get('repo1', '')
        repo2_url = sync.get('repo2', '')

        repo1_path = f"./temp_repo1_{os.path.basename(repo1_url)}"
        repo2_path = f"./temp_repo2_{os.path.basename(repo2_url)}"

        repo1 = clone_or_pull_repo(repo1_url, repo1_path)
        repo2 = clone_or_pull_repo(repo2_url, repo2_path)

        # Pre 명령어 실행
        if 'pre' in sync:
            run_command(repo2_path, sync['pre'], "Pre-sync")

        if 'directories' in sync:
            for directory in sync['directories']:
                src_dir = directory.get('src', '')
                dst_dir = directory.get('dst', '')
                glob_pattern = directory.get('glob_pattern', '*')
                exclude_pattern = directory.get('exclude_pattern', '')

                print(
                    f"\n{repo1_url}의 {src_dir}에서 {repo2_url}의 {dst_dir}로 디렉토리 동기화 시작"
                )
                sync_directory(repo1, repo2, src_dir, dst_dir, glob_pattern, exclude_pattern)

        if 'files' in sync:
            for file_sync in sync['files']:
                src_file = file_sync.get('src', '')
                dst_file = file_sync.get('dst', '')

                print(f"\n{repo1_url}의 {src_file}에서 {repo2_url}의 {dst_file}로 파일 동기화 시작")
                sync_file(repo1, repo2, src_file, dst_file)

        commit_and_push(repo2, f"Automated sync update from {repo1_url}")

        # Post 명령어 실행
        if 'post' in sync:
            run_command(repo2_path, sync['post'], "Post-sync")

        print(f"\n{repo1_url}에서 {repo2_url}로 동기화 완료\n")
