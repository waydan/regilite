"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
import re
import unittest

from regenerator.generator import memberfield
from regenerator.model import types

from . import string_unittest_utils

enum_field = types.Field(
    name="field_name",
    mask=1,
    access="ReadWrite",
    value_type=[
        types.Enumeration(name="e0", value=0),
        types.Enumeration(name="e1", value=1),
    ],
)
enum_field_with_comments = types.Field(
    name="field_name",
    mask=1,
    access="ReadWrite",
    value_type=[
        types.Enumeration(name="e0", value=0, description="enum 0"),
        types.Enumeration(name="e1", value=1, description="enum 1"),
    ],
)


class TestFieldGenerator(string_unittest_utils.TestCase):
    def test_non_enum_field_definition(self):
        test_alias = self.assertRegexExtractMatch(
            memberfield.generate_field_definition(
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

    def test_classed_enum_generated_when_field_has_value_type(self):
        self.assertRegex(
            memberfield.generate_field_definition(enum_field, ""),
            rf"(?s)^enum class {enum_field.name}_e : std::uint\d{{1,2}}_t {{.*?}};",
        )

    def test_generated_enum_includes_all_specified_values_in_binary_representation(
        self,
    ):
        self.assertRegex(
            memberfield.generate_field_definition(enum_field, ""),
            f"^enum class.*?{{\s*"
            + r",\s*".join(
                map(
                    lambda e: r"{} = 0b{:b}".format(e.name, e.value),
                    (enum for enum in enum_field.value_type),
                )
            )
            + r"\s*};",
        )

    def test_enumerated_values_may_be_followed_by_description_comments(self):
        field_text = memberfield.generate_field_definition(enum_field_with_comments)
        for enum in enum_field.value_type:
            with self.subTest(enum=enum):
                self.assertRegex(
                    field_text, rf"{enum.name}\s*=\s*.*?,?[ \t]// {enum.description}"
                )

    def test_enum_field_definition(self):
        field_text = memberfield.generate_field_definition(enum_field, "register_key")

        # The enum_field base type is given a named alias for ease of use
        test_base = self.assertRegexExtractMatch(
            field_text,
            rf"(?s)using\s+(?P<name>[_a-z]\w*)\s*=\s*regilite::Field<\s*(?P<parameters>.*?)\s*>\s*;",
        )
        value_type, mask, access, key = re.split(r"\s*,\s*", test_base["parameters"])
        self.assertRegex(value_type, rf"\b{enum_field.name}_e\b")
        self.assertRegex(mask, r"regilite::Mask<(\d+,)?\s*\d+>{}")
        self.assertRegex(access, r"regilite::ReadWrite")
        self.assertRegex(key, r"struct\s*register_key")

        # Field type is properly declared during definition
        test_field = self.assertRegexExtractMatch(
            field_text,
            rf"(?s)struct\s+field_name\s*:\s*{test_base['name']}\s*{{(?P<body>.*)}};$",
        )

        # Field body contains a construct which delegates to base class
        self.assertRegex(
            test_field["body"],
            r"(explicit\s+constexpr|constexpr\s+explicit)\s+"
            rf"field_name\s*\(\s*{enum_field.name}_e\s+(?P<argument>\w+)\s*\)\s*"
            rf":\s*{test_base['name']}\s*\(\s*(?P=argument)\s*\)\s*{{\s*}}",
        )

        # Constexpr static member is created for each possible enum value
        for enum in enum_field.value_type:
            with self.subTest(enum=enum):
                self.assertRegex(
                    test_field["body"],
                    rf"(static\s+constexpr|constexpr\s+static)\s+"
                    rf"{test_base['name']}\s+{enum.name}\s*"
                    rf"{{\s*{enum_field.name}_e::{enum.name}\s*}};",
                )


if __name__ == "__main__":
    unittest.main()
