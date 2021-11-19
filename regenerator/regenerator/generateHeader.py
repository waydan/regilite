"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import re
from functools import singledispatch
from dataclasses import dataclass
from .utils import mbind
from .model.types import Struct, Register, Array, Union
from templates import TEMPLATES


def getRegisterNamespace(register):
    return register.typename + "_"


@dataclass
class DataMember:
    type: str
    name: str = ""
    description: str = ""

    def __str__(self):
        return f"{self.type} {self.name};{mbind(self.description, lambda d: f' // {d}', '')}"


@singledispatch
def makeDataMember(model_type):
    return DataMember(
        type=generateType(model_type),
        name=model_type.name,
        description=getattr(model_type, "description", ""),
    )


@makeDataMember.register(Array)
def _(array):
    def hasSuffix(name):
        return bool(re.match(r"^\w+{}$", name))

    data_member = makeDataMember(array.element)
    if hasSuffix(data_member.name) and isSequentialNumeric(array.index):
        data_member.name = data_member.name.format(f"[{len(array.index)}]")
    else:
        data_member.name = ", ".join(
            [data_member.name.format(index) for index in array.index]
        )
    return data_member


@singledispatch
def generateType(model_type):
    raise TypeError(f"Unrecognized argument type: {type(model_type)}")


@generateType.register(Struct)
def _(struct, typename=""):
    member_data = []
    current_offset = 0
    padding_counter = 0
    for member, member_offset in struct.members:
        if member_offset > current_offset:
            member_data.append(
                DataMember(
                    type=f"regilite::padding<{member_offset - current_offset}>",
                    name=f"_reserved_{padding_counter}",
                )
            )
            padding_counter += 1
        member_data.append(makeDataMember(member))
        current_offset += member_offset + member.sizeof()
    return TEMPLATES["struct_type"].render(
        struct=struct,
        typename=typename,
        data_member_list=[str(member) for member in member_data],
    )


@generateType.register(Union)
def _(union):
    member_data = [makeDataMember(member[0]) for member in union.members]
    return TEMPLATES["union_type"].render(
        union=union, data_member_list=[str(member) for member in member_data]
    )


@generateType.register(Register)
def _(register):
    return f"{getRegisterNamespace(register)}::reg{register.sizeof()*8}_t"


def generatePeripheral(peripheral):
    return TEMPLATES["peripheral"].render(
        peripheral=peripheral,
        field_definitions=generateFields(listRegisters(peripheral.structure)),
        structure_definition=generateType(
            peripheral.structure, typename=f"{peripheral.name}_t"
        ),
    )


def generateFields(register_list):
    return [generateRegisterFieldGroup(reg) for reg in register_list]


def generateField(field, register_key=None):
    return TEMPLATES["field"].render(field=field, register_key=register_key)


def generateRegisterFieldGroup(register):
    field_definitions = (
        [
            generateField(field=field, register_key=register.name + "_")
            for field in register.fields
        ]
        if register.fields
        else []
    )
    return TEMPLATES["decl_reg"].render(
        register=register, field_definitions=field_definitions
    )


@singledispatch
def listRegisters(x):
    """returns a flat generator of all Register objects in the peripheral"""
    raise TypeError(f"Unrecognized argument type: {type(x)}")


@listRegisters.register(Register)
def _(x):
    yield x


@listRegisters.register(Struct)
@listRegisters.register(Union)
def _(x):
    for member, _ in x.members:
        yield from listRegisters(member)


@listRegisters.register(Array)
def _(x):
    yield from listRegisters(x.element)


def isSequentialNumeric(index: list):
    try:
        return all(map(lambda x: x[0] == x[1], zip(map(int, index), range(len(index)))))
    except ValueError:
        return False
