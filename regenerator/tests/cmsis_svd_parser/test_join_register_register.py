"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import cmsisSvdParser, structuralModel


class TestRegisterJoining(unittest.TestCase):
    a = structuralModel.Register(name="a", size=8, reset_value=0)
    b = structuralModel.Register(name="b", size=8, reset_value=0)

    def test_struct_created_from_nonoverlapping_registers(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(self.a, 0, self.b, 1),
            (structuralModel.Struct(name="", members=[(self.a, 0), (self.b, 1)]), 0),
        )

    def test_union_created_from_overlapping_registers(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(self.a, 0, self.b, 0),
            (structuralModel.Union(name="", members=[(self.a, 0), (self.b, 0)]), 0),
        )

    prefix_a = structuralModel.Register(name="prefix_a", size=8, reset_value=0)
    prefix_b = structuralModel.Register(name="prefix_b", size=8, reset_value=0)

    def test_struct_takes_common_prefix_as_name(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(self.prefix_a, 0, self.prefix_b, 1),
            (
                structuralModel.Struct(
                    name="prefix", members=[(self.a, 0), (self.b, 1)]
                ),
                0,
            ),
        )


if __name__ == "__main__":
    unittest.main()
