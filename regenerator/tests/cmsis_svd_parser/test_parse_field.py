"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree
from regenerator import cmsisSvdParser, structuralModel


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
        field = cmsisSvdParser.getField(field_xml)
        self.assertEqual(
            field, structuralModel.Field(name="field_name", mask=1792, access="RW")
        )

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
        field = cmsisSvdParser.getField(field_xml)
        self.assertEqual(
            field,
            structuralModel.Field(
                name="field_name",
                mask=1792,
                access="RW",
                value_type=[
                    structuralModel.Enumeration(name="six", value=6),
                    structuralModel.Enumeration(name="three", value=3),
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
