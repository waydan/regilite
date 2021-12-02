"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""
from templates import TEMPLATES


def fmt_header(device_name, peripheral_name, peripheral_body, includes):
    return TEMPLATES["header"].render(
        device_name=device_name,
        peripheral_name=peripheral_name,
        peripheral_body=peripheral_body,
        includes=includes,
    )
