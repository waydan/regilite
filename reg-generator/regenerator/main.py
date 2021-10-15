# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 10:01:49 2021

@author: w6733
"""
import os
from xml.etree import ElementTree
import cmsisSvdParser
from generateHeader import generatePeripheral


def generateHeaders(file_name):
    device_xml = ElementTree.fromstring(open(file_name, 'r').read())
    peripherals = cmsisSvdParser.getAllPeripherals(device_xml)
    device_name = device_xml.find('name').text

    directory = os.path.join(os.getcwd(), device_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    for peripheral in peripherals:
        try:
            with open(os.path.join(directory, f'{peripheral.name}.hpp'), 'w') as header:
                header.write(generatePeripheral(peripheral, device_name))
        except:
            print(f'failed to generate {peripheral.name}.hpp')
            pass