"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
import re
import unittest

from regenerator import generateHeader
from regenerator.model import types

from . import string_unittest_utils


class TestFieldGenerator(string_unittest_utils.TestCase):
    def test_non_enum_field_definition(self):
        test_alias = self.assertRegexExtractMatch(
            generateHeader.generateField(
                types.Field(name="field_name", mask=1, access="ReadWrite"),
                "register_key",
            ),
            r"^using\s+field_name\s*=\s*regilite::Field<\s*(?P<parameters>.*?)\s*>;",
        )
        value_type, mask, access, key = re.split(r"\s*,\s*", test_alias["parameters"])
        self.assertRegex(value_type, r"\bstd::uint\d{1,2}_t\b")
        self.assertRegex(mask, r"regilite::Mask<(\d+,)?\s*\d+>{}")
        self.assertRegex(access, r"regilite::ReadWrite")
        self.assertRegex(key, r"struct\s*register_key")

    def test_enum_field_definition(self):
        field = types.Field(
            name="field_name",
            mask=1,
            access="ReadWrite",
            value_type=[
                types.Enumeration(name="e0", value=0),
                types.Enumeration(name="e1", value=1),
            ],
        )
        field_text = generateHeader.generateField(field, "register_key")

        # An enun class type is defined including all legal values
        test_enum = self.assertRegexExtractMatch(
            field_text,
            r"^enum\s+class\s+(?P<type>[_a-z]\w*)\s*:\s*std::uint8_t\s*{(?P<body>.*?)};",
            re.S,
        )
        for enum in field.value_type:
            self.assertRegex(
                test_enum["body"],
                rf"{enum.name}\s*=\s*({enum.value:d}|0b0*{enum.value:b}|0x0*{enum.value:x})\s*",
            )

        # The field base type is given a named alias for ease of use
        test_base = self.assertRegexExtractMatch(
            field_text,
            rf"using\s+(?P<name>[_a-z]\w*)\s*=\s*regilite::Field<\s*(?P<parameters>.*?)\s*>\s*;",
            re.S,
        )
        value_type, mask, access, key = re.split(r"\s*,\s*", test_base["parameters"])
        self.assertRegex(value_type, rf"\b{test_enum['type']}\b")
        self.assertRegex(mask, r"regilite::Mask<(\d+,)?\s*\d+>{}")
        self.assertRegex(access, r"regilite::ReadWrite")
        self.assertRegex(key, r"struct\s*register_key")

        # Field type is properly declared during definition
        test_field = self.assertRegexExtractMatch(
            field_text,
            rf"struct\s+field_name\s*:\s*{test_base['name']}\s*{{(?P<body>.*)}};$",
            re.S,
        )

        # Field body contains a construct which delegates to base class
        self.assertRegex(
            test_field["body"],
            r"(explicit\s+constexpr|constexpr\s+explicit)\s+"
            rf"field_name\s*\(\s*{test_enum['type']}\s+(?P<argument>\w+)\s*\)\s*"
            rf":\s*{test_base['name']}\s*\(\s*(?P=argument)\s*\)\s*{{\s*}}",
        )

        # Constexpr static member is created for each possible enum value
        for enum in field.value_type:
            self.assertRegex(
                test_field["body"],
                rf"(static\s+constexpr|constexpr\s+static)\s+"
                rf"{test_base['name']}\s+{enum.name}\s*"
                rf"{{\s*{test_enum['type']}::{enum.name}\s*}};",
            )


if __name__ == "__main__":
    unittest.main()
