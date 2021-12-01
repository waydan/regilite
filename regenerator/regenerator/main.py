"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import os
from xml.etree import ElementTree

from regenerator.generator.cppstruct import generate_peripheral
from regenerator.parser import cmsissvd


def cppstructs(file_name):
    device_xml = ElementTree.fromstring(open(file_name, "r").read())
    peripherals = cmsissvd.get_all_peripherals(device_xml)
    device_name = device_xml.find("name").text

    directory = os.path.join(os.getcwd(), device_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    for peripheral in peripherals:
        try:
            with open(os.path.join(directory, f"{peripheral.name}.hpp"), "w") as header:
                header.write(generate_peripheral(peripheral, device_name))
        except:
            print(f"failed to generate {peripheral.name}.hpp")
            pass
