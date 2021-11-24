"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator.model import types, members
from regenerator import generateHeader


class TestUnionTypeGenerator(unittest.TestCase):
    R1 = members.DataMember(
        type=types.Register(name="R1", size=32), name="R1", offset=0
    )
    R2 = members.DataMember(
        type=types.Register(name="R2", size=32), name="R2", offset=0
    )

    def test_generating_empty_union(self):
        self.assertRegex(
            generateHeader.generateType(types.Union()),
            r"^union\s*{\s*}$",
        )

    def test_generating_struct_with_single_member(self):
        self.assertRegex(
            generateHeader.generateType(types.Union(members=[(self.R1, 0)])),
            r"^union\s*{{\s*{}\s*}}$".format(generateHeader.makeDataMember(self.R1)),
        )

    def test_generating_struct_with_two_same_position_members(self):
        self.assertRegex(
            generateHeader.generateType(
                types.Union(members=[(self.R1, 0), (self.R2, 0)])
            ),
            r"^union\s*{{\s*{}\s*{}\s*}}$".format(
                generateHeader.makeDataMember(self.R1),
                generateHeader.makeDataMember(self.R2),
            ),
        )


if __name__ == "__main__":
    unittest.main()
