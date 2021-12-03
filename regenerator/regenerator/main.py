"""
Copyright 2021 Daniel Way
SPDX-License-Identifier: Apache-2.0
"""

import os
import argparse

from regenerator.generator import cppstruct, header
from regenerator.parser import cmsissvd


def read_register_definition_file(pathname) -> str:
    if not os.path.exists(pathname):
        raise FileNotFoundError(f"Could not find the file: {pathname}")
    with open(pathname, "r") as file:
        return file.read()


def export_header_file(dir_path, file_name, text):
    with open(
        os.path.join(
            dir_path,
            file_name,
        ),
        "w",
    ) as header:
        header.write(text)


def main():
    cli_input = argparse.ArgumentParser()
    cli_input.add_argument(
        "input_file",
        type=str,
        help="relative or absolue path to the register definition file",
    )
    cli_args = cli_input.parse_args()

    definition_text = cmsissvd.decode_file(
        read_register_definition_file(cli_args.input_file)
    )
    device_name = cmsissvd.get_device_name(definition_text)

    directory = os.path.join(os.getcwd(), device_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    assert os.path.exists(directory), f"Could not find directory {directory}"
    for peripheral in cmsissvd.get_all_peripherals(definition_text):
        try:
            export_header_file(
                directory,
                f"{peripheral.name}.hpp",
                header.fmt_header(
                    device_name=device_name,
                    peripheral_name=peripheral.name,
                    peripheral_body=cppstruct.generate_peripheral(peripheral),
                    includes=["<cstdint>", "<regilite/everyting.hpp>"],
                ),
            )
        except Exception as e:
            print(f"failed to generate {peripheral.name}.hpp")
            print(e)


if __name__ == "__main__":
    main()
