from jinja2 import Template
from os import path

TEMPLATE_DIR = path.dirname(path.abspath(__file__))

TEMPLATES = {
    "header": Template(open(path.join(TEMPLATE_DIR, "header.stub")).read()),
    "peripheral": Template(open(path.join(TEMPLATE_DIR, "peripheral.stub")).read()),
    "decl_reg": Template(open(path.join(TEMPLATE_DIR, "decl_register.stub")).read()),
    "field": Template(open(path.join(TEMPLATE_DIR, "field.stub")).read()),
    "struct_type": Template(open(path.join(TEMPLATE_DIR, "struct_type.stub")).read()),
    "union_type": Template(open(path.join(TEMPLATE_DIR, "union_type.stub")).read()),
}
