from jinja2 import Template
import os

TEMPLATE_DIR = os.path.dirname(__file__)

TEMPLATES = {
    "peripheral": Template(open(f"{TEMPLATE_DIR}/peripheral.stub").read()),
    "struct": Template(open(f"{TEMPLATE_DIR}/struct.stub").read()),
    "union": Template(open(f"{TEMPLATE_DIR}/union.stub").read()),
    "array": Template(open(f"{TEMPLATE_DIR}/array.stub").read()),
    "register": Template(open(f"{TEMPLATE_DIR}/register.stub").read()),
    "padding": Template(open(f"{TEMPLATE_DIR}/padding.stub").read()),
    "decl_reg": Template(open(f"{TEMPLATE_DIR}/decl_register.stub").read()),
    "field": Template(open(f"{TEMPLATE_DIR}/field.stub").read()),
    "struct_type": Template(open(f"{TEMPLATE_DIR}/struct_type.stub").read()),
    "union_type": Template(open(f"{TEMPLATE_DIR}/union_type.stub").read()),
}
