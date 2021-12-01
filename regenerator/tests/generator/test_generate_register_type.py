"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import re
import unittest
from itertools import zip_longest

from regenerator import generateHeader
from regenerator.model import types

from . import string_unittest_utils


class TestRegisterTypeGenerator(string_unittest_utils.TestCase):
    def test_generating_register_type_without_fields(self):
        register_namespace = self.assertRegexExtractMatch(
            generateHeader.generateRegisterFieldGroup(
                types.Register(name="r1", size=32, reset_value=0)
            ),
            r"(?s)^(inline)?\s+namespace\s+r1_\s*{(?P<type_alias>.*)}",
        )
        register_type = self.assertRegexExtractMatch(
            register_namespace["type_alias"],
            r"using\s+reg\s*=\s*regilite::DefaultRegister<\s*(?P<parameters>.*?)\s*>;",
        )
        storage_type, reset_value = re.split(r"\s*,\s*", register_type["parameters"])
        self.assertRegex(storage_type, r"^std::uint32_t$")
        self.assertRegex(reset_value, r"^(0|0b0+|0x0+)$")

    def test_generating_register_type_with_fields(self):
        field_types = [
            types.Field(name="f0", mask=1, access="WriteOnly"),
            types.Field(
                name="f1",
                mask=0b110,
                access="ReadOnly",
                value_type=[types.Enumeration(name="e0", value=0)],
            ),
        ]
        register_namespace = self.assertRegexExtractMatch(
            generateHeader.generateRegisterFieldGroup(
                types.Register(
                    name="r2",
                    size=16,
                    reset_value=10,
                    fields=field_types,
                )
            ),
            r"(?s)^(inline)?\s+namespace\s+r2_\s*{(?P<fields_and_register>.*)}",
        )
        register_type = self.assertRegexExtractMatch(
            register_namespace["fields_and_register"],
            r"using\s+reg\s*=\s*regilite::DefaultRegister<\s*(?P<parameters>.*?)\s*>;",
        )
        storage_type, reset_value, *fields = re.split(
            r"\s*,\s*", register_type["parameters"]
        )
        self.assertEqual(storage_type, "std::uint16_t")
        self.assertRegex(reset_value, r"^(10|0b0*1010|0x0*A)$")

        # Each field appears exactly once as a template parameter
        for field_text, field_model in zip_longest(fields, field_types):
            with self.subTest(field_text=field_text):
                self.assertEqual(
                    field_text,
                    field_model.name,
                )


if __name__ == "__main__":
    unittest.main()
