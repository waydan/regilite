# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 09:42:21 2021

@author: w6733
"""
from math import floor, log2

class Peripheral:
    def __init__(self, name: str):
        self.name = name
        self.struct = Struct(None, [])
        self.instances = {}
        
        
    def addInstance(self, name: str, address: int):
        if name in self.instances:
            raise RuntimeError("{:s} is already included in the peripheral".format(name))
        else:
            self.instances[name] = address


class Register:
    def __init__(self, name: str,size: int, reset_value: int, fields: list,
                 description: str):
        self.name = name
        self.storage_type = Uint(size)
        self.reset_value = reset_value
        self.fields = fields
        self.description = description

    def sizeof(self):
        """returns size in bytes of object"""
        return self.storage_type.sizeof()
 
    
class Struct:
    def __init__(self, name: str, members: list):
        self.name = name
        self.members = members
        
    def sizeof(self):
        """returns size in bytes of object"""
        return self.members[-1].position + self.members[-1].sizeof()
    
    def addMember(self, member):
        self.members.append(member)
        return self


class Union(object):
    def __init__(self, name: str, members: list):
        self.name = name
        self.members = members
        
    def sizeof(self):
        """returns size in bytes of object"""
        return max([position + member.sizeof() for member, position in self.members])
    
    def addMember(self, member):
        self.members.append(member)
        return self


class Array:
    def __init__(self, element, index: list, increment: int):
        self.element = element
        self.index = index
        self.increment = increment
        
    def setElement(self, element):
        self.element = element
        return self
    
    
    def sizeof(self):
        """returns size in bytes of object"""
        return self.increment * len(self.index)
    
    def similarTo(self, other):
        assert(type(other) == Array)
        return self.index == other.index and self.increment == other.increment


class Field:
    def __init__(self,name, value_type, mask: int, access: str,
                 description: str):
        self.name = name
        self.value_type = value_type
        self.mask = mask
        self.access = access
        self.description = description
        
    def msb(self):
        return int(log2(self.mask)) if self.mask != 0 else None
        
    def lsb(self):
        if self.mask == 0:
            return None
        lsb = 0
        while self.mask & (1 << lsb) == 0:
            lsb += 1
        return lsb
        
        
class Enumeration:
    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.description = description
        

class Uint:
    def __init__(self, size):
        def isPow2(x):
            return floor(log2(x)) == log2(x)
        assert(size % 8 == 0)
        assert(isPow2(size))
        self.size = size
        
    def sizeof(self):
        """returns size in bytes of object"""
        return self.size // 8