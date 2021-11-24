"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator.parser import cmsissvd
from regenerator.model import types, members


Ra = types.Register(name="a", size=8)
Rb = types.Register(name="b", size=8)


class TestDataMemberJoining(unittest.TestCase):
    def test_struct_data_member_created_from_nonoverlapping_register_data_members(self):
        self.assertEqual(
            cmsissvd.smashMembers(
                members.DataMember(type=Ra, name="a", offset=0),
                members.DataMember(type=Rb, name="b", offset=1),
            ),
            members.DataMember(
                type=types.Struct(
                    members=[
                        members.DataMember(type=Ra, name="a", offset=0),
                        members.DataMember(type=Rb, name="b", offset=1),
                    ]
                ),
                name="",
                offset=0,
            ),
        )

    def test_union_data_member_created_from_overlapping_register_data_members(self):
        self.assertEqual(
            cmsissvd.smashMembers(
                members.DataMember(type=Ra, name="a", offset=0),
                members.DataMember(type=Rb, name="b", offset=0),
            ),
            members.DataMember(
                type=types.Union(
                    members=[
                        members.DataMember(type=Ra, name="a", offset=0),
                        members.DataMember(type=Rb, name="b", offset=0),
                    ]
                ),
                name="",
                offset=0,
            ),
        )

    def test_data_member_offsets_rebased_on_containing_member_offset(self):
        self.assertEqual(
            tuple(
                member.offset
                for member in cmsissvd.smashMembers(
                    members.DataMember(type=Ra, name="a", offset=4),
                    members.DataMember(type=Rb, name="b", offset=5),
                ).type.members
            ),
            (0, 1),
        )

    def test_struct_data_member_takes_common_prefix_as_name(self):
        self.assertEqual(
            cmsissvd.smashMembers(
                members.DataMember(type=Ra, name="prefix_a", offset=0),
                members.DataMember(type=Rb, name="prefix_b", offset=1),
            ).name,
            "prefix",
        )

    def test_member_name_prefix_removed_when_inserting_in_struct(self):
        self.assertEqual(
            tuple(
                member.name
                for member in cmsissvd.smashMembers(
                    members.DataMember(type=Ra, name="prefix_a", offset=0),
                    members.DataMember(type=Rb, name="prefix_b", offset=1),
                ).type.members
            ),
            ("a", "b"),
        )

    def test_register_member_inserted_into_struct_member_when_joining(self):
        self.assertEqual(
            cmsissvd.smashMembers(
                members.DataMember(type=types.Struct(), name="", offset=0),
                members.DataMember(type=Ra, name="a", offset=0),
            ),
            members.DataMember(
                type=types.Struct(
                    members=[members.DataMember(type=Ra, name="a", offset=0)]
                ),
                name="",
                offset=0,
            ),
        )

    def test_register_member_inserted_into_union_member_when_joining(self):
        self.assertEqual(
            cmsissvd.smashMembers(
                members.DataMember(type=types.Union(), name="", offset=0),
                members.DataMember(type=Ra, name="a", offset=0),
            ),
            members.DataMember(
                type=types.Union(
                    members=[members.DataMember(type=Ra, name="a", offset=0)]
                ),
                name="",
                offset=0,
            ),
        )

    def test_struct_or_union_name_removed_from_register_member_when_joining(self):
        self.assertEqual(
            cmsissvd.smashMembers(
                members.DataMember(type=types.Union(), name="prefix", offset=0),
                members.DataMember(type=Ra, name="prefix_a", offset=0),
            )
            .type.members[-1]
            .name,
            "a",
        )

    def test_struct_or_union_offset_subtracted_from_register_member_when_joining(self):
        self.assertEqual(
            cmsissvd.smashMembers(
                members.DataMember(type=types.Union(), name="", offset=4),
                members.DataMember(type=Ra, name="prefix_a", offset=4),
            )
            .type.members[-1]
            .offset,
            0,
        )


if __name__ == "__main__":
    unittest.main()
