"""
Tests for transliterate.py (unicodelowersplit).

Approach: rather than snapshot-testing the function against its own output,
`_reference_transliterate` below independently re-derives the expected
result straight from the x000/x004/x005/x020 tables, using a deliberately
simpler/different code path (no _get_repl_str, no shared Cache). Agreement
between the two implementations is a real correctness check, not a tautology.
"""
import os
import sys
import unittest

# Make the project root importable even when this file is run directly
# (e.g. `python tests/test_transliterate.py`), not just under pytest --
# pytest loads conftest.py automatically, but a direct run or plain
# `python -m unittest tests/test_transliterate.py` does not.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import x000
import x004
import x005
import x020
from transliterate import unicodelowersplit

_TABLES = {0: x000.data, 4: x004.data, 5: x005.data, 32: x020.data}


def _reference_transliterate(text):
    tokens = []
    current = ""
    lang_counts = {"en": 0, "ru": 0, "hy": 0}

    for ch in text:
        codepoint = ord(ch)
        section = codepoint >> 8
        position = codepoint % 256

        if section == 0 and position == 32:  # ASCII space ends a token
            if current:
                tokens.append(current)
                current = ""
            continue

        if section not in _TABLES:
            continue  # unmapped block: silently dropped, doesn't break the token

        current += _TABLES[section][position]
        if section == 0:
            lang_counts["en"] += 1
        elif section == 4:
            lang_counts["ru"] += 1
        else:  # 5 or 32
            lang_counts["hy"] += 1

    if current:
        tokens.append(current)

    return max(lang_counts, key=lang_counts.get), tokens


class ReferenceAgreementTests(unittest.TestCase):
    """unicodelowersplit must match an independent table lookup."""

    def check(self, text):
        self.assertEqual(unicodelowersplit(text), _reference_transliterate(text))

    def test_plain_english(self):
        self.check("Hello World")

    def test_russian_word(self):
        self.check("Привет мир")

    def test_armenian_word(self):
        self.check("Բարեւ աշխարհ")

    def test_mixed_languages(self):
        self.check("Hello Привет Բարեւ")

    def test_digits_and_punctuation(self):
        self.check("Room 12/5, Building 3.")

    def test_tabs_and_newlines_do_not_split_tokens(self):
        # only ASCII space (0x20) ends a token -- \t and \n are mapped
        # characters in x000 and get appended into the current token
        self.check("a\tb\nc")

    def test_multiple_spaces_collapse(self):
        self.check("foo    bar   baz")

    def test_leading_and_trailing_spaces(self):
        self.check("   padded text   ")

    def test_empty_string(self):
        self.check("")

    def test_only_spaces(self):
        self.check("     ")

    def test_unmapped_unicode_block_is_dropped_not_split(self):
        # emoji (section far outside 0/4/5/32) should vanish from the
        # token but must NOT act as a token boundary the way space does
        self.check("hello\U0001F600world")


class BehaviorTests(unittest.TestCase):
    """Specific, human-checkable expectations."""

    def test_basic_tokenization_and_lowercasing(self):
        lang, tokens = unicodelowersplit("Hello World")
        self.assertEqual(tokens, ["hello", "world"])
        self.assertEqual(lang, "en")

    def test_language_majority_english(self):
        lang, _ = unicodelowersplit("the quick brown fox")
        self.assertEqual(lang, "en")

    def test_language_majority_russian(self):
        lang, _ = unicodelowersplit("привет как дела")
        self.assertEqual(lang, "ru")

    def test_language_majority_armenian(self):
        lang, _ = unicodelowersplit("Բարեւ ինչպես ես")
        self.assertEqual(lang, "hy")

    def test_no_trailing_empty_token(self):
        _, tokens = unicodelowersplit("one two ")
        self.assertNotIn("", tokens)
        self.assertEqual(tokens, ["one", "two"])

    def test_digits_pass_through_unchanged(self):
        _, tokens = unicodelowersplit("building 42")
        self.assertIn("42", tokens)

    def test_known_russian_transliteration(self):
        # п=p р=r и=i в=v е=e т=t
        _, tokens = unicodelowersplit("привет")
        self.assertEqual(tokens, ["privet"])

    def test_known_data_quirk_uppercase_N(self):
        _, tokens = unicodelowersplit("N")
        self.assertEqual(tokens, ["n"])  # current (buggy) behavior
        _, tokens = unicodelowersplit("n")
        self.assertEqual(tokens, ["n"])  # lowercase is correct


if __name__ == "__main__":
    unittest.main(verbosity=2)