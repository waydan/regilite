"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree

from regenerator.model import types
from regenerator.parser import cmsissvd


class TestEnumParser(unittest.TestCase):
    """Tests the construction of an enumeration based on a name and value"""

    def test_read_name_and_value_from_svd(self):
        enum_xml = ElementTree.fromstring(
            """ <enumeratedValue>"""
            """     <name>enum_name</name>"""
            """     <value>#001</value>"""
            """ </enumeratedValue>"""
        )
        self.assertEqual(
            cmsissvd.get_enum(enum_xml), types.Enumeration(name="enum_name", value=1)
        )

    def test_append_v_to_numeric_name(self):
        enum_xml = ElementTree.fromstring(
            """ <enumeratedValue>"""
            """     <name>001</name>"""
            """     <value>#001</value>"""
            """ </enumeratedValue>"""
        )
        self.assertEqual(cmsissvd.get_enum(enum_xml).name, "v001")

    def test_description_included_when_present_in_svd(self):
        enum_xml = ElementTree.fromstring(
            """ <enumeratedValue>"""
            """     <name>001</name>"""
            """     <value>#001</value>"""
            """     <description>enum description</description>"""
            """ </enumeratedValue>"""
        )
        self.assertEqual(cmsissvd.get_enum(enum_xml).description, "enum description")


if __name__ == "__main__":
    unittest.main()
