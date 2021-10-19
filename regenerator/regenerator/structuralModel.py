"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

from dataclasses import dataclass, field, InitVar
from math import floor, log2


class Peripheral:
    def __init__(self, name: str):
        self.name = name
        self.struct = Struct(None, [])
        self.instances = {}

    def addInstance(self, name: str, address: int):
        if name in self.instances:
            raise RuntimeError(
                "{:s} is already included in the peripheral".format(name)
            )
        else:
            self.instances[name] = address


@dataclass
class Uint:
    size: int

    def __post_init__(self):
        def isPow2(x):
            return floor(log2(x)) == log2(x)

        assert self.size != 0
        assert self.size % 8 == 0
        assert isPow2(self.size)

    def sizeof(self):
        """returns size in bytes of object"""
        return self.size // 8


@dataclass
class Enumeration:
    name: str
    value: int
    description: str = field(compare=False, default="")


@dataclass
class Field:
    name: str
    mask: int
    access: str
    value_type: "list[Enumeration]" = field(compare=False, default_factory=list)
    description: str = field(compare=False, default="")

    def __post_init__(self):
        self.value_type.sort(key=lambda x: x.value)

    def msb(self):
        return int(log2(self.mask)) if self.mask != 0 else None

    def lsb(self):
        if self.mask == 0:
            return None
        lsb = 0
        while self.mask & (1 << lsb) == 0:
            lsb += 1
        return lsb


@dataclass
class Register:
    name: str
    size: InitVar[int]
    reset_value: int
    fields: "list[Field]" = field(default_factory=list)
    description: str = field(compare=False, default="")
    storage_type: Uint = None

    def __post_init__(self, size):
        self.storage_type = Uint(size)

    def sizeof(self):
        """returns size in bytes of object"""
        return self.storage_type.sizeof()


class Struct:
    def __init__(self, name: str, members: list):
        self.name = name
        self.members = members

    def sizeof(self):
        """returns size in bytes of object"""
        return self.members[-1].position + self.members[-1].sizeof()

    def addMember(self, member):
        self.members.append(member)
        return self


class Union(object):
    def __init__(self, name: str, members: list):
        self.name = name
        self.members = members

    def sizeof(self):
        """returns size in bytes of object"""
        return max([position + member.sizeof() for member, position in self.members])

    def addMember(self, member):
        self.members.append(member)
        return self


@dataclass
class Array:
    index: "list[str]"
    increment: int
    element: "Union[Struct, Union, Register]"

    def setElement(self, element):
        self.element = element
        return self

    def sizeof(self):
        """returns size in bytes of object"""
        return self.increment * len(self.index)

    def similarTo(self, other):
        assert type(other) == Array
        return self.index == other.index and self.increment == other.increment
