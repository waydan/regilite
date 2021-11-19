"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
import typing
from dataclasses import dataclass, field, InitVar
from math import floor, log2
import re


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
    size: InitVar[int]
    reset_value: int = 0
    fields: "list[Field]" = field(default_factory=list)
    description: str = field(compare=False, default="")
    storage_type: Uint = field(init=False)

    def __post_init__(self, size):
        self.storage_type = Uint(size)
        self.name = "x".join(re.split(r"{}", self.name))

    def sizeof(self):
        """returns size in bytes of object"""
        return self.storage_type.sizeof()


@dataclass
class Struct:
    name: str = ""
    members: typing.Any = field(default_factory=list)

    def sizeof(self):
        """returns size in bytes of object"""
        return self.members[-1].position + self.members[-1].sizeof()

    def addMember(self, member):
        self.members.append(member)
        return self


@dataclass
class Union(object):
    name: str = ""
    members: typing.Any = field(default_factory=list)

    def sizeof(self):
        """returns size in bytes of object"""
        return max([position + member.sizeof() for member, position in self.members])

    def addMember(self, member):
        self.members.append(member)
        return self


@dataclass
class Peripheral:
    name: str
    structure: Struct = None
    instances: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.structure:
            self.structure = Struct(name=self.name + "_t")

    def addInstance(self, name: str, address: int):
        if name in self.instances:
            raise RuntimeError(
                "{:s} is already included in the peripheral".format(name)
            )
        else:
            self.instances[name] = address


class Array:
    pass
