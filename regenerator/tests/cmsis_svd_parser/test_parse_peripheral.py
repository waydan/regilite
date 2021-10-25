"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree
from regenerator import cmsisSvdParser, structuralModel


class TestPeripheralParser(unittest.TestCase):
    def test_read_peripheral_from_svd(self):
        peripheral_xml = ElementTree.fromstring(
            """ <peripheral>"""
            """     <name>peripheral_name</name>"""
            """ </peripheral>"""
        )
        peripheral = cmsisSvdParser.getPeripheral(peripheral_xml)
        self.assertEqual(
            peripheral,
            structuralModel.Peripheral(name="peripheral_name"),
        )

    def test_read_peripheral_with_single_register(self):
        peripheral_xml = ElementTree.fromstring(
            """ <peripheral>"""
            """     <name>peripheral_name</name>"""
            """     <registers>"""
            """         <register>"""
            """             <name>a_reg</name>"""
            """             <size>8</size>"""
            """             <resetValue>0</resetValue>"""
            """             <addressOffset>0x0</addressOffset>"""
            """         </register>"""
            """     </registers>"""
            """ </peripheral>"""
        )
        peripheral = cmsisSvdParser.getPeripheral(peripheral_xml)
        self.assertEqual(
            peripheral,
            structuralModel.Peripheral(
                name="peripheral_name",
                structure=structuralModel.Struct(
                    name="",
                    members=[
                        (
                            structuralModel.Register(
                                name="a_reg", reset_value=0, size=8
                            ),
                            0,
                        )
                    ],
                ),
            ),
        )

    def test_read_peripheral_with_multiple_registers(self):
        peripheral_xml = ElementTree.fromstring(
            """ <peripheral>"""
            """     <name>peripheral_name</name>"""
            """     <registers>"""
            """         <register>"""
            """             <name>a_reg</name>"""
            """             <size>8</size>"""
            """             <resetValue>0</resetValue>"""
            """             <addressOffset>0x0</addressOffset>"""
            """         </register>"""
            """         <register>"""
            """             <name>b_reg</name>"""
            """             <size>8</size>"""
            """             <resetValue>0</resetValue>"""
            """             <addressOffset>0x1</addressOffset>"""
            """         </register>"""
            """     </registers>"""
            """ </peripheral>"""
        )
        peripheral = cmsisSvdParser.getPeripheral(peripheral_xml)
        self.assertEqual(
            peripheral,
            structuralModel.Peripheral(
                name="peripheral_name",
                structure=structuralModel.Struct(
                    name="",
                    members=[
                        (
                            structuralModel.Register(
                                name="a_reg", size=8, reset_value=0
                            ),
                            0,
                        ),
                        (
                            structuralModel.Register(
                                name="b_reg", size=8, reset_value=0
                            ),
                            1,
                        ),
                    ],
                ),
            ),
        )

    def test_read_peripheral_group_from_svd(self):
        peripheral_xml = ElementTree.fromstring(
            """ <device>"""
            """ <peripherals>"""
            """     <peripheral>"""
            """         <name>peripheral123</name>"""
            """         <groupName>peripheral_group</groupName>"""
            """         <baseAddress>0xC0FFEE</baseAddress>"""
            """     </peripheral>"""
            """ </peripherals>"""
            """ </device>"""
        )
        peripheral = cmsisSvdParser.getAllPeripherals(peripheral_xml)
        self.assertEqual(
            peripheral[0],
            structuralModel.Peripheral(
                name="peripheral_group", instances={"peripheral123": 0xC0FFEE}
            ),
        )


if __name__ == "__main__":
    unittest.main()
