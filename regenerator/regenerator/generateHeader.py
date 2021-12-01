"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import re
from dataclasses import dataclass
from functools import singledispatch

from templates import TEMPLATES

from regenerator.model import members, types
from regenerator.utils import mbind


def getRegisterNamespace(register):
    return register.name + "_"


def makeDataMember(member):
    def _hasSuffix(name):
        return bool(re.match(r"^\w+{}$", name))

    def _getMemberName(member):
        if isinstance(member, members.MemberArray):
            return (
                member.name.format(f"[{len(member.index)}]")
                if _hasSuffix(member.name) and isSequentialNumeric(member.index)
                else ", ".join([member.name.format(index) for index in member.index])
            )
        else:
            return member.name

    def _getDescriptionComment(member_type):
        return (
            " // " + member_type.description
            if hasattr(member_type, "description") and member_type.description
            else ""
        )

    return "{type} {name};{description}".format(
        type=generateType(member.type),
        name=_getMemberName(member),
        description=_getDescriptionComment(member.type),
    )


@singledispatch
def generateType(model_type):
    raise TypeError(f"Unrecognized argument type: {type(model_type)}")


@generateType.register(types.Struct)
def _(struct):
    member_data = []
    current_offset = 0
    padding_counter = 0
    for member in struct.members:
        assert member.offset >= current_offset, (
            f"Trying to place member {member.name} at offset {member.offset} "
            f"but current position is {current_offset}"
        )
        if member.offset > current_offset:
            member_data.append(
                f"regilite::padding<{member.offset - current_offset}> _reserved_{padding_counter};"
            )
            padding_counter += 1
        member_data.append(makeDataMember(member))
        current_offset = member.offset + member.sizeof()
    return TEMPLATES["struct_type"].render(
        struct=struct,
        data_member_list=member_data,
    )


@generateType.register(types.Union)
def _(union):
    return TEMPLATES["union_type"].render(
        union=union,
        data_member_list=[makeDataMember(member) for member in union.members],
    )


@generateType.register(types.Register)
def _(register):
    return f"{getRegisterNamespace(register)}::reg{register.sizeof()*8}_t"


def generatePeripheral(peripheral):
    return TEMPLATES["peripheral"].render(
        peripheral=peripheral,
        field_definitions=mbind(
            peripheral.structure, lambda s: generateFields(listRegisters(s)), []
        ),
        structure_definition=mbind(
            peripheral.structure,
            generateType,
            "",
        ),
    )


def generateFields(register_list):
    return [generateRegisterFieldGroup(register) for register in register_list]


def generateField(field, register_key=None):
    return TEMPLATES["field"].render(field=field, register_key=register_key)


def generateRegisterFieldGroup(register):
    namespace = getRegisterNamespace(register)
    return TEMPLATES["decl_reg"].render(
        register_namespace=namespace,
        register=register,
        field_definitions=mbind(
            register.fields,
            lambda fields: (
                generateField(field=field, register_key=namespace) for field in fields
            ),
            [],
        ),
    )


@singledispatch
def listRegisters(x):
    """returns a flat generator of all Register objects in the peripheral"""
    raise TypeError(f"Unrecognized argument type: {type(x)}")


@listRegisters.register(types.Register)
def _(x):
    yield x


@listRegisters.register(types.Struct)
@listRegisters.register(types.Union)
def _(x):
    for member in x.members:
        yield from listRegisters(member.type)


def isSequentialNumeric(index: list):
    try:
        return all(map(lambda x: x[0] == x[1], zip(map(int, index), range(len(index)))))
    except ValueError:
        return False
