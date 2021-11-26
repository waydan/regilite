"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
import re
from functools import reduce, singledispatch
from itertools import takewhile

from regenerator.model import members, types
from regenerator.utils import mbind


def getName(peripheral_elem):
    return mbind(
        peripheral_elem.find("groupName"),
        lambda x: x.text,
        peripheral_elem.find("name").text,
    )


def getAllPeripherals(device_elem):
    peripherals = {}
    for p_elem in device_elem.find("peripherals").findall("peripheral"):
        try:
            p_name = getName(p_elem)
            if p_name not in peripherals:
                peripherals[p_name] = getPeripheral(p_elem)
                peripherals[p_name].addInstance(
                    p_elem.find("name").text,
                    _strToUint(p_elem.find("baseAddress").text),
                )
        except Exception:
            print(f"failed with an error when parsing {p_name}")
            pass
    return list(peripherals.values())


def getPeripheral(peripheral_elem):
    peripheral_name = getName(peripheral_elem)
    return types.Peripheral(
        name=peripheral_name,
        structure=reduce(
            insertMember,
            sorted(
                (
                    getMember(register)
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


def joinMembers(a, b):
    if isinstance(a, members.DataMember):
        return _joinWithDataMember(a, b)
    elif isinstance(a, members.MemberArray):
        return _joinWithMemberArray(a, b)
    else:
        raise TypeError(f"Function requires a DataMember or MemberArray object")


def _joinWithDataMember(a, b):
    def _removeMemberPrefix(member, prefix: str):
        member.name = re.match(
            f"({re.escape(prefix)})?(_*)(?P<suffix>.+)", member.name
        ).group("suffix")
        return member

    def _adjustMemberOffset(member, offset_increment):
        member.offset += offset_increment
        return member

    if isinstance(a.type, types.Register):
        return reduce(
            _joinWithDataMember,
            (a, b),
            members.DataMember(
                type=types.Union() if _membersOverlap(a, b) else types.Struct(),
                name=_findCommonPrefix(a.name, b.name),
                offset=a.offset,
            ),
        )
    else:  # `a` is a Struct or Union
        a.type = insertMember(
            a.type,
            _adjustMemberOffset(_removeMemberPrefix(b, a.name), -a.offset),
        )
        return a


def _joinWithMemberArray(a, b):
    if a.isSimilarTo(b):
        a.member = joinMembers(a.member, b.member)
        return a
    else:
        return reduce(
            _joinWithDataMember,
            (a, b),
            members.DataMember(
                type=types.Union(),
                name=_findCommonPrefix(a.name, b.name),
                offset=a.offset,
            ),
        )


@singledispatch
def insertMember(any_type, member):
    raise TypeError(f"Type {type(any_type)} does not match the domain [Union | Struct]")


@insertMember.register(types.Struct)
def _(struct, member):
    if struct.members and _membersOverlap(struct.members[-1], member):
        return struct.addMember(joinMembers(struct.members.pop(), member))
    else:
        return struct.addMember(member)


@insertMember.register(types.Union)
def _(union, member):
    return union.addMember(member)


def getMember(register_elem):
    def isArray(register_elem):
        return register_elem.find("dim") != None

    def _offsetof(register_elem):
        return _strToUint(register_elem.find("addressOffset").text)

    register = getRegister(register_elem)
    data_member = members.DataMember(
        type=register,
        name=_getRegisterName(register_elem),
        offset=_offsetof(register_elem),
    )

    return (
        members.MemberArray(
            member=data_member,
            index=re.split(r",\s*", register_elem.find("dimIndex").text),
            increment=_strToUint(register_elem.find("dimIncrement").text),
        )
        if isArray(register_elem)
        else data_member
    )


def getRegister(register_elem):
    def getAllFields(register_elem):
        return mbind(
            register_elem.find("fields"),
            lambda fields: [getField(f) for f in fields.findall("field")],
            [],
        )

    return types.Register(
        name="x".join(re.split(r"{}", _getRegisterName(register_elem))),
        size=_strToUint(register_elem.find("size").text),
        reset_value=_strToUint(register_elem.find("resetValue").text),
        fields=getAllFields(register_elem),
        description=mbind(register_elem.find("description"), lambda x: x.text, ""),
    )


def getField(field_elem):
    def _getValueType(field_elem):
        return mbind(
            field_elem.find("enumeratedValues"),
            lambda enums: [getEnum(e) for e in enums.findall("enumeratedValue")],
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
        mask=((1 << _strToUint(field_elem.find("bitWidth").text)) - 1)
        << _strToUint(field_elem.find("bitOffset").text),
        access=_access_type_mapping[field_elem.find("access").text],
        value_type=_getValueType(field_elem),
        description=mbind(field_elem.find("description"), lambda x: x.text, ""),
    )


def getEnum(enum):
    def _makeId(name: str):
        _cpp_identifier = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")
        return name if _cpp_identifier.match(name) else "v" + name

    description = enum.find("description")
    return types.Enumeration(
        _makeId(enum.find("name").text),
        _strToUint(enum.find("value").text),
        description.text if description else "",
    )


def _strToUint(number: str):
    _uint_pattern = re.compile(
        r"[+]?((?P<hex>0x|0X)|(?P<bin>(#|0b)))?(?P<num>[a-fA-F\d]+)"
    )
    integer = _uint_pattern.match(number)
    return int(
        integer["num"], base=(16 if integer["hex"] else (2 if integer["bin"] else 10))
    )


def _membersOverlap(a, b):
    return a.offset + a.sizeof() > b.offset


def _findCommonPrefix(x: str, y: str):
    return "".join(
        char for char, _ in takewhile(lambda c: c[0] == c[1] and c[0] != "_", zip(x, y))
    )


def _getRegisterName(register_elem):
    return "{}".join(re.split("%s", register_elem.find("name").text))
