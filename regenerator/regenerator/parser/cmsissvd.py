"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
import re
from functools import reduce, singledispatch
from itertools import takewhile

from regenerator.model import members, types
from regenerator.utils import mbind


def get_name(peripheral_elem):
    return mbind(
        peripheral_elem.find("groupName"),
        lambda x: x.text,
        peripheral_elem.find("name").text,
    )


def get_all_peripherals(device_elem):
    peripherals = {}
    for p_elem in device_elem.find("peripherals").findall("peripheral"):
        try:
            p_name = get_name(p_elem)
            if p_name not in peripherals:
                peripherals[p_name] = get_peripherals(p_elem)
                peripherals[p_name].add_instance(
                    p_elem.find("name").text,
                    _str_to_uint(p_elem.find("baseAddress").text),
                )
        except Exception:
            print(f"failed with an error when parsing {p_name}")
            pass
    return list(peripherals.values())


def get_peripherals(peripheral_elem):
    peripheral_name = get_name(peripheral_elem)
    return types.Peripheral(
        name=peripheral_name,
        structure=reduce(
            insert_member,
            sorted(
                (
                    get_member(register)
                    for register in mbind(
                        peripheral_elem.find("registers"),
                        lambda x: x.findall("register"),
                        [],
                    )
                ),
                key=lambda member: member.offset,
            ),
            types.Struct(name=peripheral_name + "_t"),
        ),
    )


def join_members(a, b):
    if isinstance(a, members.DataMember):
        return _join_with_data_member(a, b)
    elif isinstance(a, members.MemberArray):
        return _join_with_member_array(a, b)
    else:
        raise TypeError(f"Function requires a DataMember or MemberArray object")


def _join_with_data_member(a, b):
    def remove_member_prefix(member, prefix: str):
        member.name = re.match(
            f"({re.escape(prefix)})?(_*)(?P<suffix>.+)", member.name
        ).group("suffix")
        return member

    def adjust_member_offset(member, offset_increment):
        member.offset += offset_increment
        return member

    if isinstance(a.type, types.Register):
        return reduce(
            _join_with_data_member,
            (a, b),
            members.DataMember(
                type=types.Union() if _members_overlap(a, b) else types.Struct(),
                name=_find_common_prefix(a.name, b.name),
                offset=a.offset,
            ),
        )
    else:  # `a` is a Struct or Union
        a.type = insert_member(
            a.type,
            adjust_member_offset(remove_member_prefix(b, a.name), -a.offset),
        )
        return a


def _join_with_member_array(a, b):
    if a.is_similar_to(b):
        a.member = join_members(a.member, b.member)
        return a
    else:
        return reduce(
            _join_with_data_member,
            (a, b),
            members.DataMember(
                type=types.Union(),
                name=_find_common_prefix(a.name, b.name),
                offset=a.offset,
            ),
        )


@singledispatch
def insert_member(any_type, member):
    raise TypeError(f"Type {type(any_type)} does not match the domain [Union | Struct]")


@insert_member.register(types.Struct)
def _(struct, member):
    if struct.members and _members_overlap(struct.members[-1], member):
        return struct.add_member(join_members(struct.members.pop(), member))
    else:
        return struct.add_member(member)


@insert_member.register(types.Union)
def _(union, member):
    return union.add_member(member)


def get_member(register_elem):
    def is_array(register_elem):
        return register_elem.find("dim") != None

    def _offsetof(register_elem):
        return _str_to_uint(register_elem.find("addressOffset").text)

    register = get_register(register_elem)
    data_member = members.DataMember(
        type=register,
        name=_get_register_name(register_elem),
        offset=_offsetof(register_elem),
    )

    return (
        members.MemberArray(
            member=data_member,
            index=re.split(r",\s*", register_elem.find("dimIndex").text),
            increment=_str_to_uint(register_elem.find("dimIncrement").text),
        )
        if is_array(register_elem)
        else data_member
    )


def get_register(register_elem):
    def get_all_fields(register_elem):
        return mbind(
            register_elem.find("fields"),
            lambda fields: [get_field(f) for f in fields.findall("field")],
            [],
        )

    return types.Register(
        name="x".join(re.split(r"{}", _get_register_name(register_elem))),
        size=_str_to_uint(register_elem.find("size").text),
        reset_value=_str_to_uint(register_elem.find("resetValue").text),
        fields=get_all_fields(register_elem),
        description=mbind(register_elem.find("description"), lambda x: x.text, ""),
    )


def get_field(field_elem):
    def get_value_type(field_elem):
        return mbind(
            field_elem.find("enumeratedValues"),
            lambda enums: [get_enum(e) for e in enums.findall("enumeratedValue")],
            [],
        )

    _access_type_mapping = {
        "read-only": "RO",
        "write-only": "WO",
        "read-write": "RW",
        "oneToClear": "W1C",
    }
    return types.Field(
        name=field_elem.find("name").text,
        mask=((1 << _str_to_uint(field_elem.find("bitWidth").text)) - 1)
        << _str_to_uint(field_elem.find("bitOffset").text),
        access=_access_type_mapping[field_elem.find("access").text],
        value_type=get_value_type(field_elem),
        description=mbind(field_elem.find("description"), lambda x: x.text, ""),
    )


def get_enum(enum):
    def make_id(name: str):
        _cpp_identifier = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")
        return name if _cpp_identifier.match(name) else "v" + name

    return types.Enumeration(
        name=make_id(enum.find("name").text),
        value=_str_to_uint(enum.find("value").text),
        description=mbind(enum.find("description"), lambda x: x.text, ""),
    )


def _str_to_uint(number: str):
    _uint_pattern = re.compile(
        r"[+]?((?P<hex>0x|0X)|(?P<bin>(#|0b)))?(?P<num>[a-fA-F\d]+)"
    )
    integer = _uint_pattern.match(number)
    return int(
        integer["num"], base=(16 if integer["hex"] else (2 if integer["bin"] else 10))
    )


def _members_overlap(a, b):
    return a.offset + a.sizeof() > b.offset


def _find_common_prefix(x: str, y: str):
    return "".join(
        char for char, _ in takewhile(lambda c: c[0] == c[1] and c[0] != "_", zip(x, y))
    )


def _get_register_name(register_elem):
    return "{}".join(re.split("%s", register_elem.find("name").text))
