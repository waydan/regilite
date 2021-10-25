"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import cmsisSvdParser, structuralModel


class TestArrayArrayJoining(unittest.TestCase):
    a = structuralModel.Register(name="a", size=8, reset_value=0)
    b = structuralModel.Register(name="b", size=8, reset_value=0)

    def test_arrays_with_same_index_and_increment_are_merged(self):
        self.assertEqual(
            cmsisSvdParser.joinMembers(
                structuralModel.Array(index=["0", "1"], increment=2, element=self.a),
                0,
                structuralModel.Array(index=["0", "1"], increment=2, element=self.b),
                1,
            ),
            (
                structuralModel.Array(
                    index=["0", "1"],
                    increment=2,
                    element=structuralModel.Struct(members=[(self.a, 0), (self.b, 1)]),
                ),
                0,
            ),
        )

    def test_arrays_with_different_index_or_increment_yields_union_of_arrays(self):
        a_array = structuralModel.Array(index=["0", "1"], increment=1, element=self.a)
        b_array = structuralModel.Array(index=["0"], increment=1, element=self.b)
        self.assertEqual(
            cmsisSvdParser.joinMembers(a_array, 0, b_array, 0),
            (
                structuralModel.Union(
                    members=[(a_array, 0), (b_array, 0)],
                ),
                0,
            ),
        )

    def test_raise_exception_when_array_gap_overlaps_joining_member(self):
        a_array = structuralModel.Array(index=["0", "1"], increment=2, element=self.a)
        with self.assertRaises(RuntimeError):
            cmsisSvdParser.joinMembers(a_array, 0, self.b, 1)


if __name__ == "__main__":
    unittest.main()
