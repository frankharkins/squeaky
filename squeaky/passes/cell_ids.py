import uuid


def add_missing_cell_ids(notebook):
    message = None
    for cell in notebook.cells:
        if hasattr(cell, "id"):
            continue
        cell.id = str(uuid.uuid4())
        message = "missing cell IDs"
    return notebook, message
