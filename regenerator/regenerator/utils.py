"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

from functools import singledispatch
from typing import Any, Callable


@singledispatch
def mbind(value: Any, fn: Callable, default):
    return fn(value)


@mbind.register(type(None))
def _(value, fn: Callable, default):
    return default


@mbind.register(str)
@mbind.register(list)
def _(value, fn: Callable, default):
    return fn(value) if value else default
