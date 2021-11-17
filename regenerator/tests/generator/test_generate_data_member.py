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

    # def test_register_typename_used_for_namespace(self):
    #     self.assertEqual(
    #         generateHeader.getRegisterNamespace(
    #             structuralModel.Register(name="register_name", size=32)
    #         ),
    #         "register_name_",
    #     )

    # def test_generating_8bit_register_type(self):
    #     self.assertEqual(
    #         generateHeader.generateType(
    #             structuralModel.Register(name="R1", size=8, reset_value=0)
    #         ),
    #         "R1_::reg8_t",
    #     )

    # def test_generating_16bit_register_type(self):
    #     R1 = structuralModel.Register(name="R1", size=16, reset_value=0)
    #     self.assertEqual(
    #         generateHeader.generateType(R1),
    #         "{}::reg16_t".format(generateHeader.getRegisterNamespace(R1)),
    #     )


if __name__ == "__main__":
    unittest.main()
