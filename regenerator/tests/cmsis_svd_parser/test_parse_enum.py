"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree
from regenerator import cmsisSvdParser, structuralModel


class TestEnumParser(unittest.TestCase):
    """Tests the construction of an enumeration based on a name and value"""

    def test_read_name_and_value_from_svd(self):
        enum_xml = ElementTree.fromstring(
            ''' <enumeratedValue>'''
            '''     <name>enum_name</name>'''
            '''     <value>#001</value>'''
            ''' </enumeratedValue>''')
        print(type(enum_xml))
        enum = cmsisSvdParser.getEnum(enum_xml)
        self.assertEqual(enum, structuralModel.Enumeration(
            name='enum_name', value=1))

    def test_append_v_to_numeric_name(self):
        enum_xml = ElementTree.fromstring(
            ''' <enumeratedValue>'''
            '''     <name>001</name>'''
            '''     <value>#001</value>'''
            ''' </enumeratedValue>''')
        enum = cmsisSvdParser.getEnum(enum_xml)
        self.assertEqual('v001', enum.name)


if __name__ == "__main__":
    unittest.main()
