
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_engine import _term_freq, _extract_ngrams 
from transliterate import unicodelowersplit

class Term_freqTests(unittest.TestCase):
    """_extract_ngrams must match independently."""

    def test_nan_txt(self):
        grams = _extract_ngrams('', (1,5))
        self.assertEqual(_term_freq(grams), {})

    def test_sample_world(self):
        _, token_list = unicodelowersplit("գյումրի")
        grams = _extract_ngrams(token_list[0], (1,5))
        rez = {'g': 0.03333333333333333, 'y': 0.03333333333333333, 'v': 0.03333333333333333, 'o': 0.03333333333333333, 'u': 0.03333333333333333, 'm': 0.03333333333333333, 'r': 0.03333333333333333, 'i': 0.03333333333333333, 'gy': 0.03333333333333333, 'yv': 0.03333333333333333, 'vo': 0.03333333333333333, 'ou': 0.03333333333333333, 'um': 0.03333333333333333, 'mr': 0.03333333333333333, 'ri': 0.03333333333333333, 'gyv': 0.03333333333333333, 'yvo': 0.03333333333333333, 'vou': 0.03333333333333333, 'oum': 0.03333333333333333, 'umr': 0.03333333333333333, 'mri': 0.03333333333333333, 'gyvo': 0.03333333333333333, 'yvou': 0.03333333333333333, 'voum': 0.03333333333333333, 'oumr': 0.03333333333333333, 'umri': 0.03333333333333333, 'gyvou': 0.03333333333333333, 'yvoum': 0.03333333333333333, 'voumr': 0.03333333333333333, 'oumri': 0.03333333333333333}
        self.assertEqual(_term_freq(grams), rez)

if __name__ == "__main__":
    unittest.main(verbosity=2)