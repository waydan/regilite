"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator import generateHeader
from regenerator.model import types


class TestRegisterTypeGenerator(unittest.TestCase):
    def test_register_typename_used_for_namespace(self):
        self.assertEqual(
            generateHeader.getRegisterNamespace(
                types.Register(name="register_name", size=32)
            ),
            "register_name_",
        )

    def test_generating_8bit_register_type(self):
        self.assertEqual(
            generateHeader.generateType(
                types.Register(name="R1", size=8, reset_value=0)
            ),
            "R1_::reg8_t",
        )

    def test_generating_16bit_register_type(self):
        R1 = types.Register(name="R1", size=16, reset_value=0)
        self.assertEqual(
            generateHeader.generateType(R1),
            "{}::reg16_t".format(generateHeader.getRegisterNamespace(R1)),
        )


if __name__ == "__main__":
    unittest.main()
