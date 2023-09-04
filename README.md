# Squeaky

> ✨ Make your Jupyter notebooks squeaky clean ✨

Squeaky removes unwanted changes to your notebooks to make your Git diffs
cleaner. Tools like [nbdime](https://nbdime.readthedocs.io/en/latest/) and
[ReviewNB](https://www.reviewnb.com/) are awesome, but are one extra program to
install and learn. Instead, Squeaky makes notebook diffs more manageable with
standard Git tools.

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

## Features

- **Reset metadata**

  If you're running your notebooks in CI, then you probably don't care about
  the last environment a notebook was edited in. Squeaky resets notebook
  metadata to a standard metadata.

- **Minify SVGs**

  Setting code image outputs to SVGs makes images look great, but comes with
  horrendous diffs. Squeaky minifies SVG outputs to a single line, which also
  reduces file size.

## Wishlist

- **Remove empty cells**
- **Remove trailing whitespace** (from end of lines *and* empty lines from ends
  of cells).
