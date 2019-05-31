"""
GciLibrary provides the public API for access to GemStone
"""

import os
import platform
from GciClasses import *

class GciLibrary:

    def __init__(self, version='3.4.3', directory=os.getcwd()):
        self._initLibrary(version, directory)

        self.gciI32ToOop = self.library.GciI32ToOop
        self.gciI32ToOop.restype = c_int32
        self.gciI32ToOop.argtypes = [OopType]

        self.gciTsCharToOop = self.library.GciTsCharToOop
        self.gciTsCharToOop.restype = OopType
        self.gciTsCharToOop.argtypes = [c_uint]

        self.gciTsDoubleToSmallDouble = self.library.GciTsDoubleToSmallDouble
        self.gciTsDoubleToSmallDouble.restype = OopType
        self.gciTsDoubleToSmallDouble.argtypes = [c_double]

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

        self.gciTsOopIsSpecial = self.library.GciTsOopIsSpecial
        self.gciTsOopIsSpecial.restype = c_bool
        self.gciTsOopIsSpecial.argtypes = [OopType]

        self.gciTsOopToChar = self.library.GciTsOopToChar
        self.gciTsOopToChar.restype = c_int
        self.gciTsOopToChar.argtypes = [OopType]

        self.gciTsSessionIsRemote = self.library.GciTsSessionIsRemote
        self.gciTsSessionIsRemote.restype = c_int
        self.gciTsSessionIsRemote.argtypes = [GciSession]

        self.gciTsVersion = self.library.GciTsVersion
        self.gciTsVersion.restype = c_int
        self.gciTsVersion.argtypes = [c_char_p, c_size_t]

    def _initLibrary(self, version, directory):
        system = platform.system()    # 'Darwin', 'Linux', or 'Windows'
        size = sizeof(c_voidp)        # 4 (32-bit) or 8 (64-bit)
        suffixes = {
            4: {
                'Darwin':  '32.dylib',
                'Linux':   '32.so',
                'Windows': '32.dll'
            },
            8: {
                'Darwin':  '64.dylib',
                'Linux':   '64.so',
                'Windows': '64.dll'
            }
        }
        suffix = suffixes.get(size, 'Invalid size').get(system, 'Invalid system')
        path = os.path.join(directory, 'libgcits-' + version + '-' + suffix)
        self.library = CDLL(path)

    def charToOop(self, ch) -> OopType:
        result = self.gciTsCharToOop(ch)
        # should check for 1 (OOP_ILLEGAL)
        return result
    
    def doubleToSmallDouble(self, aFloat) -> c_double:
        result = self.gciTsDoubleToSmallDouble(aFloat)
        # should check for 1 (OOP_ILLEGAL)
        return result

    def I32ToOop(self, arg) -> c_int32:
        result = self.gciI32ToOop(arg)
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
            host_user, 
            host_password, 
            False,
            gem_nrs.encode('ascii'),
            gs_user.encode('ascii'), 
            gs_password.encode('ascii'),
            0, 0, byref(error))
        if session is None:
            raise GciException(error)
        return session

    def logout(self, session) -> None:
        error = GciErrSType()
        if not self.gciTsLogout(session, byref(error)):
            raise GciException(error)
        return None

    def oopIsSpecial(self, oop) -> c_bool:
        result = self.gciTsOopIsSpecial(oop)
        return result

    def oopToChar(self, oop) -> c_int:
        result = self.gciTsOopToChar(oop)
        # should check for -1
        return result
    
    def version(self) -> str:
        buf = create_string_buffer(256)
        code = self.gciTsVersion(buf, sizeof(buf))
        assert code == 3
        return buf.value.decode('ascii')
