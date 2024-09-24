import argparse
import subprocess
from typing import List


def run_rsync_with_filters(
    source: str, destination: str, include_patterns: List[str], exclude_patterns: List[str]
):
    """
    Run rsync with white (include) and black (exclude) filter patterns.

    :param source: Source directory or file
    :param destination: Destination directory
    :param include_patterns: List of patterns to include
    :param exclude_patterns: List of patterns to exclude
    """
    rsync_command = ["rsync", "-avv"]

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
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    run_rsync_with_filters(args.source, args.destination, args.include, args.exclude)
