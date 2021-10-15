# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 13:39:54 2021

@author: Daniel Way
@license: Apache 2.0
"""
import re
from functools import singledispatch
from .structuralModel import Peripheral, Struct, Union, Array, Register, Field, Enumeration


# Peripheral Parser
def getAllPeripherals(device_element):
    peripherals = {}
    for p_elem in device_element.find('peripherals').findall('peripheral'):
        try:
            p_name = getName(p_elem)
            if p_name not in peripherals:
                peripherals[p_name] = getPeripheral(p_elem)
                peripherals[p_name].addInstance(p_elem.find('name').text,
                                                strToUint(p_elem.find('baseAddress').text))
        except:
            print(f'failed with an error when parsing {p_name}')
            pass
    return peripherals.values()


def getPeripheral(peripheral_element):
    peripheral = Peripheral(name=getName(peripheral_element))
    register_list = peripheral_element.find('registers').findall('register')
    register_list.sort(key=offsetof)
    member_list = [getMember(register) for register in register_list]

    peripheral.struct.addMember(member_list.pop(0))
    for member in member_list:
        if membersOverlap(peripheral.struct.members[-1], member):
            peripheral.struct.addMember(joinMembers(*peripheral.struct.members.pop(),
                                                    *member))
        else:
            peripheral.struct.addMember(member)
    return peripheral

@singledispatch
def joinMembers(x, x_position, y, y_position):
    raise RuntimeError(f"Type {type(x)} does not match the domain "
                       "(Register, Array, Union, or Struct)")

@joinMembers.register(Array)
def _(x, x_position, y, y_position):
    assert(x_position <= y_position)
    if isinstance(y, Array) and x.similarTo(y):
        return (x.setElement(joinMembers(x.element, x_position,
                                         y.element, y_position)[0]), x_position)
    elif x_position == y_position:
        return (Union(None, [(x, 0), (y, 0)]), x_position)
    else:
        raise RuntimeError('Could not resolve dissimilar arrays '
                           f'{x.element.name} and {y.element.name}')

@joinMembers.register(Struct)
def _(x, x_position, y, y_position):
    assert(x_position <= y_position)
    y.name = removePrefix(x.name, y.name)
    y_position -= x_position
    if membersOverlap(x.members[-1], (y, y_position)):
        return (x.addMember(joinMembers(*x.members.pop(), y, y_position)), x_position)
    else:
        return (x.addMember((y, y_position)), x_position)

@joinMembers.register(Union)
def _(x, x_position, y, y_position):
    assert(x_position <= y_position)
    y.name = removePrefix(x.name, y.name)
    return (x.addMember((y, y_position - x_position)), x_position)

@joinMembers.register(Register)
def _(x, x_position, y, y_position):
    assert(x_position <= y_position)
    assert(isinstance(y, Register))
    common_prefix = getCommonPrefix(x.name, y.name)
    if not common_prefix:
        common_prefix = 'CONTROL'
    x.name = removePrefix(common_prefix, x.name)
    y.name = removePrefix(common_prefix, y.name)
    if membersOverlap((x, x_position), (y, y_position)):
        return (Union(common_prefix, [(x, 0), (y, y_position - x_position)]),
                x_position)
    else:
        return (Struct(common_prefix, [(x, 0), (y, y_position - x_position)]),
                x_position)


def getMember(register_elem):
    def getArray(register_elem):
        register, position = getRegister(register_elem)
        return (Array(index=getIndex(register_elem),
                      increment=strToUint(register_elem.find('dimIncrement').text),
                      element=register),
                position)
    def getRegister(register_elem):
        return (Register(name=''.join(re.split('%s', register_elem.find('name').text)),
                         size=strToUint(register_elem.find('size').text),
                         reset_value=strToUint(register_elem.find('resetValue').text),
                         fields=getAllFields(register_elem),
                         description=register_elem.find('description').text),
                offsetof(register_elem))
    return getArray(register_elem) if isArray(register_elem) else getRegister(register_elem)


# Field Parser
def getAllFields(register_elem):
    fields = register_elem.find('fields')
    return [getField(f) for f in fields.findall('field')] \
        if fields != None else None


def getField(field_elem):
    return Field(name=field_elem.find('name').text,
                 mask=((1 << strToUint(field_elem.find('bitWidth').text)) - 1)<<
                     strToUint(field_elem.find('bitOffset').text),
                 access=ACCESS_TYPE[field_elem.find('access').text],
                 value_type=getValueType(field_elem),
                 description=field_elem.find('description').text)




def getValueType(field_elem):
    enums = field_elem.find('enumeratedValues')
    return None if enums == None else \
        [getEnum(e) for e in enums.findall('enumeratedValue')]


# Enumeration Parser
def getEnum(enum):
    def makeId(name: str):
        return name if CPP_IDENTIFIER.match(name) else 'v' + name
    description = enum.find('description')
    return Enumeration(makeId(enum.find('name').text),
                       strToUint(enum.find('value').text),
                       description.text if description else "")



def strToUint(number: str):
    integer = UINT_PATTERN.match(number)
    return int(integer['num'], base=(16 if integer['hex'] \
                                     else (2 if integer['bin'] \
                                           else 10)))

def inGroup(peripheral_element):
    return peripheral_element.find('groupName') != None

def getName(peripheral_element):
    return peripheral_element.find('groupName').text \
            if peripheral_element.find('groupName') != None \
            else peripheral_element.find('name').text


def isArray (register_element):
    return register_element.find('dim') != None

def getIndex(register_element):
    return re.split(r',\s*', register_element.find('dimIndex').text)


def offsetof(register_element):
    return strToUint(register_element.find('addressOffset').text)

def membersOverlap(x, y):
    x_obj, x_position = x
    y_obj, y_position = y
    return x_position + x_obj.sizeof() > y_position

def getCommonPrefix(x: str, y: str):
    prefix = []
    for a, b in zip(x, y):
        if a != '_' and a == b:
            prefix.append(a)
        else:
            break
    return ''.join(prefix)

def removePrefix(prefix: str, string:str):
    return re.match(f'({re.escape(prefix)})?(_*)(?P<suffix>.+)',
                    string)['suffix']

ACCESS_TYPE = {'read-only': 'RO',
               'write-only': 'WO',
               'read-write': 'RW',
               'oneToClear': 'W1C'}


UINT_PATTERN = re.compile(r'[+]?'
                         r'((?P<hex>0x|0X)|(?P<bin>(#|0b)))?'
                         r'(?P<num>[a-fA-F\d]+)')

CPP_IDENTIFIER = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*')
