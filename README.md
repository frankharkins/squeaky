# Squeaky

> ✨ Make your Jupyter notebooks squeaky clean ✨

Squeaky removes unwanted changes to your notebooks to make your Git diffs
cleaner. Tools like [nbdime](https://nbdime.readthedocs.io/en/latest/) and
[ReviewNB](https://www.reviewnb.com/) are awesome, but can be clunky and
difficult to learn. Instead, Squeaky makes it easier to manage notebook diffs
with standard Git tools.


## Usage

First, install:

```sh
pip install squeaky
```

Then use Squeaky to clean a notebook:

```sh
squeaky path/to/notebook(s).ipynb
```

To check notebooks without modifying them, use the `--check` flag.

```sh
squeaky path/to/notebook.ipynb --check
```

### Jupyter pre-save hook

You can automatically run your notebooks through Squeaky before saving them by
editing your Jupyter config file. First, find the location of your config
directory by running

```sh
jupyter --config-dir
```

Your config directory may contain either a `jupyter_lab_config.py` or a
`jupyter_server_config.py` (if neither exists, create an empty file with either
of these names).

> :warning: If you're using Jupyter notebook < 7, then the file will be called
> `jupyter_notebook_config.py`.

Then, add the following lines to that config file.

```python
from squeaky import squeaky_clean_hook
c.FileContentsManager.pre_save_hook = squeaky_clean_hook
```

### Pre-commit hook

To use with [pre-commit](https://pre-commit.com/), add the following to your
`.pre-commit-config.yaml`.

```yaml
repos:
  - repo: local
    hooks:
      - name: Clean notebooks
        id: clean-notebooks
        entry: squeaky --check
        language: python
        files: '(.*?).ipynb$'
```

## Features

- **Reset metadata**

  If you're running your notebooks in CI, then you probably don't care about
  the last environment a notebook was edited in. Squeaky resets notebook
  metadata to a standard metadata.

- **Minify SVGs**

  Setting code image outputs to SVGs makes images look great, but comes with
  horrendous diffs. Squeaky minifies SVG outputs to a single line, which also
  reduces file size.

- **Reset IDs in SVG outputs**

  SVG outputs have another problem: Randomized IDs in the source. Squeaky
  re-generates these IDs deterministically using on the cell's unique ID. This
  means re-running the notebook won't change the output unless the image
  actually changes.

- **Remove trailing whitespace**

  Often missed in markdown (but not in version control), Squeaky removes
  trailing whitespace from ends of lines *and* empty lines from ends and
  beginnings of cells.

- **Remove empty cells**
  
  Squeaky removes empty cells, including that annoying empty code cell at the
  bottom of every other notebook.

- **Add missing cell IDs**

  Cells without IDs now raise a warning in `nbformat`. Squeaky adds these IDs
  for you so you don't need to think about it.

## Contributing

To install requirements and add pre-commit hooks:

```sh
pip install -r requirements-dev.txt
pre-commit install
```

To run unit tests (also run on commit):

```sh
tox
```

## Wishlist

- **Add `--help` message**
- **Turn off features through config file**
