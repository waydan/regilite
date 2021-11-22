"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree

from regenerator.parser import cmsissvd
from regenerator.model import types


class TestFieldParser(unittest.TestCase):
    def test_read_nonenum_field_from_svd(self):
        field_xml = ElementTree.fromstring(
            """ <field>"""
            """     <name>field_name</name>"""
            """     <bitOffset>8</bitOffset>"""
            """     <bitWidth>3</bitWidth>"""
            """     <access>read-write</access>"""
            """ </field>"""
        )
        field = cmsissvd.getField(field_xml)
        self.assertEqual(field, types.Field(name="field_name", mask=1792, access="RW"))

    def test_read_enum_field_from_svd(self):
        field_xml = ElementTree.fromstring(
            """ <field>"""
            """     <name>field_name</name>"""
            """     <bitOffset>8</bitOffset>"""
            """     <bitWidth>3</bitWidth>"""
            """     <access>read-write</access>"""
            """     <enumeratedValues>"""
            """         <enumeratedValue>"""
            """             <name>three</name>"""
            """             <value>#011</value>"""
            """         </enumeratedValue>"""
            """         <enumeratedValue>"""
            """             <name>six</name>"""
            """             <value>#110</value>"""
            """         </enumeratedValue>"""
            """     </enumeratedValues>"""
            """ </field>"""
        )
        field = cmsissvd.getField(field_xml)
        self.assertEqual(
            field,
            types.Field(
                name="field_name",
                mask=1792,
                access="RW",
                value_type=[
                    types.Enumeration(name="six", value=6),
                    types.Enumeration(name="three", value=3),
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
