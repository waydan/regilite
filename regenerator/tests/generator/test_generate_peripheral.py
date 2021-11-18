"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from regenerator import structuralModel, generateHeader


class TestPeripheralGenreator(unittest.TestCase):
    empty_peripheral = structuralModel.Peripheral(name="peripheral")
    R1 = structuralModel.Register(name="R1", size=16)
    R2 = structuralModel.Register(name="R2", size=8)

    def test_peripheral_name_is_outermost_namespace(self):
        self.assertRegex(
            generateHeader.generatePeripheral(self.empty_peripheral),
            r"(?s)^(inline)?\s+namespace\s+peripheral\s*{.*}\s*//\s*peripheral$",
        )

    def test_struct_type_is_peripheral_name_with_underscore_t(self):
        self.assertRegex(
            generateHeader.generatePeripheral(self.empty_peripheral),
            r"struct\s+peripheral_t\s*{\s*};",
        )

    def test_register_definitions_listed_in_peripheral_before_struct(self):
        self.assertRegex(
            generateHeader.generatePeripheral(
                structuralModel.Peripheral(
                    name="p",
                    structure=structuralModel.Struct(
                        members=[(self.R1, 0), (self.R2, 2)]
                    ),
                )
            ),
            r"(?s)^inline\s+namespace\s+p\s*{\s*"
            + r"inline namespace\s*{0:}\s*{{.*?}}\s*//\s*{0:}\s*".format(
                generateHeader.getRegisterNamespace(self.R1)
            )
            + r"inline namespace\s*{0:}\s*{{.*?}}\s*//\s*{0:}\s*".format(
                generateHeader.getRegisterNamespace(self.R2)
            ),
        )


if __name__ == "__main__":
    unittest.main()
