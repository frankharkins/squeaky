import sys
import argparse
from typing import Iterable
from itertools import chain
from pathlib import Path

def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="squeaky",
        description="✨ Make your Jupyter notebooks squeaky clean ✨",
        epilog="Complain at https://github.com/frankharkins/squeaky/issues"
    )
    parser.add_argument("filepaths", nargs="+", type=Path)
    parser.add_argument("--check", action="store_true", dest="check",
        help="do not fix notebooks, just print message and return non-zero exit code if notebooks need linting"
    )
    parser.add_argument("--no-advice", action="store_true", dest="no_advice",
        help="do not explain how to fix (helpful if contributors should use squeaky through a custom linting workflow)"
    )
    return parser

def get_inputs() -> argparse.Namespace:
    """
    Parses sys.argv to find notebook paths and switches

    Returns a tuple with:
        - A list of filepaths
        - An argparse.Namespace for the switches
    """
    inputs = _make_parser().parse_args()
    _check_for_non_existent_files(inputs.filepaths)
    inputs.filepaths = _recurse_directory_paths(inputs.filepaths)
    return inputs

def _recurse_directory_paths(paths: list[Path]) -> Iterable:
    """
    Return iterator that includes all files in paths plus any notebooks inside directories.
    """
    def is_not_hidden(path: Path):
        return not any(part.startswith(".") for part in path.parts)

    non_dirs = filter(lambda f: f.is_file(), paths)
    dirs = filter(lambda f: not f.is_file(), paths)
    recursed_dirs = [filter(is_not_hidden, p.rglob("**/*.ipynb")) for p in dirs]

    return chain(non_dirs, *recursed_dirs)

def _check_for_non_existent_files(paths: list[Path]) -> None:
    non_existant_files = list(filter(lambda f: not f.exists(), paths))
    if non_existant_files == []:
        return
    plural = len(non_existant_files) > 1
    print(
        "\033[91m"
        + f"ERROR: Could not find the following file{ 's' if plural else '' }:\n  "
        + "\n  ".join(map(str, non_existant_files))
        + "\033[0m"
    )
    sys.exit(1)
