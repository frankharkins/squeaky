import unittest
from pyfakefs.fake_filesystem_unittest import TestCase as FsTestCase
import tempfile
from pathlib import Path
import nbformat
import sys
from io import StringIO
from unittest.mock import patch

from squeaky import squeaky_cli
from squeaky import clean_notebook as clean_notebook_fn
from squeaky.tools import get_inputs


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
        new_notebook, problems = clean_notebook_fn(examples.dirty_notebook)
        assert len(problems) == 5
        assert new_notebook == examples.clean_notebook
        examples.reset()


class TestCLI(unittest.TestCase):
    @patch("sys.stdout", StringIO())
    @patch("sys.argv", ["squeaky", str(examples.dirty_tempfile_path), "--check"])
    def test_check_flag_does_not_modify(self):
        with self.assertRaises(SystemExit) as context:
            squeaky_cli()
        self.assertEqual(context.exception.code, 1)
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

    @patch("sys.stdout", new_callable=StringIO)
    @patch(
        "sys.argv",
        ["squeaky", str(examples.dirty_tempfile_path), "--check", "--no-advice"],
    )
    def test_no_advice_flag_works(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            squeaky_cli()
        self.assertEqual(
            mock_stdout.getvalue().strip().split("\n")[-1],
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        )
        examples.reset()

class TestCLIPaths(FsTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir("examples")
        self.fs.create_dir("examples/.ipynb_checkpoints")
        self.fs.create_dir("other")
        for path in [
            "my_notebook.ipynb",
            ".my_hidden_notebook.ipynb",
            "examples/another_notebook.ipynb",
            "examples/.ipynb_checkpoints/hidden_notebook.ipynb",
            "examples/not-a-notebook.yml"
        ]:
            self.fs.create_file(path)

    @patch("sys.argv", ["squeaky", "my_notebook.ipynb", "examples/"])
    def test_recurse_directories(self):
        inputs = get_inputs()
        paths = set(map(str, inputs.filepaths))
        self.assertEqual(paths, { "my_notebook.ipynb", "examples/another_notebook.ipynb" })

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", ["squeaky", "invalid.ipynb", "unvalid.ipynb"])
    def test_missing_files_message(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            squeaky_cli()
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "\033[91mERROR: Could not find the following files:\n  invalid.ipynb\n  unvalid.ipynb\033[0m"
        )

if __name__ == "__main__":
    unittest.main(buffer=True)
    os.remove(clean_tempfile_path)
    os.remove(dirty_tempfile_path)
