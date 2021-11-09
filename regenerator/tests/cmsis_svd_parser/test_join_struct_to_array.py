"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import cmsisSvdParser, structuralModel


class TestStructRegisterJoining(unittest.TestCase):
    array = structuralModel.Array(
        element=structuralModel.Register(name="prefix_reg", size=8, reset_value=0),
        index=["A", "B", "C", "D"],
        increment=4,
    )

    def test_joining_array_to_unnamed_struct_does_not_modify_member_name(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(structuralModel.Struct(), 0, self.array, 0)[0]
            .members[0][0]
            .element.name,
            "prefix_reg",
        )

    def test_remove_array_member_name_prifix_if_matches_struct_name(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(
                structuralModel.Struct(name="prefix"), 0, self.array, 0
            )[0]
            .members[0][0]
            .element.name,
            "reg",
        )


if __name__ == "__main__":
    unittest.main()
