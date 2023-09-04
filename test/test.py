import unittest
import tempfile
from pathlib import Path
import nbformat
import sys
from io import StringIO
from unittest.mock import patch

from squeaky import clean_notebooks
from squeaky.passes.metadata import clean_metadata
from squeaky.passes.svg import clean_svgs

# set up
with open(f"test/example-notebooks/clean.ipynb") as f:
    clean_notebook = nbformat.read(f, 4)
clean_tempfile_path = Path(tempfile.gettempdir(), "squeaky-unittest-clean.ipynb")
nbformat.write(clean_notebook, clean_tempfile_path)

with open(f"test/example-notebooks/dirty.ipynb") as f:
    dirty_notebook = nbformat.read(f, 4)
dirty_tempfile_path = Path(tempfile.gettempdir(), "squeaky-unittest-dirty.ipynb")
nbformat.write(dirty_notebook, dirty_tempfile_path)


class TestPasses(unittest.TestCase):
    def test_clean_svgs(self):
        notebook, msg = clean_svgs(dirty_notebook)
        assert msg is not None

        notebook, msg = clean_svgs(notebook)
        assert msg is None

    def test_clean_metadata(self):
        """
        Check `clean_metadata` function
        """
        notebook, msg = clean_metadata(dirty_notebook)
        assert msg is not None

        notebook, msg = clean_metadata(notebook)
        assert msg is None


class TestCLI(unittest.TestCase):
    
    @patch("sys.stdout", StringIO())
    @patch("sys.argv", ["squeaky", str(dirty_tempfile_path), "--check"])
    def test_check_flag_does_not_modify(self):
        print(sys.argv)
        with self.assertRaises(SystemExit) as context:
            clean_notebooks()
        assert context.exception.code == 2

        with open(dirty_tempfile_path) as f:
            assert nbformat.read(f, 4) == dirty_notebook


if __name__ == "__main__":
    unittest.main(buffer=True)
    os.remove(dirty_tempfile_path)
    os.remove(clean_tempfile_path)
