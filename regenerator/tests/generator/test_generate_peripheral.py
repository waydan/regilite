"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.generator import cppstruct
from regenerator.model import members, types

R1 = members.DataMember(type=types.Register(name="R1", size=16), name="R1", offset=0)
R2 = members.DataMember(type=types.Register(name="R2", size=8), name="R2", offset=2)


class TestPeripheralGenreator(unittest.TestCase):
    def test_peripheral_name_is_outermost_namespace(self):
        self.assertRegex(
            cppstruct.generatePeripheral(types.Peripheral(name="peripheral")),
            r"(?s)^(inline)?\s+namespace\s+peripheral\s*{.*}\s*//\s*peripheral$",
        )

    def test_register_definitions_listed_in_peripheral_before_struct(self):
        self.assertRegex(
            cppstruct.generatePeripheral(
                types.Peripheral(
                    name="p",
                    structure=types.Struct(members=[R1, R2]),
                )
            ),
            r"(?s)^inline\s+namespace\s+p\s*{\s*"
            + r"inline namespace\s*{0:}\s*{{.*?}}\s*//\s*{0:}\s*".format(
                cppstruct.getRegisterNamespace(R1.type)
            )
            + r"inline namespace\s*{0:}\s*{{.*?}}\s*//\s*{0:}\s*".format(
                cppstruct.getRegisterNamespace(R2.type)
            ),
        )


if __name__ == "__main__":
    unittest.main()
