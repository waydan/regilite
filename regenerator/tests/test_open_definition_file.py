"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from os import path, remove, getcwd

from regenerator import main

CWD = path.dirname(__file__)
EMPTY_FILE = "empty_file.xml"
TEST_STRING_FILE = "test_string_file.xml"


class TestOpeningFilesInMain(unittest.TestCase):
    def create_test_file(self, filepath, text):
        if path.exists(filepath):
            raise FileExistsError(f"{filepath} already exists in the current directory")
        else:
            with open(filepath, "w") as file:
                file.write(text)
            self.addCleanup(remove, filepath)

    def test_exception_raised_when_file_not_found(self):
        self.assertRaises(
            FileNotFoundError,
            main.read_register_definition_file,
            "/not/a/real/file.xml",
        )

    def test_absolute_path_file_found(self):
        self.create_test_file(EMPTY_FILE, "")
        self.assertEqual(
            main.read_register_definition_file(path.abspath(EMPTY_FILE)),
            "",
        )

    def test_relative_path_file_found(self):
        self.create_test_file(EMPTY_FILE, "")
        self.assertEqual(
            main.read_register_definition_file(EMPTY_FILE),
            "",
        )

    def test_file_contents_read_as_string(self):
        self.create_test_file(TEST_STRING_FILE, "test string")
        self.assertEqual(
            main.read_register_definition_file(TEST_STRING_FILE),
            "test string",
        )


if __name__ == "__main__":
    unittest.main()
