"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestRegisterTypeGenerator(unittest.TestCase):
    def test_generating_register_member_without_description(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Register(name="r1", size=32, reset_value=0)
            ),
            rf"^r1_::reg\s+r1\s*;$",
        )

    def test_register_description_appears_to_right(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Register(
                    name="r1", size=32, reset_value=0, description="test description"
                )
            ),
            rf"^r1_::reg\s+r1\s*;\s*//\s*test description$",
        )


if __name__ == "__main__":
    unittest.main()
