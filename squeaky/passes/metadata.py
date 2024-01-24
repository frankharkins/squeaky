CLEAN_METADATA = {
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


def clean_metadata(notebook):
    message = None
    for key, value in CLEAN_METADATA.items():
        if notebook.metadata[key] != value:
            message = "modified notebook metadata"
            notebook.metadata[key] = value
    return notebook, message
