"""
Definitions of basic classes and types for the GCI Library
"""

from ctypes import *
from typing import Type

GciSession: Type[c_void_p] = c_void_p
OopType: Type[c_longlong] = c_int64

GCI_ERR_STR_SIZE = 1024
GCI_ERR_reasonSize = GCI_ERR_STR_SIZE
GCI_MAX_ERR_ARGS = 10
OOP_ILLEGAL = 1
OOP_NIL = 20

class GciErrSType(Structure):
    """
    see $GEMSTONE/include/gci.ht
    """

    _fields_ = [
        ('category',        OopType),   # error dictionary
        ('context',         OopType),   # a GsProcess
        ('exceptionObj',    OopType),   # an AbstractException or nil
        ('args',            OopType * GCI_MAX_ERR_ARGS),    # arguments
        ('number',          c_int),     # GemStone error number
        ('argCount',        c_int),     # num of arg in the args[]
        ('fatal',           c_ubyte),   # nonzero if err is fatal
        ('message',         c_char * (GCI_ERR_STR_SIZE + 1)),      # null-terminated Utf8
        ('reason',          c_char * (GCI_ERR_reasonSize + 1))     # null-terminated Utf8
    ]

    def __repr__(self):
        return 'aGciErrSType'

    def __str__(self):
        return 'GciErrSType(category=' + hex(self.category) +   \
               ', context=' + hex(self.context) +               \
               ', exceptionObj=' + hex(self.exceptionObj) +     \
               ', args=' + str(list(map(hex, self.args))[0:self.argCount]) +     \
               ', number=' + str(self.number) +                 \
               ', argCount=' + str(self.argCount) +             \
               ', fatal=' + str(self.fatal) +                   \
               ', message=' + str(self.message) +               \
               ', reason=' + str(self.reason) + ')'


class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidArgumentError(Error):
    """Invalid argument for GCI function"""
    pass

class GciException(Error):

    def __init__(self, ex: GciErrSType):
        super().__init__(str(ex.message))
        self.ex = ex

    def number(self):
        return self.ex.number

