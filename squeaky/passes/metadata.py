CLEAN_PYTHON_METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3",
    },
}

def _is_python_notebook(notebook):
    language = notebook.metadata.get("kernelspec", {}).get("language", None)
    # Unspecified languages are assumed to be python
    return language is None or language == "python"


def clean_metadata(notebook):
    message = None
    if not _is_python_notebook(notebook):
        # We don't mess with non-python metadata
        return notebook, message

    for key, value in CLEAN_PYTHON_METADATA.items():
        if notebook.metadata.get(key, None) != value:
            message = "modified notebook metadata"
            notebook.metadata[key] = value
    return notebook, message
