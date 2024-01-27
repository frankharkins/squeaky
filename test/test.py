import unittest
import tempfile
from pathlib import Path
import nbformat
import sys
from io import StringIO
from unittest.mock import patch

from squeaky import squeaky_cli
from squeaky import clean_notebook as clean_notebook_fn


# set up
class ExampleNotebooks:
    def __init__(self):
        self.reset()

    def reset(self):
        self.clean_notebook = nbformat.read("test/example-notebooks/clean.ipynb", 4)
        self.clean_tempfile_path = Path(tempfile.gettempdir(), "squeaky-unittest-clean.ipynb")
        nbformat.write(self.clean_notebook, self.clean_tempfile_path)

        self.dirty_notebook = nbformat.read("test/example-notebooks/dirty.ipynb", 4)
        self.dirty_tempfile_path = Path(tempfile.gettempdir(), "squeaky-unittest-dirty.ipynb")
        nbformat.write(self.dirty_notebook, self.dirty_tempfile_path)

examples = ExampleNotebooks()

class TestAPI(unittest.TestCase):
    def test_clean_notebooks(self):
        new_notebook, modified = clean_notebook_fn(examples.dirty_notebook)
        assert modified == True
        assert new_notebook == examples.clean_notebook
        examples.reset()


class TestCLI(unittest.TestCase):
    @patch("sys.stdout", StringIO())
    @patch("sys.argv", ["squeaky", str(examples.dirty_tempfile_path), "--check"])
    def test_check_flag_does_not_modify(self):
        with self.assertRaises(SystemExit) as context:
            squeaky_cli()
        self.assertEqual(context.exception.code, 2)
        self.assertEqual(
            nbformat.read(examples.dirty_tempfile_path, 4),
            examples.dirty_notebook
        )
        examples.reset()

    @patch("sys.stdout", StringIO())
    @patch("sys.argv", ["squeaky", str(examples.dirty_tempfile_path)])
    def test_command_modifies(self):
        squeaky_cli()
        with open(examples.dirty_tempfile_path) as f:
            self.assertEqual(
                nbformat.read(f, 4),
                examples.clean_notebook
            )
        examples.reset()


if __name__ == "__main__":
    unittest.main(buffer=True)
    os.remove(clean_tempfile_path)
    os.remove(dirty_tempfile_path)
