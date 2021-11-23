"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.parser import cmsissvd
from regenerator.model import types, members


Reg = types.Register(name="REG", size=8, reset_value=0)
member_a = members.DataMember(type=Reg, name="a", offset=0)
member_b = members.DataMember(type=Reg, name="b", offset=1)
member_c = members.DataMember(type=Reg, name="c", offset=0)


class TestJoiningStructWithDataMember(unittest.TestCase):
    def test_nonoverlapping_member_appended_to_member_list(self):
        self.assertEqual(
            cmsissvd.insertMember(
                types.Struct(members=[member_a]),
                member_b,
            ),
            types.Struct(members=[member_a, member_b]),
        )

    def test_overlapping_members_joined_and_appended_to_member_list(self):
        self.assertEqual(
            cmsissvd.insertMember(
                types.Struct(members=[member_a]),
                member_c,
            ),
            types.Struct(members=[cmsissvd.smashMembers(member_a, member_c)]),
        )


if __name__ == "__main__":
    unittest.main()
