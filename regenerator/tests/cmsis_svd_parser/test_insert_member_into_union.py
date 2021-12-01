"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.model import members, types
from regenerator.parser import cmsissvd

Reg = types.Register(name="REG", size=8, reset_value=0)
member = members.DataMember(type=Reg, name="member", offset=0)


class TestInsertingDataMemberIntoUnion(unittest.TestCase):
    def test_insert_member_into_memberless_union(self):
        self.assertEqual(
            cmsissvd.insert_member(
                types.Union(),
                member,
            ),
            types.Union(members=[member]),
        )

    def test_insert_member_into_union_with_other_member(self):
        self.assertEqual(
            cmsissvd.insert_member(
                types.Union(members=[member]),
                member,
            ),
            types.Union(members=[member, member]),
        )


if __name__ == "__main__":
    unittest.main()
