"""
>>> # See gcits.hf for details

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

>>> gci.doubleToSmallDouble(1.0)
9151314442816847878

>>> gci.doubleToSmallDouble(1e40)
1

>>> gci.I32ToOop(0)
2

>>> gci.I32ToOop(55)
442

>>> try:
...     gci.login(netldi='badldi', stone='badstone')
... except GciException as ex:
...     ex.number()     # invalid NetLDI
4147

>>> try:
...     gci.login(netldi=netldi, stone='badstone')
... except GciException as ex:
...     ex.number()     # invalid stone
4065

>>> try:
...     gci.login(netldi=netldi, stone=stone, gs_user='badUser')
... except GciException as ex:
...     ex.number()     # invalid user/password
4051

>>> session = gci.login(netldi=netldi, stone=stone, gs_user=gs_user, gs_password=gs_password)
>>> isinstance(session, int)      # successful login
True

>>> gci.is_session_valid(session)
True

>>> gci.logout(session)

>>> gci.is_session_valid(session)
False

>>> try:
...     gci.logout(session)
... except GciException as ex:
...     ex.number()     # invalid session
4100

"""

if __name__ == '__main__':
    import os
    if (not os.path.isfile('GciLogin.py')):
        import shutil
        shutil.copy2('GciDefault.py', 'GciLogin.py')
    from GciLibrary import GciLibrary, GciException
    from GciLogin import *
    import doctest
    print('Start tests')
    doctest.testmod()
    print('End tests')
