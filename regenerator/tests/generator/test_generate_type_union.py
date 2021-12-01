"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator import generateHeader
from regenerator.model import members, types

Reg32 = types.Register(name="Register", size=32)
R1 = members.DataMember(type=Reg32, name="R1", offset=0)
R2 = members.DataMember(type=Reg32, name="R2", offset=0)


class TestUnionTypeGenerator(unittest.TestCase):
    def test_generating_empty_union(self):
        self.assertRegex(
            generateHeader.generateType(types.Union()),
            r"^union\s*{\s*}$",
        )

    def test_union_name_used_as_type_name(self):
        self.assertRegex(
            generateHeader.generateType(types.Union(name="UnionType")),
            r"^union UnionType {\s*}$",
        )

    def test_generating_struct_with_single_member(self):
        self.assertRegex(
            generateHeader.generateType(types.Union(members=[R1])),
            r"^union\s*{{\s*{}\s*}}$".format(generateHeader.makeDataMember(R1)),
        )

    def test_generating_struct_with_two_same_position_members(self):
        self.assertRegex(
            generateHeader.generateType(types.Union(members=[R1, R2])),
            r"^union\s*{{\s*{}\s*{}\s*}}$".format(
                *map(generateHeader.makeDataMember, (R1, R2))
            ),
        )


if __name__ == "__main__":
    unittest.main()
