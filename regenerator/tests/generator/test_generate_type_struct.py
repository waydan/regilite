"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.generator import cppstruct
from regenerator.model import members, types

Reg16 = types.Register(name="Register", size=16)
Reg32 = types.Register(name="Register", size=32)
member_at_0 = members.DataMember(type=Reg32, name="MR0", offset=0)
member_at_2 = members.DataMember(type=Reg16, name="MR2", offset=2)
member_at_4 = members.DataMember(type=Reg32, name="MR4", offset=4)
member_at_6 = members.DataMember(type=Reg16, name="MR6", offset=6)
member_at_8 = members.DataMember(type=Reg16, name="MR8", offset=8)


class TestStructTypeGenerator(unittest.TestCase):
    def test_generating_empty_struct(self):
        self.assertRegex(
            cppstruct.generate_type(types.Struct()),
            r"^struct {\s*}$",
        )

    def test_struct_name_used_as_type_name(self):
        self.assertRegex(
            cppstruct.generate_type(types.Struct(name="StructType")),
            r"^struct StructType {\s*}$",
        )

    def test_generating_struct_with_single_zero_offset_member(self):
        self.assertRegex(
            cppstruct.generate_type(types.Struct(members=[member_at_0])),
            r"^struct\s*{{\s*{}\s*}}$".format(cppstruct.make_data_member(member_at_0)),
        )

    def test_generating_struct_with_two_adjacent_members(self):
        self.assertRegex(
            cppstruct.generate_type(types.Struct(members=[member_at_0, member_at_4])),
            r"^struct\s*{{\s*{}\s*{}\s*}}$".format(
                *map(cppstruct.make_data_member, (member_at_0, member_at_4))
            ),
        )

    def test_assertion_raised_if_adjacent_struct_members_have_same_offset(self):
        self.assertRaises(
            AssertionError,
            cppstruct.generate_type,
            types.Struct(members=[member_at_0, member_at_0]),
        )

    def test_add_padding_if_first_member_not_at_zero_offset(self):
        self.assertRegex(
            cppstruct.generate_type(types.Struct(members=[member_at_4])),
            r"^struct\s*{{\s*regilite::padding<4> _reserved_\d+;\s*{}\s*}}".format(
                cppstruct.make_data_member(member_at_4)
            ),
        )

    def test_padding_sized_to_fill_gap_between_data_members(self):
        self.assertRegex(
            cppstruct.generate_type(types.Struct(members=[member_at_0, member_at_6])),
            r"^struct\s*{{\s*{}\s*regilite::padding<2> _reserved_\d+;\s*{}\s*}}".format(
                *map(cppstruct.make_data_member, (member_at_0, member_at_6)),
            ),
        )

    def test_padding_identifier_made_unique_by_incrementing_suffix(self):
        self.assertRegex(
            cppstruct.generate_type(types.Struct(members=[member_at_2, member_at_8])),
            r"^struct\s*{{\s*regilite::padding<2> _reserved_0;\s*{}"
            r"\s*regilite::padding<4> _reserved_1;\s*{}\s*}}".format(
                *map(cppstruct.make_data_member, (member_at_2, member_at_8))
            ),
        )

    def test_struct_offset_increments_properly_for_three_registers(self):
        self.assertRegex(
            cppstruct.generate_type(
                types.Struct(members=[member_at_0, member_at_4, member_at_8])
            ),
            r"^struct\s*{{\s*{}\s*{}\s*{}\s*}}".format(
                *map(
                    cppstruct.make_data_member,
                    (member_at_0, member_at_4, member_at_8),
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()
