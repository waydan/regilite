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
        assert other.isArray()
        return self.index == other.index and self.increment == other.increment