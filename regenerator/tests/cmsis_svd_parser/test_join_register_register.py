"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import cmsisSvdParser, structuralModel


class TestRegisterJoining(unittest.TestCase):
    a = structuralModel.Register(name="a", size=8, reset_value=0)
    b = structuralModel.Register(name="b", size=8, reset_value=0)

    def test_join_nonoverlapping_registers(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(self.a, 0, self.b, 1),
            (structuralModel.Struct(name="", members=[(self.a, 0), (self.b, 1)]), 0),
        )

    def test_join_overlapping_registers(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(self.a, 0, self.b, 0),
            (structuralModel.Union(name="", members=[(self.a, 0), (self.b, 0)]), 0),
        )


if __name__ == "__main__":
    unittest.main()
