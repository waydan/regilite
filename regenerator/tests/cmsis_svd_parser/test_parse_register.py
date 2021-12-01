"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree

from regenerator.model import types
from regenerator.parser import cmsissvd


class TestRegisterParser(unittest.TestCase):
    def test_read_register_from_svd(self):
        register_xml = ElementTree.fromstring(
            """ <register>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        register = cmsissvd.getRegister(register_xml)
        self.assertEqual(
            register,
            types.Register(name="register_name", size=32, reset_value=0),
        )

    def test_read_description_when_present(self):
        register_xml = ElementTree.fromstring(
            """ <register>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <resetValue>0</resetValue>"""
            """     <description>test description</description>"""
            """ </register>"""
        )
        register = cmsissvd.getRegister(register_xml)
        self.assertEqual(register.description, "test description")

    def test_array_index_replaced_by_lowercase_x(self):
        register_xml = ElementTree.fromstring(
            """ <register>"""
            """     <dim>3</dim>"""
            """     <dimIndex>1, 2, 3</dimIndex>"""
            """     <dimIncrement>0x4</dimIncrement>"""
            """     <name>R%sR</name>"""
            """     <size>32</size>"""
            """     <addressOffset>0</addressOffset>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        self.assertEqual(cmsissvd.getRegister(register_xml).name, "RxR")


if __name__ == "__main__":
    unittest.main()
