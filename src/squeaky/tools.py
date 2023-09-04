import sys
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
            filepaths.append(a)

    # Make all paths of form ./notebook_root/folder/notebook.ipynb
    for idx, path in enumerate(filepaths):
        path = Path(path)
        if path.suffix == "":
            path = path.with_suffix(".ipynb")

        if not path.exists():
            path = Path(NB_ROOT) / path

        filepaths[idx] = path

    return switches, filepaths
