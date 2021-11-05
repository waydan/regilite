"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestStructMemberGenerator(unittest.TestCase):
    def test_generating_struct_member_without_registers(self):
        self.assertRegex(
            generateHeader.generate(structuralModel.Struct(name="s1")),
            r"^struct\s+{\s*}\s*s1\s*;$",
        )

    def test_generating_struct_member_with_single_register(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Struct(
                    name="s1",
                    members=[
                        (structuralModel.Register(name="r1", size=32, reset_value=0), 0)
                    ],
                )
            ),
            r"^struct\s+{\s*[\w:]+\sr1;\s*}\s*s1\s*;$",
        )


if __name__ == "__main__":
    unittest.main()
