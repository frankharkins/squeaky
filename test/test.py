import unittest
import nbformat

from squeaky.passes.metadata import clean_metadata
from squeaky.passes.svg import clean_svgs

with open(f"test/example-notebooks/dirty.ipynb") as f:
    dirty_notebook = nbformat.read(f, 4)

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

if __name__ == "__main__":
    unittest.main()
