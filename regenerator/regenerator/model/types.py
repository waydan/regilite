"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
import typing
from dataclasses import dataclass, field
from math import floor, log2


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
        assert self.mask > 0, "Field mask value may not be less-than or equal to zero"

    def msb(self):
        return int(log2(self.mask))

    def lsb(self):
        lsb = 0
        while self.mask & (1 << lsb) == 0:
            lsb += 1
        return lsb


@dataclass
class Register:
    name: str
    size: int
    reset_value: int = 0
    fields: "list[Field]" = field(default_factory=list)
    description: str = field(compare=False, default="")

    def __post_init__(self):
        def is_pow2(x):
            return floor(log2(x)) == log2(x)

        assert self.size != 0
        assert self.size % 8 == 0
        assert is_pow2(self.size)

    def sizeof(self):
        """returns size in bytes of object"""
        return self.size // 8

    def alignof(self):
        return self.sizeof()


@dataclass
class Struct:
    name: str = ""
    members: typing.Any = field(default_factory=list)

    def sizeof(self):
        """returns size in bytes of object"""
        return self.members[-1].offset + self.members[-1].sizeof()

    def alignof(self):
        return max(member.alignof() for member in self.members)

    def add_member(self, member):
        self.members.append(member)
        return self


@dataclass
class Union(object):
    name: str = ""
    members: typing.Any = field(default_factory=list)

    def sizeof(self):
        """returns size in bytes of object"""
        return max(
            _align_as(member.offset + member.sizeof(), self.alignof())
            for member in self.members
        )

    def alignof(self):
        return max(member.alignof() for member in self.members)

    def add_member(self, member):
        self.members.append(member)
        return self


@dataclass
class Peripheral:
    name: str
    structure: Struct = None
    instances: dict = field(default_factory=dict)

    def add_instance(self, name: str, address: int):
        if name in self.instances:
            raise RuntimeError(
                "{:s} is already included in the peripheral".format(name)
            )
        else:
            self.instances[name] = address


def _align_as(position: int, alignment: int):
    return (position + 1) // alignment * alignment
