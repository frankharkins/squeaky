import sys
from typing import Iterable
from itertools import chain
from pathlib import Path


def parse_args(argv):
    """Parses sys.argv to find notebook paths and switches

    Returns a tuple with:
        - A set of switches (arguments starting with '--')
        - A list of filepaths
    """
    argv = argv[1:] if len(argv) > 1 else []

    switches = set()
    for a in argv:
        if a.startswith("--"):
            switches.add(a)

    filepaths = []
    for a in argv:
        if a not in switches:
            path = Path(a)
            filepaths.append(path)

    return switches, _recurse_directory_paths(filepaths)

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
