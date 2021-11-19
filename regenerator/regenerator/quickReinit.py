"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import os
from xml.etree import ElementTree
from functools import singledispatch
from .cmsisSvdParser import getPeripheral
from .generateHeader import generatePeripheral, generateType
from .model.types import Struct, Union, Array, Register

CURRENT_DIR = os.path.dirname(__file__)


@singledispatch
def printStructure(s, prepend=""):
    print("<Unrecognized type!>")


@printStructure.register(Struct)
def _(s, prepend=""):
    print(f"{prepend}struct {s.name}")
    for m, _ in s.members:
        printStructure(m, prepend + "\t")


@printStructure.register(Register)
def _(s, prepend=""):
    print(f"{prepend}{s.name}")


@printStructure.register(Array)
def _(s, prepend=""):
    printStructure(s.element, prepend)
    print(f"{prepend}{s.index}")


@printStructure.register(Union)
def _(s, prepend=""):
    print(f"{prepend}union {s.name}")
    for m, _ in s.members:
        printStructure(m, prepend + "\t")


if __name__ == "__main__":
    ftm = getPeripheral(
        ElementTree.fromstring(
            open(f"{CURRENT_DIR}/../tests/test_peripheral.xml").read()
        )
    )
    ftm_full = getPeripheral(
        ElementTree.fromstring(open(f"{CURRENT_DIR}/../tests/test_ftm_full.xml").read())
    )
    spi = getPeripheral(
        ElementTree.fromstring(open(f"{CURRENT_DIR}/../tests/test_spi.xml").read())
    )
    pdb = getPeripheral(
        ElementTree.fromstring(open(f"{CURRENT_DIR}/../tests/test_pdb.xml").read())
    )
    mtbdwt = getPeripheral(
        ElementTree.fromstring(open(f"{CURRENT_DIR}/../tests/test_mtbdwt.xml").read())
    )
    dma = getPeripheral(
        ElementTree.fromstring(open(f"{CURRENT_DIR}/../tests/test_dma.xml").read())
    )
    sysctrl = getPeripheral(
        ElementTree.fromstring(open(f"{CURRENT_DIR}/../tests/test_sysctrl.xml").read())
    )

    print(generateType(pdb.structure))
    # print(generateType(dma.structure))

    # print(generatePeripheral(sysctrl, "mkv11z"))
