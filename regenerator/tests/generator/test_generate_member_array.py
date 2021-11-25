"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest

from regenerator import generateHeader
from regenerator.model import members, types

Rx = members.DataMember(type=types.Register(name="Rx", size=32), name="R{}", offset=0)
RxR = members.DataMember(
    type=types.Register(name="RxR", size=32), name="R{}R", offset=0
)


class TestArrayMember(unittest.TestCase):
    def test_suffix_appended_to_register_name(self):
        self.assertRegex(
            generateHeader.makeDataMember(
                members.MemberArray(
                    member=Rx,
                    index=["1"],
                    increment=4,
                )
            ),
            r"R1;$",
        )

    def test_multiple_suffixed_names_appear_on_single_line(self):
        self.assertRegex(
            generateHeader.makeDataMember(
                members.MemberArray(
                    member=Rx,
                    index=["1", "2", "3"],
                    increment=4,
                )
            ),
            r"R1, R2, R3;$",
        )

    def test_use_array_syntax_when_index_is_sequential_and_zero_ordinal(self):
        self.assertRegex(
            generateHeader.makeDataMember(
                members.MemberArray(
                    member=Rx,
                    index=["0", "1", "2"],
                    increment=4,
                )
            ),
            r"R\[3\];$",
        )

    def test_do_not_use_array_syntax_for_infix(self):
        self.assertRegex(
            generateHeader.makeDataMember(
                members.MemberArray(
                    member=RxR,
                    index=["0", "1", "2"],
                    increment=4,
                )
            ),
            r"R0R, R1R, R2R;$",
        )

    def test_element_description_is_preserved(self):
        Rx_description = members.DataMember(
            type=types.Register(name="Rx", size=32, description="description"),
            name="R{}",
            offset=0,
        )
        self.assertRegex(
            generateHeader.makeDataMember(
                members.MemberArray(
                    member=Rx_description,
                    index=["1"],
                    increment=4,
                )
            ),
            rf"^{generateHeader.generateType(Rx.type)}\s+R1\s*;\s*//\s*description$",
        )


if __name__ == "__main__":
    unittest.main()
