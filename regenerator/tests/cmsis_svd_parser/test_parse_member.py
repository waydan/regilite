"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree
from regenerator import cmsisSvdParser, structuralModel


class TestArrayParser(unittest.TestCase):
    def test_read_register_member_register_tuple(self):
        member_xml = ElementTree.fromstring(
            """ <register>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <addressOffset>0x8</addressOffset>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        member = cmsisSvdParser.getMember(member_xml)
        self.assertEqual(
            member,
            (structuralModel.Register(name="register_name", size=32, reset_value=0), 8),
        )

    def test_read_register_member_tuple(self):
        member_xml = ElementTree.fromstring(
            """ <register>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <addressOffset>0x8</addressOffset>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        member = cmsisSvdParser.getMember(member_xml)
        self.assertEqual(
            member,
            (structuralModel.Register(name="register_name", size=32, reset_value=0), 8),
        )

    def test_read_array_member_tuple(self):
        member_xml = ElementTree.fromstring(
            """ <register>"""
            """     <dim>3</dim>"""
            """     <dimIndex>1, 2, 3</dimIndex>"""
            """     <dimIncrement>0x4</dimIncrement>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <addressOffset>0x8</addressOffset>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        member = cmsisSvdParser.getMember(member_xml)
        self.assertEqual(
            member,
            (
                structuralModel.Array(
                    increment=4,
                    index=["1", "2", "3"],
                    element=structuralModel.Register(
                        name="register_name", size=32, reset_value=0
                    ),
                ),
                8,
            ),
        )


if __name__ == "__main__":
    unittest.main()
