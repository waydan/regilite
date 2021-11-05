"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
import re
from . import string_unittest_utils
from regenerator import structuralModel, generateHeader


class TestRegisterTypeGenerator(string_unittest_utils.TestCase):
    def test_generating_register_type_without_fields(self):
        register_namespace = self.assertRegexExtractMatch(
            generateHeader.generateRegisterFieldGroup(
                structuralModel.Register(name="r1", size=32, reset_value=0)
            ),
            r"^(inline)?\s+namespace\s+r1_\s*{(?P<type_alias>.*)}",
            re.S,
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
            structuralModel.Field(name="f0", mask=1, access="WriteOnly"),
            structuralModel.Field(
                name="f1",
                mask=0b110,
                access="ReadOnly",
                value_type=[structuralModel.Enumeration(name="e0", value=0)],
            ),
        ]
        register_namespace = self.assertRegexExtractMatch(
            generateHeader.generateRegisterFieldGroup(
                structuralModel.Register(
                    name="r2",
                    size=16,
                    reset_value=10,
                    fields=field_types,
                )
            ),
            r"^(inline)?\s+namespace\s+r2_\s*{(?P<fields_and_register>.*)}",
            re.S,
        )
        register_type = self.assertRegexExtractMatch(
            register_namespace["fields_and_register"],
            r"using\s+reg\s*=\s*regilite::DefaultRegister<\s*(?P<parameters>.*?)\s*>;",
        )
        storage_type, reset_value, *fields = re.split(
            r"\s*,\s*", register_type["parameters"]
        )
        self.assertRegex(storage_type, r"^std::uint16_t$")
        self.assertRegex(reset_value, r"^(10|0b0*1010|0x0*A)$")

        # Each field appears exactly once as a template parameter
        for field_text, field_model in zip(fields, field_types):
            self.assertRegex(
                field_text,
                rf"\b{field_model.name}{'_' if field_model.value_type else ''}\b",
            )

    def test_generating_register_type_for_array(self):
        self.assertRegex(
            generateHeader.generateRegisterFieldGroup(
                structuralModel.Register(name="REGISTER{}_TYPE", size=32, reset_value=0)
            ),
            r"^(inline)?\s+namespace\s+REGISTERx_TYPE_\s*{.*}(?s)",
        )


if __name__ == "__main__":
    unittest.main()
