"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
from regenerator.templates import TEMPLATES


def fmt_field(field, register_key=None):
    return TEMPLATES["field"].render(field=field, register_key=register_key)
