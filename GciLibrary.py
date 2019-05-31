"""
>>> # See $GEMSTONE/include/gcits.hf for details

>>> gci = GciLibrary()
>>> isinstance(gci, GciLibrary)
True

>>> gci.version()
'3.4.3 build gss64_3_4_x_branch-45183'

>>> gci.oopToChar(16668)
65

>>> gci.oopToChar(16667)
-1

>>> gci.oopToChar(24860)  # $a
97

>>> gci.charToOop(65)
16668

>>> gci.charToOop(97) # $a
24860

>>> gci.charToOop(1114111)
285212444

>>> gci.charToOop(1114112)
1

>>> try:
...     gci.doubleToSmallDouble(1.0)
... except InvalidArgumentError:
...     "InvalidArgumentError"
9151314442816847878

>>> try:
...     gci.doubleToSmallDouble(1e40)
... except InvalidArgumentError:
...     "InvalidArgumentError"
'InvalidArgumentError'

>>> gci.I32ToOop(0)
2

>>> gci.I32ToOop(55)
442



>>> try:
...     gci.login(netldi='gs64ldi99', stone='gs64stone4')
... except GciException as ex:
...     ex.number()     # invalid NetLDI
4147

>>> try:
...     gci.login(netldi='gs64ldi', stone='gs64stone44')
... except GciException as ex:
...     ex.number()     # invalid stone
4065

>>> try:
...     gci.login(netldi='gs64ldi', stone='gs64stone', gs_user='fred')
... except GciException as ex:
...     ex.number()     # invalid user/password
4051

>>> session = gci.login(netldi='gs64ldi', stone='gs64stone')
>>> isinstance(session, int)      # successful login
True

>>> gci.is_session_valid(session)
True

>>> try:
...     gci.abort(session)
... except GciException as ex:
...     ex.number()

>>> try:
...     gci.logout(session)
... except GciException as ex:
...     ex.number()     # invalid session

>>> gci.is_session_valid(session)
False

>>> try:
...     gci.logout(session)
... except GciException as ex:
...     ex.number()     # invalid session
4100

>>> try:
...     gci.abort(session)
... except GciException as ex:
...     ex.number()
4100
"""

from ctypes import *
from typing import Type

GciSession: Type[c_void_p] = c_void_p
OopType: Type[c_longlong] = c_int64

GCI_ERR_STR_SIZE = 1024
GCI_ERR_reasonSize = GCI_ERR_STR_SIZE
GCI_MAX_ERR_ARGS = 10
OOP_ILLEGAL = 1

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


class GciLibrary:

    def __init__(self, version='3.4.3', directory=''):
        path = directory + 'libgcits-' + version + '-32.dll'
        self.library = CDLL(path)

        self.gciTsLogin = self.library.GciTsLogin
        self.gciTsLogin.restype = GciSession
        self.gciTsLogin.argtypes = [c_char_p,   # const char *StoneNameNrs
                                    c_char_p,   # const char *HostUserId
                                    c_char_p,   # const char *HostPassword
                                    c_bool,     # BoolType hostPwIsEncrypted
                                    c_char_p,   # const char *GemServiceNrs
                                    c_char_p,   # const char *gemstoneUsername
                                    c_char_p,   # const char *gemstonePassword
                                    c_uint,     # unsigned int loginFlags (per GCI_LOGIN* in gci.ht)
                                    c_int,      # int haltOnErrNum
                                    POINTER(GciErrSType)    # GciErrSType *err
                                    ]

        self.gciTsLogout = self.library.GciTsLogout
        self.gciTsLogout.restype = c_bool
        self.gciTsLogout.argtypes = [GciSession, POINTER(GciErrSType)]

        self.gciTsSessionIsRemote = self.library.GciTsSessionIsRemote
        self.gciTsSessionIsRemote.restype = c_int
        self.gciTsSessionIsRemote.argtypes = [GciSession]

        self.gciTsVersion = self.library.GciTsVersion
        self.gciTsVersion.restype = c_int
        self.gciTsVersion.argtypes = [c_char_p, c_size_t]

        self.gciTsOopToChar = self.library.GciTsOopToChar
        self.gciTsOopToChar.restype = c_int
        self.gciTsOopToChar.argtypes = [OopType]

        self.gciTsCharToOop = self.library.GciTsCharToOop
        self.gciTsCharToOop.restype = OopType
        self.gciTsCharToOop.argtypes = [c_uint]

        self.gciTsDoubleToSmallDouble = self.library.GciTsDoubleToSmallDouble
        self.gciTsDoubleToSmallDouble.restype = OopType
        self.gciTsDoubleToSmallDouble.argtypes = [c_double]

        self.gciI32ToOop = self.library.GciI32ToOop
        self.gciI32ToOop.restype = c_int32
        self.gciI32ToOop.argtypes = [OopType]

        self.gciTsOopIsSpecial = self.library.GciTsOopIsSpecial
        self.gciTsOopIsSpecial.restype = c_bool
        self.gciTsOopIsSpecial.argtypes = [OopType]

        self.gciTsAbort = self.library.GciTsAbort
        self.gciTsAbort.restype = c_bool
        self.gciTsAbort.argtypes = [GciSession, POINTER(GciErrSType)]

    def abort(self, session) -> None:
        error = GciErrSType()
        if not self.gciTsAbort(session, byref(error)):
            raise GciException(error)
        return None

    def oopIsSpecial(self, oop) -> c_bool:
        result = self.gciTsOopIsSpecial(oop)
        return result

    def I32ToOop(self, arg) -> c_int32:
        result = self.gciI32ToOop(arg)
        return result

    def doubleToSmallDouble(self, aFloat) -> c_double:
        result = self.gciTsDoubleToSmallDouble(aFloat)
        if result == OOP_ILLEGAL:
            raise InvalidArgumentError()
        return result

    def charToOop(self, ch) -> OopType:
        result = self.gciTsCharToOop(ch)
        # should check for 1 (OOP_ILLEGAL)
        return result
    
    def oopToChar(self, oop) -> c_int:
        result = self.gciTsOopToChar(oop)
        # should check for -1
        return result
    
    def is_session_valid(self, session) -> bool:
        return self.gciTsSessionIsRemote(session) == 1

    def login(self,
              gem_host='localhost',
              stone='gs64stone',
              gs_user='DataCurator',
              gs_password='swordfish',
              netldi='netldi',
              host_user='',
              host_password='') -> GciSession:
        stone_nrs = '!tcp@localhost#server!' + stone
        gem_nrs = '!tcp@' + gem_host + '#netldi:' + netldi + '#task!gemnetobject'
        if host_user is None:
            host_user = ''
        else:
            host_user = host_user.encode('ascii')
        if host_password is None:
            host_password = ''
        else:
            host_password = host_password.encode('ascii')
        error = GciErrSType()
        session = self.gciTsLogin(
            stone_nrs.encode('ascii'),
            host_user, host_password, False,
            gem_nrs.encode('ascii'),
            gs_user.encode('ascii'), gs_password.encode('ascii'),
            0, 0, byref(error))
        if session is None:
            raise GciException(error)
        return session

    def logout(self, session) -> None:
        error = GciErrSType()
        if not self.gciTsLogout(session, byref(error)):
            raise GciException(error)
        return None

    def version(self) -> str:
        buf = create_string_buffer(256)
        code = self.gciTsVersion(buf, sizeof(buf))
        assert code == 3
        return buf.value.decode('ascii')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
