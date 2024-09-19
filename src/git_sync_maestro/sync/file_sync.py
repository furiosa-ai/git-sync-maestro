import os
import shutil

from git import Repo


def sync_file(repo1: Repo, repo2: Repo, src_file: str, dst_file: str):
    """두 저장소 간에 특정 파일을 동기화합니다."""
    src_path = os.path.join(repo1.working_dir, src_file)
    dst_path = os.path.join(repo2.working_dir, dst_file)

    if not os.path.exists(src_path):
        print(f"경고: 소스 파일을 찾을 수 없음: {src_path}")
        return

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f"파일 동기화: {src_file} -> {dst_file}")
