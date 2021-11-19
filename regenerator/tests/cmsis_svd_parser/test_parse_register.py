"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree
from regenerator import cmsisSvdParser
from regenerator.model import types


class TestRegisterParser(unittest.TestCase):
    def test_read_register_from_svd(self):
        register_xml = ElementTree.fromstring(
            """ <register>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        register = cmsisSvdParser.getRegister(register_xml)
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
        register = cmsisSvdParser.getRegister(register_xml)
        self.assertEqual(register.description, "test description")


if __name__ == "__main__":
    unittest.main()
