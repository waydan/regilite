"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from os import path, remove, getcwd

from regenerator import main


class TestExportFilesFromApplication(unittest.TestCase):
    def test_directory_created_when_non_existant(self):
        self.assertFalse(path.exists("test_directory"))

    # def test_absolute_path_file_found(self):
    #     self.create_test_file(EMPTY_FILE, "")
    #     self.assertEqual(
    #         main.read_register_definition_file(path.abspath(EMPTY_FILE)),
    #         "",
    #     )

    # def test_relative_path_file_found(self):
    #     self.create_test_file(EMPTY_FILE, "")
    #     self.assertEqual(
    #         main.read_register_definition_file(EMPTY_FILE),
    #         "",
    #     )

    # def test_file_contents_read_as_string(self):
    #     self.create_test_file(TEST_STRING_FILE, "test string")
    #     self.assertEqual(
    #         main.read_register_definition_file(TEST_STRING_FILE),
    #         "test string",
    #     )


if __name__ == "__main__":
    unittest.main()
