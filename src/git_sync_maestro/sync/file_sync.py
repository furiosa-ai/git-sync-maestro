import os
import shutil

from git import Repo
from git_sync_maestro.plugin import BasePlugin, register_plugin


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

        repo = self.context.get_resource('src_repo')

        # Perform file synchronization
        src_path = src
        dst_path = dst

        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)

        # Commit
        repo.git.add(dst)
        repo.index.commit(f"Sync file from {src} to {dst}")

        print(f"File synced from {src} to {dst} in repository")
