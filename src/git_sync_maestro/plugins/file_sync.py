import os
import shutil

from ..core import BasePlugin, register_plugin


@register_plugin("file_sync")
class FileSyncPlugin(BasePlugin):
    def validate_config(self, config):
        required_keys = ['src', 'dst']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")

    def do_action(self, **kwargs):
        src = kwargs['src']
        dst = kwargs['dst']
        src_root_path = kwargs['src_resource']['path']
        dst_root_path = kwargs['dst_resource']['path']
        dst_repo = kwargs['dst_resource']['repo']

        # Perform file synchronization
        src_path = os.path.join(src_root_path, src)
        dst_path = os.path.join(dst_root_path, dst)

        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)

        # Commit
        with dst_repo.git.custom_environment(GIT_WORK_TREE=dst_repo.working_dir):
            dst_repo.git.add(dst)
            dst_repo.index.commit(f"Sync file from {src} to {dst}")

        self.logger.info(f"File synced from {src_path} to {dst_path}")
