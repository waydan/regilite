"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import os
from xml.etree import ElementTree

from regenerator.generator import cppstruct, header
from regenerator.parser import cmsissvd


def read_register_definition_file(pathname) -> str:
    if not os.path.exists(pathname):
        raise FileNotFoundError(f"Could not find the file: {pathname}")
    with open(pathname, "r") as file:
        return file.read()


def main(file_name):
    device_xml = ElementTree.fromstring(open(file_name, "r").read())
    peripherals = cmsissvd.get_all_peripherals(device_xml)
    device_name = cmsissvd.get_device_name(device_xml)

    directory = os.path.join(os.getcwd(), device_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    for peripheral in peripherals:
        try:
            with open(os.path.join(directory, f"{peripheral.name}.hpp"), "w") as header:
                header.write(cppstruct.generate_peripheral(peripheral, device_name))
        except:
            print(f"failed to generate {peripheral.name}.hpp")
            pass
