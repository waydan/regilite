"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import re
from functools import singledispatch

from regenerator.generator import fieldtype
from regenerator.model import members, types
from regenerator.utils import mbind
from regenerator.templates import TEMPLATES


def get_register_namespace(register):
    return register.name + "_"


def fmt_data_member(member):
    def has_suffix(name):
        return bool(re.match(r"^\w+{}$", name))

    def get_member_name(member):
        if isinstance(member, members.MemberArray):
            return (
                member.name.format(f"[{len(member.index)}]")
                if has_suffix(member.name) and _is_sequential_numeric(member.index)
                else ", ".join([member.name.format(index) for index in member.index])
            )
        else:
            return member.name

    def get_description_comment(member_type):
        return (
            " // " + member_type.description
            if hasattr(member_type, "description") and member_type.description
            else ""
        )

    return "{type} {name};{description}".format(
        type=fmt_member_type(member.type),
        name=get_member_name(member),
        description=get_description_comment(member.type),
    )


@singledispatch
def fmt_member_type(model_type):
    raise TypeError(f"Unrecognized argument type: {type(model_type)}")


@fmt_member_type.register(types.Struct)
def _(struct):
    def list_members_with_padding(member_list):
        current_offset = 0
        padding_counter = 0
        for member in member_list:
            assert member.offset >= current_offset, (
                f"Trying to place member {member.name} at offset {member.offset} "
                f"but current position is {current_offset}"
            )
            if member.offset > current_offset:
                yield (
                    f"regilite::padding<{member.offset - current_offset}> _reserved_{padding_counter};"
                )
                padding_counter += 1
            yield fmt_data_member(member)
            current_offset = member.offset + member.sizeof()

    return TEMPLATES["struct_type"].render(
        struct=struct,
        data_member_list=list_members_with_padding(struct.members),
    )


@fmt_member_type.register(types.Union)
def _(union):
    return TEMPLATES["union_type"].render(
        union=union,
        data_member_list=[fmt_data_member(member) for member in union.members],
    )


@fmt_member_type.register(types.Register)
def _(register):
    return f"{get_register_namespace(register)}::reg{register.size}_t"


def generate_peripheral(peripheral):
    @singledispatch
    def list_registers(x):
        """returns a flat generator of all Register objects in the peripheral"""
        raise TypeError(f"Unrecognized argument type: {type(x)}")

    @list_registers.register(types.Register)
    def _(x):
        yield x

    @list_registers.register(types.Struct)
    @list_registers.register(types.Union)
    def _(x):
        for member in x.members:
            yield from list_registers(member.type)

    return TEMPLATES["peripheral"].render(
        peripheral=peripheral,
        field_definitions=mbind(
            peripheral.structure,
            lambda struct: (
                fmt_field_set(register) for register in list_registers(struct)
            ),
            (),
        ),
        structure_definition=mbind(
            peripheral.structure,
            fmt_member_type,
            "",
        ),
    )


def fmt_field_set(register):
    namespace = get_register_namespace(register)
    return TEMPLATES["decl_reg"].render(
        register_namespace=namespace,
        register=register,
        field_definitions=mbind(
            register.fields,
            lambda fields: (
                fieldtype.fmt_field(field=field, register_key=namespace)
                for field in fields
            ),
            (),
        ),
    )


def _is_sequential_numeric(index: list):
    try:
        return all(map(lambda x: x[0] == x[1], enumerate(map(int, index))))
    except ValueError:
        return False
