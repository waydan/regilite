"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestArrayMemberGenerator(unittest.TestCase):
    def test_generating_zero_ordinal_register_array(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Array(
                    element=structuralModel.Register(
                        name="R{}", size=32, reset_value=0
                    ),
                    index=["0", "1", "2"],
                    increment=4,
                )
            ),
            r"^Rx_::reg\s+R\[3\]\s*;$",
        )

    def test_generating_zero_ordinal_register_array_with_subscript_in_middle(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Array(
                    element=structuralModel.Register(
                        name="R{}R", size=32, reset_value=0
                    ),
                    index=["0", "1", "2"],
                    increment=4,
                )
            ),
            r"^RxR_::reg\s+R0R,\s*R1R,\s*R2R\s*;$",
        )

    def test_generating_nonzero_ordinal_register_array(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Array(
                    element=structuralModel.Register(
                        name="R{}", size=32, reset_value=0
                    ),
                    index=["1", "2", "3"],
                    increment=4,
                )
            ),
            r"^Rx_::reg\s+R1,\s*R2,\s*R3\s*;$",
        )

    def test_generating_register_array_with_description(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Array(
                    element=structuralModel.Register(
                        name="R{}", size=32, reset_value=0, description="description"
                    ),
                    index=["1"],
                    increment=4,
                )
            ),
            r"^Rx_::reg\s+R1\s*;\s*//\s*description$",
        )

    def test_generating_struct_array_without_description(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Array(
                    element=structuralModel.Struct(
                        name="ST",
                        members=[
                            (
                                structuralModel.Register(
                                    name="R",
                                    size=32,
                                    reset_value=0,
                                ),
                                0,
                            )
                        ],
                    ),
                    index=["1"],
                    increment=4,
                ),
            ),
            r"^struct\s*{\s*R_::reg\s+R\s*;\s*}\s*ST1\s*;",
        )

    def test_generating_struct_array_with_description(self):
        self.assertRegex(
            generateHeader.generate(
                structuralModel.Array(
                    element=structuralModel.Struct(
                        name="ST",
                        members=[
                            (
                                structuralModel.Register(
                                    name="R",
                                    size=32,
                                    reset_value=0,
                                    description="description",
                                ),
                                0,
                            )
                        ],
                    ),
                    index=["1"],
                    increment=4,
                ),
            ),
            r"^struct\s*{\s*R_::reg\s+R\s*;\s*//\s*description\s*}\s*ST1\s*;",
        )


if __name__ == "__main__":
    unittest.main()
