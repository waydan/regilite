"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestRegisterTypeGenerator(unittest.TestCase):
    def test_generating_8bit_register_type(self):
        self.assertEqual(
            generateHeader.generateType(
                structuralModel.Register(name="r1", size=8, reset_value=0)
            ),
            r"r1_::reg8_t",
        )

    def test_generating_16bit_register_type(self):
        self.assertEqual(
            generateHeader.generateType(
                structuralModel.Register(name="r1", size=16, reset_value=0)
            ),
            r"r1_::reg16_t",
        )


if __name__ == "__main__":
    unittest.main()
