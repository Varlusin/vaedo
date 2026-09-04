import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_engine import _term_freq, _extract_ngrams, SearchIndex 
from transliterate import unicodelowersplit

class Term_freqTests(unittest.TestCase):
    """_extract_ngrams must match independently."""

    _, world_list = unicodelowersplit("գյուղ քաղաք մարզ country, city, vilage, город")
    test_model = SearchIndex()
    test_model.fit(world_list)
    print(test_model.labels_)

    def test_nan_txt(self):
        grams = _extract_ngrams('', (1,5))
        self.assertEqual(_term_freq(grams), {})



if __name__ == "__main__":
    unittest.main(verbosity=2)