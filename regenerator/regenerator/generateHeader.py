"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import re
from jinja2 import Template
from functools import singledispatch
from .structuralModel import Struct, Register, Array, Union
from templates import TEMPLATES


def generatePeripheral(peripheral, device):
    return TEMPLATES["peripheral"].render(
        device=device,
        peripheral=peripheral,
        field_definitions=generateFields(listRegisters(peripheral.struct)),
        structure_definition=generate(
            peripheral.struct, typename=f"{peripheral.name}_t"
        ),
    )


@singledispatch
def generate(element, **kwargs):
    raise TypeError(f"Unrecognized argument type: {type(element)}")


@generate.register(Struct)
def _(struct, **kwargs):
    typename = kwargs["typename"] if "typename" in kwargs else None
    insert_pos = 0
    reserved_cnt = 0
    member_list = []
    for member, position in struct.members:
        if position > insert_pos:
            member_list.append(
                TEMPLATES["padding"].render(
                    size=position - insert_pos, index=reserved_cnt
                )
            )
            reserved_cnt += 1
        member_list.append(generate(member))
        insert_pos = position + member.sizeof()
    return TEMPLATES["struct"].render(
        struct=struct, member_list=member_list, type_name=typename
    )


@generate.register(Union)
def _(union, **kwargs):
    member_list = [generate(member) for member, _ in union.members]
    return TEMPLATES["union"].render(union=union, member_list=member_list)


@generate.register(Array)
def _(array, **kwargs):
    element = re.match(
        r"^(?P<type>(.*?)[\}\s]\s*)(?P<name>[_a-zA-z]\w*(?P<indexible>{})?\w*)\s*;(?P<description>\s*//.*)?$",
        generate(array.element),
        re.S,
    )
    names = (
        (
            element["name"].format(f"[{len(array.index)}]")
            if isSequentialNumeric(array.index) and re.search(r"{}$", element["name"])
            else ", ".join([element["name"].format(str(i)) for i in array.index])
        )
        if element["indexible"]
        else ", ".join([element["name"] + str(i) for i in array.index])
    )
    return TEMPLATES["array"].render(
        body=element["type"], names=names, description=element["description"]
    )


@generate.register(Register)
def _(register, **kwargs):
    return TEMPLATES["register"].render(register=register)


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
