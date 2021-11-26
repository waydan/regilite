"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator.model import members, types


class TestUnionTypeGenerator(unittest.TestCase):
    def test_sizeof_register_is_bit_size_div_8(self):
        self.assertEqual(types.Register(name="R", size=32).sizeof(), 4)

    def test_sizeof_union_with_only_zero_offset_members_is_sizeof_biggest_member(self):
        self.assertEqual(
            types.Union(
                members=[
                    members.DataMember(
                        type=types.Register(name="R", size=16), name="", offset=0
                    ),
                    members.DataMember(
                        type=types.Register(name="R", size=8), name="", offset=0
                    ),
                ]
            ).sizeof(),
            2,
        )

    def test_sizeof_union_depends_on_member_offset(self):
        self.assertEqual(
            types.Union(
                members=[
                    members.DataMember(
                        type=types.Register(name="R", size=16), name="", offset=0
                    ),
                    members.DataMember(
                        type=types.Register(name="R", size=8), name="", offset=2
                    ),
                ]
            ).sizeof(),
            4,
        )

    def test_sizeof_struct_with_sigle_zero_offset_register_is_sizeof_register(self):
        self.assertEqual(
            types.Struct(
                members=[
                    members.DataMember(
                        type=types.Register(name="R", size=32), name="", offset=0
                    )
                ]
            ).sizeof(),
            4,
        )
