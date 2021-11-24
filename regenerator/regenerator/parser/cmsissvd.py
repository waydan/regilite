"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
import re
from functools import singledispatch
from regenerator.utils import mbind
from regenerator.model import types, members


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
                    p_elem.find("name").text, strToUint(p_elem.find("baseAddress").text)
                )
        except Exception:
            print(f"failed with an error when parsing {p_name}")
            pass
    return list(peripherals.values())


def getPeripheral(peripheral_elem):
    peripheral = types.Peripheral(name=getName(peripheral_elem))
    peripheral.structure = types.Struct(name=peripheral.name + "_t")
    register_list = mbind(
        peripheral_elem.find("registers"), lambda x: x.findall("register"), []
    )
    register_list.sort(key=offsetof)
    for member in [getMember(register) for register in register_list]:
        peripheral.structure = insertMember(peripheral.structure, member)
    return peripheral


def joinMembers(a, b):
    if isinstance(a, members.DataMember):
        return _joinWithDataMember(a, b)
    elif isinstance(a, members.MemberArray):
        return _joinWithMemberArray(a, b)
    else:
        raise TypeError(f"Function requires a DataMember or MemberArray object")


def _joinWithDataMember(a, b):
    def renameMember(member, func):
        member.name = func(member.name)
        return member

    def adjustMemberOffset(member, offset_increment):
        member.offset += offset_increment
        return member

    if isinstance(a.type, types.Register):
        a = joinMembers(
            members.DataMember(
                type=types.Union() if membersOverlap(a, b) else types.Struct(),
                name=getCommonPrefix(a.name, b.name),
                offset=a.offset,
            ),
            a,
        )
    # Intentional `if` fallthrough
    # `a` is a type.Struct or types.Union
    a.type = insertMember(
        a.type,
        adjustMemberOffset(
            renameMember(b, lambda n: removePrefix(a.name, n)), -a.offset
        ),
    )
    return a


def _joinWithMemberArray(a, b):
    if a.isSimilarTo(b):
        a.member = joinMembers(a.member, b.member)
        return a
    else:
        return _joinWithDataMember(
            _joinWithDataMember(
                members.DataMember(
                    type=types.Union(),
                    name=getCommonPrefix(a.name, b.name),
                    offset=a.offset,
                ),
                a,
            ),
            b,
        )


@singledispatch
def insertMember(any_type, member):
    raise TypeError(f"Type {type(any_type)} does not match the domain [Union | Struct]")


@insertMember.register(types.Struct)
def _(struct, member):
    if struct.members and membersOverlap(struct.members[-1], member):
        return struct.addMember(joinMembers(struct.members.pop(), member))
    else:
        return struct.addMember(member)


@insertMember.register(types.Union)
def _(union, member):
    return union.addMember(member)


def getMember(register_elem):
    def isArray(register_elem):
        return register_elem.find("dim") != None

    register = getRegister(register_elem)
    data_member = members.DataMember(
        type=register, name=register.name, offset=offsetof(register_elem)
    )

    return (
        members.MemberArray(
            member=data_member,
            index=re.split(r",\s*", register_elem.find("dimIndex").text),
            increment=strToUint(register_elem.find("dimIncrement").text),
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
        name="{}".join(re.split("%s", register_elem.find("name").text)),
        size=strToUint(register_elem.find("size").text),
        reset_value=strToUint(register_elem.find("resetValue").text),
        fields=getAllFields(register_elem),
        description=mbind(register_elem.find("description"), lambda x: x.text, ""),
    )


def getArray(register_elem):
    def getIndex(register_elem):
        return re.split(r",\s*", register_elem.find("dimIndex").text)

    return types.Array(
        index=getIndex(register_elem),
        increment=strToUint(register_elem.find("dimIncrement").text),
        element=getRegister(register_elem),
    )


def getField(field_elem):
    def getValueType(field_elem):
        return mbind(
            field_elem.find("enumeratedValues"),
            lambda enums: [getEnum(e) for e in enums.findall("enumeratedValue")],
            [],
        )

    return types.Field(
        name=field_elem.find("name").text,
        mask=((1 << strToUint(field_elem.find("bitWidth").text)) - 1)
        << strToUint(field_elem.find("bitOffset").text),
        access=ACCESS_TYPE[field_elem.find("access").text],
        value_type=getValueType(field_elem),
        description=mbind(field_elem.find("description"), lambda x: x.text, ""),
    )


def getEnum(enum):
    def makeId(name: str):
        return name if _CPP_IDENTIFIER.match(name) else "v" + name

    description = enum.find("description")
    return types.Enumeration(
        makeId(enum.find("name").text),
        strToUint(enum.find("value").text),
        description.text if description else "",
    )


def strToUint(number: str):
    integer = _UINT_PATTERN.match(number)
    return int(
        integer["num"], base=(16 if integer["hex"] else (2 if integer["bin"] else 10))
    )


def offsetof(register_elem):
    return strToUint(register_elem.find("addressOffset").text)


def membersOverlap(a, b):
    return a.offset + a.sizeof() > b.offset


def getCommonPrefix(x: str, y: str):
    prefix = []
    for a, b in zip(x, y):
        if a != "_" and a == b:
            prefix.append(a)
        else:
            break
    return "".join(prefix)


def removePrefix(prefix: str, string: str):
    return re.match(f"({re.escape(prefix)})?(_*)(?P<suffix>.+)", string)["suffix"]


def renameMember(member, renaming_fn):
    member.name = renaming_fn(member.name)


ACCESS_TYPE = {
    "read-only": "RO",
    "write-only": "WO",
    "read-write": "RW",
    "oneToClear": "W1C",
}

_UINT_PATTERN = re.compile(
    r"[+]?" r"((?P<hex>0x|0X)|(?P<bin>(#|0b)))?" r"(?P<num>[a-fA-F\d]+)"
)

_CPP_IDENTIFIER = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")
