import sys
import nbformat
import subprocess

from .passes.metadata import clean_metadata
from .passes.svg import clean_svgs
from .tools import parse_args


def clean_notebooks():
    switches, filepaths = parse_args(sys.argv)

    check = "--check" in switches
    git_add = "--git-add" in switches
    if check and git_add:
        print("Can't set both `--check` and `--git-add`")
        sys.exit(1)

    num_unclean = 0
    for path in filepaths:
        print(f"\033[1m{path}\033[0m")
        notebook = nbformat.read(path, 4)
        passed = True

        for fn in [clean_metadata, clean_svgs]:
            notebook, msg = fn(notebook)
            if msg is not None:
                if check:
                    print(f"❌ {msg.capitalize()}")
                else:
                    print(f"✅ Fixed {msg}")
                passed = False

        if not check:
            nbformat.write(notebook, path)
        if not passed:
            num_unclean += 1
        if git_add:
            subprocess.run(["git", "add", path])

    if num_unclean > 0:
        print("\n----------------------------------------")
        if check:
            print(
                f"Problems in {num_unclean} notebook"
                f"{'s' if num_unclean > 1 else ''}; to fix, run"
                "\n\n  squeaky path/to/notebook.ipynb\n"
            )
            sys.exit(2)
        print(f"Modified {num_unclean} notebook{'s' if num_unclean > 1 else ''}")
    print("✨ All clean ✨")
