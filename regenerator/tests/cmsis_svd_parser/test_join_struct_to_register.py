"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator import cmsisSvdParser
from regenerator.model import types, members


class TestJoiningStructWithDataMember(unittest.TestCase):
    a = types.Register(name="a", size=8, reset_value=0)
    b = types.Register(name="b", size=8, reset_value=0)

    member_a = members.DataMember(type=a, name="a", offset=0)
    member_b = members.DataMember(type=b, name="b", offset=1)

    def test_nonoverlapping_member_appended_to_member_list(self):
        self.assertEqual(
            cmsisSvdParser.insertMember(
                types.Struct(members=[self.member_a]),
                self.member_b,
            ),
            types.Struct(members=[self.member_a, self.member_b]),
        )


if __name__ == "__main__":
    unittest.main()
