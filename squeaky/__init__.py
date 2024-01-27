import sys
import nbformat
import subprocess

from .passes.cell_ids import add_missing_cell_ids
from .passes.metadata import clean_metadata
from .passes.svg import clean_svgs
from .passes.svg_id import clean_svg_ids
from .passes.empty_cells import clean_empty_cells
from .passes.trailing_whitespace import clean_trailing_whitespace
from .tools import parse_args


def clean_notebook(notebook, check=False):
    modified = False
    for fn in [
        add_missing_cell_ids,
        clean_metadata,
        clean_svgs,
        clean_svg_ids,
        clean_trailing_whitespace,
        clean_empty_cells,
    ]:
        notebook, msg = fn(notebook)
        if msg is None:
            continue
        modified = True
        if check:
            print(f"❌ {msg.capitalize()}")
        else:
            print(f"✅ Fixed {msg}")
    return notebook, modified


def squeaky_clean_hook(model, **_):
    """
    To run automatically when saving Jupyter notebooks.
    """
    if model["type"] != "notebook":
        return
    if model["content"]["nbformat"] != 4:
        return
    model["content"], _ = clean_notebook(
        nbformat.from_dict(model["content"])
    )


def squeaky_cli():
    """
    To run from the command line
    """
    switches, filepaths = parse_args(sys.argv)
    check = "--check" in switches

    num_unclean = 0
    for path in filepaths:
        print(f"\033[1m{path}\033[0m")
        notebook = nbformat.read(path, 4)
        cleaned_notebook, modified = clean_notebook(notebook, check=check)
        if not modified:
            continue
        num_unclean += 1
        if not check:
            nbformat.write(cleaned_notebook, path)

    if num_unclean > 0:
        print("━" * 35)
        if check:
            print(
                f"Problems in {num_unclean} notebook"
                f"{'s' if num_unclean != 1 else ''}; to fix, run"
                "\n\n  squeaky path/to/notebook.ipynb\n"
            )
            sys.exit(2)
        print(f"Modified {num_unclean} notebook{'s' if num_unclean != 1 else ''}")
        print("━" * 35)
    print("✨ All clean ✨")
