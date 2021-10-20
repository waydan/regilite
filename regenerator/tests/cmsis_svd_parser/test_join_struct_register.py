"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import cmsisSvdParser, structuralModel


class TestStructRegisterJoining(unittest.TestCase):
    a = structuralModel.Register(name="a", size=8, reset_value=0)
    b = structuralModel.Register(name="b", size=8, reset_value=0)

    def test_nonoverlapping_register_appended_to_members(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(
                structuralModel.Struct(name="a_only", members=[(self.a, 0)]),
                0,
                self.b,
                1,
            ),
            (
                structuralModel.Struct(
                    name="a_only", members=[(self.a, 0), (self.b, 1)]
                ),
                0,
            ),
        )

    def test_inserted_register_positioned_relative_to_struct(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(
                structuralModel.Struct(name="a_only", members=[(self.a, 0)]),
                10,
                self.b,
                11,
            ),
            (
                structuralModel.Struct(
                    name="a_only", members=[(self.a, 0), (self.b, 1)]
                ),
                10,
            ),
        )

    prefix_b = structuralModel.Register(name="prefix_b", size=8, reset_value=0)

    def test_remove_register_name_prifix_if_matches_struct_name(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(
                structuralModel.Struct(name="prefix", members=[(self.a, 0)]),
                0,
                self.prefix_b,
                1,
            ),
            (
                structuralModel.Struct(
                    name="prefix", members=[(self.a, 0), (self.b, 1)]
                ),
                0,
            ),
        )


if __name__ == "__main__":
    unittest.main()
