import os
from typing import Any, Dict

from git import Repo


class Context:
    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._env = {}
        self._resources = {}
        self._process_env_vars()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _process_env_vars(self):
        for item in self._config.get('env', []):
            for key, value in item.items():
                if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                    env_var = value[2:-1]
                    default_value = None
                    if ':-' in env_var:
                        env_var, default_value = env_var.split(':-')
                    self._env[key] = os.environ.get(env_var, default_value)
                else:
                    self._env[key] = value

    def get_config(self, key: str, default=None):
        return self._config.get(key, default)

    def get_env(self, key: str, default=None):
        return self._env.get(key, default)

    def set_resource(self, key: str, value: Any):
        self._resources[key] = value

    def get_resource(self, key: str, default=None):
        return self._resources.get(key, default)

    def setup_repo(self):
        repo_url = self.get_config('repo')
        if repo_url:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            local_path = f"./temp/{repo_name}"
            if os.path.exists(local_path):
                repo = Repo(local_path)
                origin = repo.remotes.origin
                origin.pull()
            else:
                repo = Repo.clone_from(repo_url, local_path)
            self.set_resource('repo', repo)
            self.set_resource('repo_path', local_path)

    def cleanup(self):
        repo = self.get_resource('repo')
        if repo and repo.is_dirty():
            repo.git.add(A=True)
            repo.index.commit("Sync changes")
            repo.remote().push()
