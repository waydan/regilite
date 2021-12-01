"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import re
import unittest
from itertools import zip_longest

from regenerator.generator import cppstruct
from regenerator.model import types

from . import string_unittest_utils


class TestRegisterTypeGenerator(string_unittest_utils.TestCase):
    def test_register_type_alias_shows_size(self):
        for register_size in 8, 16, 32, 64:
            with self.subTest(register_size=register_size):
                self.assertRegex(
                    cppstruct.generate_register_field_group(
                        types.Register(name="r1", size=register_size)
                    ),
                    rf"using reg{register_size}_t =",
                )

    def test_fields_and_register_alias_wrapped_in_namespace(self):
        self.assertRegex(
            cppstruct.generate_register_field_group(types.Register(name="r1", size=32)),
            r"(?s)^(inline)?\s+namespace\s+r1_\s*{.*} // r1_$",
        )

    def test_storage_type_and_reset_value_included_in_register_alias(self):
        for size in 8, 16, 32:
            for reset_value in range(0, 2 ** size - 1, (2 ** size) // 3):
                with self.subTest(size=size, reset_value=reset_value):
                    self.assertRegex(
                        cppstruct.generate_register_field_group(
                            types.Register(
                                name="r1", size=size, reset_value=reset_value
                            )
                        ),
                        rf"(?m)^using \w+ = regilite::DefaultRegister<std::uint{size}_t, 0x{reset_value:X}>;$",
                    )

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
        register_type = self.assertRegexExtractMatch(
            cppstruct.generate_register_field_group(
                types.Register(
                    name="r2",
                    size=16,
                    reset_value=10,
                    fields=field_types,
                )
            ),
            r"(?m)^using\s+\w+\s*=\s*regilite::DefaultRegister<\s*(?P<parameters>.*?)\s*>;$",
        )
        _storage_type, _reset_value, *fields = re.split(
            r"\s*,\s*", register_type["parameters"]
        )

        # Each field appears exactly once as a template parameter
        for field_text, field_model in zip_longest(fields, field_types):
            with self.subTest(field_text=field_text):
                self.assertEqual(
                    field_text,
                    field_model.name,
                )


if __name__ == "__main__":
    unittest.main()
