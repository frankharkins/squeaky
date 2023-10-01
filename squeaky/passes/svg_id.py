import re
from hashlib import md5

def generate_ids(cell):
    n = 1
    while True:
        yield md5(
            (cell.id + str(n)).encode("utf-8")
        ).hexdigest()

def clean_svg_ids(notebook):
    """
    Set SVG IDs deterministically based on cell ID, so they should be unique
    but also not change if the notebook is re-run.
    """
    modified = False
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue

        new_ids = generate_ids(cell)
        for output in cell.outputs:
            if "data" not in output:
                continue
            if "image/svg+xml" not in output["data"]:
                continue

            svg = output["data"]["image/svg+xml"]

            existing_ids = re.findall(
                '[^A-z]id="([A-z0-9]+?)"',
                svg
            )
            if not existing_ids:
                continue

            new_svg = svg
            for existing_id in existing_ids:
                new_svg = new_svg.replace(
                        existing_id,
                        new_ids.__next__()
                )
            if new_svg != svg:
                modified = True

            output["data"]["image/svg+xml"] = new_svg

    if modified:
        return notebook, "SVG IDs"
    return notebook, None
