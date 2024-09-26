# src/git_sync_maestro/utils/pretty_print.py

import textwrap
from typing import Any, Callable, Dict, List, Optional


def pretty_print_env(
    env: Dict[str, Any],
    indent: int = 0,
    print_func: Optional[callable] = print,
    exclude_keys: Optional[List[str]] = None,
    include_keys: Optional[List[str]] = None,
    filter_func: Optional[Callable[[str, Any], bool]] = None,
):
    """
    Prints the environment variables in a pretty format.

    :param env: Dictionary of environment variables.
    :param indent: Number of spaces to indent each line.
    :param print_func: Function to use for printing (default is built-in print function).
    :param exclude_keys: List of keys to exclude from printing.
    :param include_keys: List of keys to include in printing (if specified, only these keys will be printed).
    :param filter_func: A function that takes a key and value, and returns True if the item should be included.
    """
    indent_str = ' ' * indent

    if not env:
        print_func(f"{indent_str}No environment variables set.")
        return

    # Apply filters
    filtered_env = {}
    for key, value in env.items():
        if exclude_keys and key in exclude_keys:
            continue
        if include_keys and key not in include_keys:
            continue
        if filter_func and not filter_func(key, value):
            continue
        filtered_env[key] = value

    if not filtered_env:
        print_func(f"{indent_str}No environment variables to display after filtering.")
        return

    max_key_length = max(len(key) for key in filtered_env.keys())

    print_func(f"{indent_str}Environment Variables:")
    for key, value in sorted(filtered_env.items()):
        key_str = f"{key}:".ljust(max_key_length + 1)
        if value == "":
            print_func(f"{indent_str}  {key_str} <empty string>\n")
        else:
            value_lines = textwrap.wrap(str(value), width=80 - indent - max_key_length - 3)
            if not value_lines:  # 값이 공백 문자들로만 이루어진 경우
                print_func(f"{indent_str}  {key_str} <whitespace>\n")
            else:
                print_func(f"{indent_str}  {key_str} {value_lines[0]}\n")
                for line in value_lines[1:]:
                    print_func(f"{indent_str}  {' ' * (max_key_length + 1)} {line}\n")
