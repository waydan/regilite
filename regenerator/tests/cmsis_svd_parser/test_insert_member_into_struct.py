"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.model import members, types
from regenerator.parser import cmsissvd

Reg = types.Register(name="REG", size=8, reset_value=0)
member_at_0 = members.DataMember(type=Reg, name="a", offset=0)
member_at_1 = members.DataMember(type=Reg, name="b", offset=1)


class TestInsertingDataMemberIntoStruct(unittest.TestCase):
    def test_insert_member_into_memberless_struct(self):
        self.assertEqual(
            cmsissvd.insert_member(
                types.Struct(),
                member_at_0,
            ),
            types.Struct(members=[member_at_0]),
        )

    def test_nonoverlapping_member_appended_to_member_list(self):
        self.assertEqual(
            cmsissvd.insert_member(
                types.Struct(members=[member_at_0]),
                member_at_1,
            ),
            types.Struct(members=[member_at_0, member_at_1]),
        )

    def test_overlapping_members_joined_and_appended_to_member_list(self):
        self.assertEqual(
            cmsissvd.insert_member(
                types.Struct(members=[member_at_0]),
                member_at_0,
            ),
            types.Struct(members=[cmsissvd.join_members(member_at_0, member_at_0)]),
        )


if __name__ == "__main__":
    unittest.main()
