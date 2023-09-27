def clean_empty_cells(notebook):
    """
    Remove any empty cells (source is empty string, or metadata is empty dict).
    """
    initial_len = len(notebook.cells)
    notebook.cells[:] = [
        cell for cell in notebook.cells
        if cell.source or cell.metadata
    ]

    if len(notebook.cells) != initial_len:
        return notebook, "empty cells"
    return notebook, None
