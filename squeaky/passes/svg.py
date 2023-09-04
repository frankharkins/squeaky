from scour import scour


class ScourOptions:
    def __init__(self, **entries):
        self.__dict__.update(entries)


SCOUR_OPTIONS = ScourOptions(
    **{
        "simple_colors": False,
        "style_to_xml": True,
        "group_collapse": True,
        "group_create": True,
        "keep_editor_data": False,
        "keep_defs": False,
        "renderer_workaround": True,
        "strip_xml_prolog": False,
        "remove_titles": True,
        "remove_descriptions": True,
        "remove_metadata": True,
        "remove_descriptive_elements": True,
        "strip_comments": True,
        "enable_viewboxing": True,
        "indent_type": "none",
        "newlines": False,
        "strip_xml_space_attribute": False,
        "strip_ids": True,
    }
)


def clean_svgs(notebook):
    """
    Search through notebook and find/replace un-minimized SVGs
    """
    modified = False
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue

        for output in cell.outputs:
            if "data" not in output:
                continue
            if "image/svg+xml" not in output["data"]:
                continue

            svg = output["data"]["image/svg+xml"]
            if "\n" not in svg:
                continue

            modified = True
            min_svg = scour.scourString(svg, SCOUR_OPTIONS)
            min_svg = min_svg.replace("\n", "")
            output["data"]["image/svg+xml"] = min_svg

    if modified:
        return notebook, "un-minified SVGs"
    return notebook, None
