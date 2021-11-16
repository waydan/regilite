"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

from typing import Any, Callable


def mbind(value: Any, fn: Callable, default):
    return fn(value) if value != None else default
