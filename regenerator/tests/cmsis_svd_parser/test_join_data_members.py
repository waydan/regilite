"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator import cmsisSvdParser
from regenerator.model import types, members


Ra = types.Register(name="a", size=8)
Rb = types.Register(name="b", size=8)
prefix_a = members.DataMember(type=Ra, name="prefix_a", offset=0)
prefix_b = members.DataMember(type=Rb, name="prefix_b", offset=1)


class TestDataMemberJoining(unittest.TestCase):
    a = types.Register(name="a", size=8)
    b = types.Register(name="b", size=8)

    def test_struct_data_member_created_from_nonoverlapping_register_data_members(self):
        self.assertEqual(
            cmsisSvdParser.smashMembers(
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
            cmsisSvdParser.smashMembers(
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
            cmsisSvdParser.smashMembers(
                members.DataMember(type=Ra, name="a", offset=4),
                members.DataMember(type=Rb, name="b", offset=5),
            ),
            members.DataMember(
                type=types.Struct(
                    members=[
                        members.DataMember(type=Ra, name="a", offset=0),
                        members.DataMember(type=Rb, name="b", offset=1),
                    ]
                ),
                name="",
                offset=4,
            ),
        )

    def test_struct_data_member_takes_common_prefix_as_name(self):
        self.assertEqual(
            cmsisSvdParser.smashMembers(prefix_a, prefix_b),
            members.DataMember(
                type=types.Struct(
                    members=[
                        members.DataMember(type=Ra, name="a", offset=0),
                        members.DataMember(type=Rb, name="b", offset=1),
                    ]
                ),
                name="prefix",
                offset=0,
            ),
        )


if __name__ == "__main__":
    unittest.main()
