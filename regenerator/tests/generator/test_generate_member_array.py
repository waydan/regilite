"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestArrayMember(unittest.TestCase):
    def test_suffix_appended_to_register_name(self):
        self.assertEqual(
            generateHeader.makeDataMember(
                structuralModel.Array(
                    element=structuralModel.Register(name="R{}", size=32),
                    index=["1"],
                    increment=4,
                )
            ).name,
            "R1",
        )

    def test_multiple_suffixed_names_appear_on_single_line(self):
        self.assertEqual(
            generateHeader.makeDataMember(
                structuralModel.Array(
                    element=structuralModel.Register(name="R{}", size=32),
                    index=["1", "2", "3"],
                    increment=4,
                )
            ).name,
            "R1, R2, R3",
        )

    def test_use_array_syntax_when_index_is_sequential_and_zero_ordinal(self):
        self.assertEqual(
            generateHeader.makeDataMember(
                structuralModel.Array(
                    element=structuralModel.Register(name="R{}", size=32),
                    index=["0", "1", "2"],
                    increment=4,
                )
            ).name,
            "R[3]",
        )

    def test_do_not_use_array_syntax_for_infix(self):
        self.assertEqual(
            generateHeader.makeDataMember(
                structuralModel.Array(
                    element=structuralModel.Register(name="R{}R", size=32),
                    index=["0", "1", "2"],
                    increment=4,
                )
            ).name,
            "R0R, R1R, R2R",
        )

    def test_element_description_is_preserved(self):
        Rx = structuralModel.Register(
            name="R{}", size=32, reset_value=0, description="description"
        )
        self.assertRegex(
            str(
                generateHeader.makeDataMember(
                    structuralModel.Array(
                        element=Rx,
                        index=["1"],
                        increment=4,
                    )
                )
            ),
            rf"^{generateHeader.generateType(Rx)}\s+R1\s*;\s*//\s*description$",
        )


if __name__ == "__main__":
    unittest.main()
