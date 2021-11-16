"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestUnionTypeGenerator(unittest.TestCase):
    R1 = structuralModel.Register(name="R1", size=32)
    R2 = structuralModel.Register(name="R2", size=32)

    def test_generating_empty_union(self):
        self.assertRegex(
            generateHeader.generateType(structuralModel.Union()),
            r"^union\s*{\s*}$",
        )

    def test_generating_struct_with_single_member(self):
        self.assertRegex(
            generateHeader.generateType(structuralModel.Union(members=[(self.R1, 0)])),
            r"^union\s*{{\s*{}\s*}}$".format(
                generateHeader.generateDataMember(self.R1)
            ),
        )

    def test_generating_struct_with_two_same_position_members(self):
        self.assertRegex(
            generateHeader.generateType(
                structuralModel.Union(members=[(self.R1, 0), (self.R2, 0)])
            ),
            r"^union\s*{{\s*{}\s*{}\s*}}$".format(
                generateHeader.generateDataMember(self.R1),
                generateHeader.generateDataMember(self.R2),
            ),
        )


if __name__ == "__main__":
    unittest.main()
