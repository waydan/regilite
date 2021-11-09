"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from . import string_unittest_utils
from regenerator import structuralModel, generateHeader


class TestStructMemberGenerator(string_unittest_utils.TestCase):
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

    def test_padding_added_between_noncontiguous_members(self):
        test_struct = self.assertRegexExtractMatch(
            generateHeader.generate(
                structuralModel.Struct(
                    name="ST",
                    members=[
                        (
                            structuralModel.Register(
                                name="R1",
                                size=32,
                                reset_value=0,
                            ),
                            0,
                        ),
                        (
                            structuralModel.Register(
                                name="R2",
                                size=32,
                                reset_value=0,
                            ),
                            8,
                        ),
                    ],
                )
            ),
            r"(?s)^struct\s*{(?P<body>.*)}\s*ST\s*;",
        )
        self.assertRegex(
            test_struct["body"], r"(?m)^[ \t]*regilite::padding<4>\s+_reserved_\d+"
        )


if __name__ == "__main__":
    unittest.main()
