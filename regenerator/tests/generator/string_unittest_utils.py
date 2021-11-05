import unittest
import re


class TestCase(unittest.TestCase):
    def assertRegexExtractMatch(self, text, regex, regex_flags=0):
        match = re.search(regex, text, regex_flags)
        if not match:
            self.fail(f"Regex didn't match: {regex!r} not found in {text!r}")
        return match
