import fnmatch
import os
import shutil

from git import Repo


def should_include_file(file_path: str, glob_pattern: str, exclude_pattern: str) -> bool:
    """파일이 동기화에 포함되어야 하는지 확인합니다."""
    return fnmatch.fnmatch(file_path, glob_pattern) and not fnmatch.fnmatch(
        file_path, exclude_pattern
    )


def sync_directory(
    repo1: Repo, repo2: Repo, src_dir: str, dst_dir: str, glob_pattern: str, exclude_pattern: str
):
    """두 저장소의 특정 디렉토리 간에 파일을 동기화합니다."""
    src_path = os.path.join(repo1.working_dir, src_dir)
    dst_path = os.path.join(repo2.working_dir, dst_dir)

    if not os.path.exists(src_path):
        print(f"경고: 소스 디렉토리를 찾을 수 없음: {src_path}")
        return

    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    for root, _, files in os.walk(src_path):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_path)

            if should_include_file(rel_path, glob_pattern, exclude_pattern):
                dst_file = os.path.join(dst_path, rel_path)

                if os.path.exists(dst_file):
                    if os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                        shutil.copy2(src_file, dst_file)
                        print(f"파일 업데이트: {rel_path} (src -> dst)")
                else:
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    print(f"파일 추가: {rel_path} (src -> dst)")

    # 대상 디렉토리에 있지만 소스 디렉토리에 없는 파일 삭제
    for root, _, files in os.walk(dst_path):
        for file in files:
            dst_file = os.path.join(root, file)
            rel_path = os.path.relpath(dst_file, dst_path)
            src_file = os.path.join(src_path, rel_path)

            if not os.path.exists(src_file) and should_include_file(
                rel_path, glob_pattern, exclude_pattern
            ):
                os.remove(dst_file)
                print(f"파일 삭제: {rel_path} (dst)")
