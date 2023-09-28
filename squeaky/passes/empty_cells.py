def _has_metadata(cell):
    if not cell.metadata:
        return False

    defaults = {
        "editable": True,
        "slideshow": {
         "slide_type": ""
        },
        "tags": []
    }

    metadata = dict(cell.metadata)
    for key, value in defaults.items():
        if metadata.pop(key, value) != value:
            return True

    if not metadata:
        return False
    return True

def clean_empty_cells(notebook):
    """
    Remove any empty cells (source is empty string, or metadata is empty dict).
    """
    initial_len = len(notebook.cells)
    notebook.cells[:] = [
        cell for cell in notebook.cells
        if cell.source or _has_metadata(cell)
    ]

    if len(notebook.cells) != initial_len:
        return notebook, "empty cells"
    return notebook, None
