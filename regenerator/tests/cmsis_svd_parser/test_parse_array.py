"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree
from regenerator import cmsisSvdParser, structuralModel


class TestArrayParser(unittest.TestCase):
    def test_read_array_from_svd(self):
        array_xml = ElementTree.fromstring(
            """ <register>"""
            """     <dim>3</dim>"""
            """     <dimIndex>1, 2, 3</dimIndex>"""
            """     <dimIncrement>0x4</dimIncrement>"""
            """     <name>register_name</name>"""
            """     <name>register_name</name>"""
            """     <size>32</size>"""
            """     <resetValue>0</resetValue>"""
            """ </register>"""
        )
        array = cmsisSvdParser.getArray(array_xml)
        self.assertEqual(
            array,
            structuralModel.Array(
                increment=4,
                index=["1", "2", "3"],
                element=structuralModel.Register(
                    name="register_name", size=32, reset_value=0
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
