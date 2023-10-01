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

**Experimental:** To automatically fix problems on commit, replace `--check`
with `--git-add`, but beware this can sometimes fail when committing notebooks
with unstaged changes and create a merge conflict (ironic, I know). This should
only be a problem if you `git add --patch` a notebook.


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
