"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.model import members, types
from regenerator.parser import cmsissvd

Reg = types.Register(name="Register", size=32)
member_a = members.DataMember(type=Reg, name="a", offset=0)
member_b = members.DataMember(type=Reg, name="b", offset=4)


class TestArrayArrayJoining(unittest.TestCase):
    def test_arrays_with_same_index_and_increment_are_merged(self):
        self.assertEqual(
            cmsissvd.join_members(
                members.MemberArray(member=member_a, index=["0", "1"], increment=4),
                members.MemberArray(member=member_b, index=["0", "1"], increment=4),
            ).member,
            cmsissvd.join_members(member_a, member_b),
        )

    def test_joining_dissimilar_arrays_yields_union_of_arrays(self):
        a_array = members.MemberArray(
            member=members.DataMember(type=Reg, name="a", offset=0),
            index=["0", "1"],
            increment=4,
        )
        b_array = members.MemberArray(
            member=members.DataMember(type=Reg, name="b", offset=0),
            index=["0"],
            increment=4,
        )
        self.assertEqual(
            cmsissvd.join_members(a_array, b_array),
            members.DataMember(
                type=types.Union(members=[a_array, b_array]), name="", offset=0
            ),
        )

    def test_unioned_arrays_are_renamed_and_offset_rebased_when_combined(self):
        self.assertEqual(
            tuple(
                (array.member.name, array.member.offset)
                for array in cmsissvd.join_members(
                    members.MemberArray(
                        member=members.DataMember(type=Reg, name="prefix_ra", offset=4),
                        index=["0", "1"],
                        increment=4,
                    ),
                    members.MemberArray(
                        member=members.DataMember(type=Reg, name="prefix_rb", offset=4),
                        index=["0"],
                        increment=4,
                    ),
                ).type.members
            ),
            (("ra", 0), ("rb", 0)),
        )


if __name__ == "__main__":
    unittest.main()
