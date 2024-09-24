import argparse
import subprocess
from typing import List

DEFAULT_EXCLUDE_PATTERNS = [
    ".git/",
    "*.swp",
    "*.swo",
    "*~",
    ".DS_Store",
    "/build/",
    "/dist/",
    "*.pyc",
    "__pycache__/",
    "/node_modules/",
    "/vendor/",
    "*.log",
    ".env",
    ".env.*",
    "config.ini",
]


def run_rsync_with_filters(
    source: str,
    destination: str,
    include_patterns: List[str],
    exclude_patterns: List[str],
    use_default_excludes: bool,
):
    """
    Run rsync with white (include) and black (exclude) filter patterns.

    :param source: Source directory or file
    :param destination: Destination directory
    :param include_patterns: List of patterns to include
    :param exclude_patterns: List of patterns to exclude
    :param use_default_excludes: Whether to use default exclude patterns
    """
    rsync_command = ["rsync", "-av"]
    if use_default_excludes:
        for pattern in DEFAULT_EXCLUDE_PATTERNS:
            rsync_command.extend(["--exclude", pattern])

    # Add black filter patterns (exclude)
    for pattern in exclude_patterns:
        rsync_command.extend(["--exclude", pattern])

    # Add white filter patterns (include)
    for pattern in include_patterns:
        rsync_command.extend(["--include", pattern])

    # Exclude everything else if white patterns are specified
    if include_patterns:
        rsync_command.extend(["--exclude", "*"])

    # Add source and destination
    rsync_command.extend([source, destination])
    print("Executing rsync command:", " ".join(rsync_command))

    # Run the rsync command
    try:
        result = subprocess.run(rsync_command, check=True, text=True, capture_output=True)
        print("Rsync completed successfully")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Rsync failed with error: {e}")
        print(e.stderr)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run rsync with include and exclude filter patterns"
    )
    parser.add_argument("source", help="Source directory or file")
    parser.add_argument("destination", help="Destination directory")
    parser.add_argument("--include", action='append', default=[], help="Include filter patterns")
    parser.add_argument("--exclude", action='append', default=[], help="Exclude filter patterns")
    parser.add_argument(
        "--no-default-excludes", action='store_true', help="Disable default exclude patterns"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    run_rsync_with_filters(
        args.source, args.destination, args.include, args.exclude, not args.no_default_excludes
    )
