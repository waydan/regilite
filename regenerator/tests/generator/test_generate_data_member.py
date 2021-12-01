"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator.generator import cppstruct
from regenerator.model import members, types


class TestDataMember(unittest.TestCase):
    R1 = members.DataMember(
        type=types.Register(name="R1", size=32), name="R1", offset=0
    )
    R2 = members.DataMember(
        type=types.Register(name="R2", size=32, description="description"),
        name="R2",
        offset=0,
    )

    def test_creating_data_member_without_description(self):
        self.assertRegex(
            cppstruct.fmt_data_member(self.R1),
            r"^{}\s+R1;$".format(cppstruct.fmt_member_type(self.R1.type)),
        )

    def test_creating_data_member_with_description(self):
        self.assertRegex(
            cppstruct.fmt_data_member(self.R2),
            r"^{}\s+R2; *// description$".format(
                cppstruct.fmt_member_type(self.R2.type)
            ),
        )

    def test_creating_data_member_from_object_with_no_description_attribute(self):
        self.assertTrue(
            cppstruct.fmt_data_member(
                members.DataMember(type=types.Union(name="union"), name="", offset=0)
            )
        )


if __name__ == "__main__":
    unittest.main()
