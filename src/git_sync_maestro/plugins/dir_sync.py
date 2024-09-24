import fnmatch
import os
import re
import shutil
from typing import Any, Dict, List, Union

from ..core import BasePlugin, register_plugin


@register_plugin("dir_sync")
class DirSyncPlugin(BasePlugin):
    def validate_config(self, config: Dict[str, Any]):
        required_keys = ['src_dir', 'dst_dir']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: '{key}'")

    def do_action(self, **kwargs):
        src_dir = kwargs['src_dir']
        dst_dir = kwargs['dst_dir']
        include_patterns = self._normalize_patterns(kwargs.get('include_pattern', ['*']))
        exclude_patterns = self._normalize_patterns(kwargs.get('exclude_pattern', []))

        self.logger.info(f"Syncing directory from {src_dir} to {dst_dir}")
        self.logger.info(f"Include patterns: {include_patterns}")
        self.logger.info(f"Exclude patterns: {exclude_patterns}")

        for root, dirs, files in os.walk(src_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_dir)
                dst_path = os.path.join(dst_dir, rel_path)

                if self._should_include_file(rel_path, include_patterns, exclude_patterns):
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    if not os.path.exists(dst_path) or os.path.getmtime(
                        src_path
                    ) > os.path.getmtime(dst_path):
                        shutil.copy2(src_path, dst_path)
                        self.logger.info(f"Copied: {rel_path}")
                else:
                    self.logger.debug(f"Skipped: {rel_path}")

        # Remove files in dst that don't exist in src
        for root, dirs, files in os.walk(dst_dir):
            for file in files:
                dst_path = os.path.join(root, file)
                rel_path = os.path.relpath(dst_path, dst_dir)
                src_path = os.path.join(src_dir, rel_path)

                if not os.path.exists(src_path):
                    os.remove(dst_path)
                    self.logger.info(f"Removed: {rel_path}")

        self.logger.info("Directory sync completed")

    def _normalize_patterns(
        self, patterns: Union[str, List[str]]
    ) -> List[Dict[str, Union[str, bool]]]:
        if isinstance(patterns, str):
            patterns = [patterns]

        normalized = []
        for pattern in patterns:
            if isinstance(pattern, str):
                normalized.append({"pattern": pattern, "is_regex": False})
            elif isinstance(pattern, dict):
                normalized.append(
                    {"pattern": pattern["pattern"], "is_regex": pattern.get("is_regex", False)}
                )
            else:
                raise ValueError(f"Invalid pattern format: {pattern}")
        return normalized

    def _should_include_file(
        self,
        file_path: str,
        include_patterns: List[Dict[str, Union[str, bool]]],
        exclude_patterns: List[Dict[str, Union[str, bool]]],
    ) -> bool:
        def matches_any_pattern(patterns):
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                is_regex = pattern_info["is_regex"]

                if is_regex:
                    if re.search(pattern, file_path):
                        return True
                else:
                    if fnmatch.fnmatch(file_path, pattern):
                        return True
            return False

        # File must match at least one include pattern and no exclude patterns
        return matches_any_pattern(include_patterns) and not matches_any_pattern(exclude_patterns)
