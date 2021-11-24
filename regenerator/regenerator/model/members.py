"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
from dataclasses import dataclass, field
import typing
from regenerator.model import types


@dataclass
class DataMember:
    type: typing.Union[types.Register, types.Struct, types.Union]
    name: str
    offset: int

    def sizeof(self):
        return self.type.sizeof()

    def rename(self, func):
        self.name = func(self.name)
        return self


@dataclass
class MemberArray:
    member: DataMember
    index: "list[str]"
    increment: int

    def sizeof(self):
        return self.increment * len(self.index)

    def isSimilarTo(self, other):
        return (
            isinstance(other, MemberArray)
            and self.index == other.index
            and self.increment == other.increment
        )

    def __getattr__(self, __name: str):
        return getattr(self.member, __name)

    def __setattr__(self, __name: str, __value):
        # allow write access to DataMember 'name' and 'offset' attributes
        if __name in ["name", "offset"]:
            setattr(self.member, __name, __value)
        else:
            self.__dict__[__name] = __value
