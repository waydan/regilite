"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestStructTypeGenerator(unittest.TestCase):
    R1 = structuralModel.Register(name="R1", size=32)
    R2 = structuralModel.Register(name="R2", size=32)
    R3 = structuralModel.Register(name="R3", size=16)

    def test_generating_empty_struct(self):
        self.assertRegex(
            generateHeader.generateType(structuralModel.Struct()),
            r"^struct\s*{\s*}$",
        )

    def test_generating_struct_with_single_zero_offset_member(self):
        self.assertRegex(
            generateHeader.generateType(structuralModel.Struct(members=[(self.R1, 0)])),
            r"^struct \s*{{\s*{}\s*}}$".format(
                generateHeader.generateDataMember(self.R1)
            ),
        )

    def test_generating_struct_with_two_adjacent_members(self):
        self.assertRegex(
            generateHeader.generateType(
                structuralModel.Struct(members=[(self.R1, 0), (self.R2, 4)])
            ),
            r"^struct \s*{{\s*{}\s*{}\s*}}$".format(
                generateHeader.generateDataMember(self.R1),
                generateHeader.generateDataMember(self.R2),
            ),
        )

    def test_add_padding_if_first_member_not_at_zero_offset(self):
        self.assertRegex(
            generateHeader.generateType(structuralModel.Struct(members=[(self.R1, 4)])),
            r"^struct \s*{{\s*regilite::padding<4> _reserved_\d+;\s*{}\s*}}".format(
                generateHeader.generateDataMember(self.R1)
            ),
        )

    def test_padding_sized_to_fill_gap_between_data_members(self):
        self.assertRegex(
            generateHeader.generateType(
                structuralModel.Struct(members=[(self.R1, 0), (self.R3, 6)])
            ),
            r"^struct \s*{{\s*{}\s*regilite::padding<2> _reserved_\d+;\s*{}\s*}}".format(
                generateHeader.generateDataMember(self.R1),
                generateHeader.generateDataMember(self.R3),
            ),
        )

    def test_padding_identifier_made_unique_by_incrementing_suffix(self):
        self.assertRegex(
            generateHeader.generateType(
                structuralModel.Struct(members=[(self.R3, 2), (self.R2, 8)])
            ),
            r"^struct \s*{{\s*regilite::padding<2> _reserved_0;\s*{}"
            r"\s*regilite::padding<4> _reserved_1;\s*{}\s*}}".format(
                generateHeader.generateDataMember(self.R3),
                generateHeader.generateDataMember(self.R2),
            ),
        )


if __name__ == "__main__":
    unittest.main()
