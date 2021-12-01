"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import unittest
from xml.etree import ElementTree

from regenerator.model import members, types
from regenerator.parser import cmsissvd


class TestPeripheralParser(unittest.TestCase):
    def test_read_peripheral_from_svd(self):
        peripheral_xml = ElementTree.fromstring(
            """ <peripheral>"""
            """     <name>peripheral_name</name>"""
            """ </peripheral>"""
        )
        peripheral = cmsissvd.get_peripherals(peripheral_xml)
        self.assertEqual(
            peripheral,
            types.Peripheral(
                name="peripheral_name", structure=types.Struct(name="peripheral_name_t")
            ),
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
        peripheral = cmsissvd.get_peripherals(peripheral_xml)
        self.assertEqual(
            peripheral,
            types.Peripheral(
                name="peripheral_name",
                structure=types.Struct(
                    name="peripheral_name_t",
                    members=[
                        members.DataMember(
                            type=types.Register(name="a_reg", size=8, reset_value=0),
                            name="a_reg",
                            offset=0,
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
        peripheral = cmsissvd.get_peripherals(peripheral_xml)
        self.assertEqual(
            peripheral,
            types.Peripheral(
                name="peripheral_name",
                structure=types.Struct(
                    name="peripheral_name_t",
                    members=[
                        members.DataMember(
                            type=types.Register(name="a_reg", size=8, reset_value=0),
                            name="a_reg",
                            offset=0,
                        ),
                        members.DataMember(
                            type=types.Register(name="b_reg", size=8, reset_value=0),
                            name="b_reg",
                            offset=1,
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
        peripheral = cmsissvd.get_all_peripherals(peripheral_xml)
        self.assertEqual(
            peripheral[0],
            types.Peripheral(
                name="peripheral_group",
                structure=types.Struct(name="peripheral_group_t"),
                instances={"peripheral123": 0xC0FFEE},
            ),
        )


if __name__ == "__main__":
    unittest.main()
