"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree

from regenerator.model import members, types
from regenerator.parser import cmsissvd


class TestCreateDataMember(unittest.TestCase):
    example_register = types.Register(name="register_name", size=32, reset_value=0)

    def test_read_data_member(self):
        member_xml = ElementTree.fromstring(
            """ <register>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <addressOffset>0x8</addressOffset>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        self.assertEqual(
            cmsissvd.get_member(member_xml),
            members.DataMember(
                type=self.example_register,
                name="register_name",
                offset=8,
            ),
        )

    def test_read_array_member(self):
        member_xml = ElementTree.fromstring(
            """ <register>"""
            """     <dim>3</dim>"""
            """     <dimIndex>1, 2, 3</dimIndex>"""
            """     <dimIncrement>0x4</dimIncrement>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <addressOffset>0</addressOffset>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        self.assertEqual(
            cmsissvd.get_member(member_xml),
            members.MemberArray(
                members.DataMember(
                    type=self.example_register, name="register_name", offset=0
                ),
                index=["1", "2", "3"],
                increment=4,
            ),
        ),

    def test_member_array_gets_formatable_name_from_register(self):
        member_xml = ElementTree.fromstring(
            """ <register>"""
            """     <dim>3</dim>"""
            """     <dimIndex>1, 2, 3</dimIndex>"""
            """     <dimIncrement>0x4</dimIncrement>"""
            """     <name>R%s</name>"""
            """     <size>32</size>"""
            """     <addressOffset>0</addressOffset>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        self.assertEqual(cmsissvd.get_member(member_xml).name, "R{}")


if __name__ == "__main__":
    unittest.main()
