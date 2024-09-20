import os

from git import Repo

from ..core import BasePlugin, register_plugin


@register_plugin("git_clone")
class GitClonePlugin(BasePlugin):
    def validate_config(self, config):
        required_keys = ['src_repo', 'clone_path']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")

    def do_action(self, **kwargs):
        resolved_kwargs = self.resolve_config(kwargs)
        repo_url = resolved_kwargs['src_repo']
        clone_path = resolved_kwargs['clone_path']
        resource_name = resolved_kwargs['resource_name']

        if not os.path.exists(clone_path):
            repo = Repo.clone_from(repo_url, clone_path)
        else:
            repo = Repo(clone_path)
            origin = repo.remotes.origin
            origin.pull()

        self.context.set_resource(resource_name, {'repo': repo, 'path': clone_path})
        print(f"Repository cloned/pulled at: {clone_path}")
        print(f"Set as resource: {resource_name}")
