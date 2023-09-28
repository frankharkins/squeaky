def clean_trailing_whitespace(notebook):
    """
    Remove trailing whitespace from ends of lines and cells.
    Also remove empty lines from beginning of cells.
    """
    modified = False
    for cell in notebook.cells:
        # Whitespace from ends of lines
        new_source = "\n".join([
            line.rstrip() for line in cell.source.split("\n")
        ])

        # Empty lines at beginning of cell
        new_source = new_source.lstrip("\n")

        # Trailing newlines at end of cell
        new_source = new_source.rstrip()
        if new_source != cell.source:
            modified = True
            cell.source = new_source

    if modified:
        return notebook, "trailing whitespace"
    return notebook, None
