"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestDataMember(unittest.TestCase):
    R1 = structuralModel.Register(name="R", size=32)
    R2 = structuralModel.Register(name="R", size=32, description="description")

    def test_generating_data_member_without_description(self):
        self.assertRegex(
            str(generateHeader.makeDataMember(self.R1)),
            r"^{}\s+R;$".format(generateHeader.generateType(self.R1)),
        )

    def test_generating_data_member_with_description(self):
        self.assertRegex(
            str(generateHeader.makeDataMember(self.R2)),
            r"^{}\s+R; *// description$".format(generateHeader.generateType(self.R2)),
        )


if __name__ == "__main__":
    unittest.main()
