# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 13:26:45 2021

@author: w6733
"""
import re
from jinja2 import Template
from functools import singledispatch
from .structuralModel import Struct, Register, Array, Union
from .. templates import TEMPLATES

def generatePeripheral(peripheral, device):
    return TEMPLATES['peripheral'].render(device=device,
                                          peripheral=peripheral,
                                          field_definitions=generateFields(listRegisters(peripheral.struct)),
                                          structure_definition=generate(peripheral.struct,
                                                                         typename=f'{peripheral.name}_t'))


@singledispatch
def generate(element, **kwargs):
    raise TypeError(f"Unrecognized argument type: {type(element)}")

@generate.register(Struct)
def _(struct, prefix=[], **kwargs):
    typename = kwargs['typename'] if 'typename' in kwargs else None
    insert_pos = 0
    reserved_cnt = 0
    member_list = []
    for member, position in struct.members:
        if position > insert_pos:
            member_list.append(TEMPLATES['padding'].render(size=position - insert_pos,
                                                           index=reserved_cnt))
            reserved_cnt += 1
        member_list.append(generate(member, prefix + [struct.name] if struct.name else prefix))
        insert_pos = position + member.sizeof()
    return TEMPLATES['struct'].render(struct=struct,
                                      member_list=member_list,
                                      type_name=typename)

@generate.register(Union)
def _(union, prefix=[], **kwargs):
    member_list = [generate(member, prefix + [union.name] if union.name else prefix)
                   for member, _ in union.members]
    return TEMPLATES['union'].render(union=union, member_list=member_list)

@generate.register(Array)
def _(array, prefix=[], **kwargs):
    element = re.match(r'^(?P<type>(?:.*?)[\}\s]\s*)'
                       '(?P<name>[_a-zA-z][_0-9a-zA-z]*)\s*$',
             generate(array.element, prefix), re.S)
    names = element['name'] + f'[{len(array.index)}]' \
        if isSequentialNumeric(array.index) \
            else ', '.join([element['name'] + str(i) for i in array.index])
    return TEMPLATES['array'].render(body=element['type'], names=names)

@generate.register(Register)
def _(register, prefix=[], **kwargs):
    return TEMPLATES['register'].render(register=register, reg_prefix=prefix)


def generateFields(register_list):
    return [generateRegisterFieldGroup(reg, prefix) for reg, prefix in register_list]

def generateRegisterFieldGroup(register, prefix):
    field_definitions = [TEMPLATES['field'].render(field=field,
                                                   register_key=register.name + '_')
                         for field in register.fields] if register.fields else []
    return TEMPLATES['decl_reg'].render(register=register, reg_prefix=prefix,
                                        field_definitions=field_definitions)


@singledispatch
def listRegisters(x, prefix=[]):
    """returns a flat generator of all Register objects in the peripheral"""
    raise TypeError(f"Unrecognized argument type: {type(x)}")

@listRegisters.register(Register)
def _(x, prefix=[]):
    yield (x, prefix)

@listRegisters.register(Struct)
@listRegisters.register(Union)
def _(x, prefix=[]):
    for member, _ in x.members:
        yield from listRegisters(member,
                                 prefix + [x.name] if x.name else prefix)

@listRegisters.register(Array)
def _(x, prefix=[]):
    yield from listRegisters(x.element, prefix)


def isSequentialNumeric(index: list):
    try:
        return all(map(lambda x: x[0] == x[1], zip(map(int, index), range(len(index)))))
    except ValueError:
        return False
