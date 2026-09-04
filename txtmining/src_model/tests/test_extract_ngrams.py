import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_engine import _extract_ngrams
from transliterate import unicodelowersplit

class Extract_ngramsTests(unittest.TestCase):
    """_extract_ngrams must match independently."""

    def test_nan_txt(self):
        self.assertEqual(_extract_ngrams('', (1,5)), [])

    def test_txt_length_small_maxN(self):
        self.assertEqual(_extract_ngrams('abc', (1,5)), ["a", "b", "c", "ab", 'bc', 'abc'])

if __name__ == "__main__":
    unittest.main(verbosity=2)