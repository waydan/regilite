"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.model import members, types
from regenerator.parser import cmsissvd

Reg = types.Register(name="Register", size=8)


class TestDataMemberJoining(unittest.TestCase):
    def test_struct_data_member_created_from_nonoverlapping_register_data_members(self):
        self.assertIsInstance(
            cmsissvd.joinMembers(
                members.DataMember(type=Reg, name="a", offset=0),
                members.DataMember(type=Reg, name="b", offset=1),
            ).type,
            types.Struct,
        )

    def test_union_data_member_created_from_overlapping_register_data_members(self):
        self.assertIsInstance(
            cmsissvd.joinMembers(
                members.DataMember(type=Reg, name="a", offset=0),
                members.DataMember(type=Reg, name="b", offset=0),
            ).type,
            types.Union,
        )

    def test_register_member_inserted_into_struct_member_when_joining(self):
        self.assertEqual(
            cmsissvd.joinMembers(
                members.DataMember(type=types.Struct(), name="", offset=0),
                members.DataMember(type=Reg, name="a", offset=0),
            ),
            members.DataMember(
                type=types.Struct(
                    members=[members.DataMember(type=Reg, name="a", offset=0)]
                ),
                name="",
                offset=0,
            ),
        )

    def test_register_member_inserted_into_union_member_when_joining(self):
        self.assertEqual(
            cmsissvd.joinMembers(
                members.DataMember(type=types.Union(), name="", offset=0),
                members.DataMember(type=Reg, name="a", offset=0),
            ),
            members.DataMember(
                type=types.Union(
                    members=[members.DataMember(type=Reg, name="a", offset=0)]
                ),
                name="",
                offset=0,
            ),
        )

    def test_struct_or_union_member_named_from_common_prefix(self):
        self.assertEqual(
            cmsissvd.joinMembers(
                members.DataMember(type=Reg, name="prefix_a", offset=0),
                members.DataMember(type=Reg, name="prefix_b", offset=1),
            ).name,
            "prefix",
        )

    def test_struct_or_union_name_removed_from_register_member_when_joining(self):
        self.assertEqual(
            cmsissvd.joinMembers(
                members.DataMember(type=types.Union(), name="prefix", offset=0),
                members.DataMember(type=Reg, name="prefix_a", offset=0),
            )
            .type.members[-1]
            .name,
            "a",
        )

    def test_struct_or_union_offset_subtracted_from_register_member_when_joining(self):
        self.assertEqual(
            cmsissvd.joinMembers(
                members.DataMember(type=types.Union(), name="", offset=4),
                members.DataMember(type=Reg, name="prefix_a", offset=4),
            )
            .type.members[-1]
            .offset,
            0,
        )


if __name__ == "__main__":
    unittest.main()
