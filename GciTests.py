"""
>>> # See gcits.hf for details

>>> # obtain an object representing the C library
>>> gci = GciLibrary()
>>> isinstance(gci, GciLibrary)
True

>>> # simplest test to see if we have a GCI library
>>> gci.version()
'3.5.0 build 64bit-46205'

>>> # convert a Smalltalk OOP to an ASCII character
>>> gci.oopToChar(16668)  # $A
65

>>> # this OOP is not a valid character
>>> gci.oopToChar(16667)
-1

>>> gci.oopToChar(24860)  # $a
97

>>> # convert an ASCII code point to a Smalltalk OOP
>>> gci.charToOop(65) # $A
16668

>>> gci.charToOop(97) # $a
24860

>>> # we can convert Unicode as well
>>> gci.charToOop(1114111)
285212444

>>> # this is not a valid character, so get back OOP_INVALID (1)
>>> gci.charToOop(1114112)
1

>>> # convert a double to a Smalltalk OOP
>>> try:
...     gci.doubleToSmallDouble(1.0)
... except InvalidArgumentError:
...     "InvalidArgumentError"
9151314442816847878

>>> # demonstrate that we can properly handle exceptions
>>> try:
...     gci.doubleToSmallDouble(1e40)
... except InvalidArgumentError:
...     "InvalidArgumentError"
'InvalidArgumentError'

>>> gci.I32ToOop(0)
2

>>> gci.I32ToOop(55)
442

>>> # expect an exception for a bad login argument
>>> try:
...     gci.login(gem_host=gem_host, netldi='badldi', stone='badstone')
... except GciException as ex:
...     ex.number()     # invalid NetLDI
4147

>>> try:
...     gci.login(gem_host=gem_host, netldi=netldi, stone='badstone')
... except GciException as ex:
...     ex.number()     # invalid stone
4065

>>> try:
...     gci.login(gem_host=gem_host, netldi=netldi, stone=stone, gs_user='badUser')
... except GciException as ex:
...     ex.number()     # invalid user/password
4051

>>> # using the provided login info we should be successful
>>> session = gci.login(gem_host=gem_host, netldi=netldi, stone=stone, gs_user=gs_user, gs_password=gs_password)
>>> isinstance(session, int)      # successful login
True

>>> gci.is_session_valid(session)
True

>>> # do a name lookup of an object (with a well-known OOP)
>>> symbolName = 'Globals'
>>> try:
...     gci.resolveSymbol(session, symbolName)
... except GciException as ex:
...     ex.number()
207361

>>> object = 7
>>> try:
...     gci.resolveSymbolObj(session, object)
... except GciException as ex:
...     ex.number()
2101

>>> # the following should quietly succeed
>>> try:
...     gci.abort(session)
... except GciException as ex:
...     ex.number()

>>> try:
...     gci.begin(session)
... except GciException as ex:
...     ex.number()

>>> try:
...     gci.commit(session)
... except GciException as ex:
...     ex.number()

>>> # logout should not error
>>> try:
...     gci.logout(session)
... except GciException as ex:
...     ex.number()     # invalid session

>>> # session should no longer be valid
>>> gci.is_session_valid(session)
False

>>> # subsequent logout attempts should fail
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

>>> try:
...     gci.begin(session)
... except GciException as ex:
...     ex.number()
4100

>>> try:
...     gci.commit(session)
... except GciException as ex:
...     ex.number()
4100

"""

if __name__ == '__main__':
    import os
    # Create a local login file that is not under version control
    if (not os.path.isfile('GciLogin.py')):
        import shutil
        shutil.copy2('GciDefault.py', 'GciLogin.py')
    # Import interesting things from GciLibrary
    from GciLibrary import GciLibrary, GciException, InvalidArgumentError
    # Get local login information (not under version control)
    from GciLogin import *
    # Import testing framework
    import doctest
    print('Start tests')
    # Run tests shown in docstring above
    doctest.testmod()
    print('End tests')
