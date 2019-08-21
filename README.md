# Python FFI for GemStone

[GemStone](https://gemtalksystems.com/products/gs64/) is an object database and application runtime environment. You interact with the database through a dynamically linked C library available for Linux, macOS, and Windows. To use a C library from Python we use [ctypes](https://docs.python.org/3/library/ctypes.html), a foreign function library wrapper that allows us to define C types, structures, and function entry points, then load and call a C library.

GemBuilder for C documentation ([HTML](https://downloads.gemtalksystems.com/docs/GemStone64/3.4.x/GS64-GemBuilderC-3.4/GS64-GemBuilderC-3.4.htm) or [PDF](https://downloads.gemtalksystems.com/docs/GemStone64/3.4.x/GS64-GemBuilderforC-3.4.pdf)) describes the API for the *single-threaded* GCI library. We are using a new *thread-safe* library that has fewer functions (but more features). It is not separately documented, but has a header file, `gcits.hf`, that is the definitive specification (a recent copy is included with this checkout).

The needed C libraries are not included as part of this checkout since there is a different set of libraries for each platform (Linux, macOS, and Windows), and for each GemStone version. You should download a recent version and the appropriate [product](https://gemtalksystems.com/products/gs64/) for your platform. Then move the appropriate files into the `./lib/` directory (below this README.md file).

* Linux:
  * libfloss-3.4.x-64.so and libgcits-3.4.x-64.so
  * libgcits-3.5.x-64.so, libkrb5-3.5.x-64.so and libssl-3.5.0-64.so 
* macOS:
  * libfloss-3.4.x-64.dylib and libgcits-3.4.x-64.dylib
  * libgcits-3.5.x-64.dylib, libkrb5-3.5.x-64.dylib, and libssl-3.5.0-64.dylib
* Windows:
  * libgcits-3.4.x-32.dll and libssl-3.4.x-32.dll
  * libgcits-3.5.x-32.dll and libssl-3.5.x-32.dll

## Files

In addition to this README.md and the C header file (used for reference only) the checkout provides four files:

* **GciLibrary.py**: This is the primary API and the only one that client code should import directly.
* **GciClasses.py**: This file defines some basic constants, types, and classes that are used by the library. It is used internally and should not be referenced by client code.
* **GciDefault.py**: This file is a template for you to customize as GciLogin.py, which is used by GciTests.py. It is only needed if you run tests.
* **GCITests.py**: This file demonstrates use of the library and tests each of the methods using [doctest](https://docs.python.org/3/library/doctest.html).

## Contributing Code

To add new function wrappers follow these steps:

* Identify a new function from `gcits.hf` (pick from the list below);
* Add it to `__init__` with the appropriate name, arguments, and return type;
* Add a wrapper function to GciLibrary to provide a Python-like API; 
* Add a test to show that it works; and, finally,
* Submit a pull request!

# Function List

The following provides a list of all the functions defined in `gcits.hf` grouped to roughly parallel the tables in the GemBuilder for C manual. Checked items have been completed. Numbered items are suggested next tasks (with priority).

### Table 7.1 Functions for Controlling Sessions and Transactions
```
✓	BoolType   GciTsAbort(GciSession sess, GciErrSType *err);
1	BoolType   GciTsBegin(GciSession sess, GciErrSType *err);
1	BoolType   GciTsCommit(GciSession sess, GciErrSType *err);
	char*      GciTsEncrypt(const char* password, char *outBuf, size_t outBuffSize);
✓	int        GciTsSessionIsRemote(GciSession sess);
✓	GciSession GciTsLogin(
	BoolType   GciTsForkLogin(
✓	BoolType   GciTsLogout(GciSession sess, GciErrSType *err);
```

### Table 7.2 Functions for Handling Errors and Interrupts and for Debugging
```
1	BoolType   GciTsBreak(GciSession sess, BoolType hard, GciErrSType *err);
1	int        GciTsCallInProgress(GciSession sess, GciErrSType *err);
	BoolType   GciTsClearStack(GciSession sess, OopType gsProcess, GciErrSType *err);
	OopType    GciTsContinueWith(GciSession sess,
	BoolType   GciTsForkContinueWith(GciSession sess,
	int        GciTsGemTrace(GciSession sess, int enable, GciErrSType *err);
```

### Table 7.3 Functions for Managing Object Bitmaps
```
	BoolType   GciTsReleaseObjs(GciSession sess, OopType *buf, int count, GciErrSType *err);
	BoolType   GciTsReleaseAllObjs(GciSession sess, GciErrSType *err);
	BoolType   GciTsSaveObjs(GciSession sess, OopType *buf, int count, GciErrSType *err);
```

### Table 7.4 Functions for Compiling and Executing Smalltalk Code in the Database
```
	OopType    GciTsCompileMethod(GciSession sess,
	BoolType   GciTsProtectMethods(GciSession sess, BoolType mode, GciErrSType *err);
	BoolType   GciTsClassRemoveAllMethods(GciSession sess, 
3	OopType    GciTsExecute(GciSession sess,
	BoolType   GciTsForkExecute(GciSession sess,
	OopType    GciTsExecute_(GciSession sess,
3	ssize_t    GciTsExecuteFetchBytes(GciSession sess,
3	OopType    GciTsPerform(GciSession sess,
	BoolType   GciTsForkPerform(GciSession sess,
3	ssize_t    GciTsPerformFetchBytes(GciSession sess,
```

### Table 7.5 Functions for Accessing Symbol Dictionaries
```
2	OopType    GciTsResolveSymbol(GciSession sess, 
	OopType    GciTsResolveSymbolObj(GciSession sess, 
```

### Table 7.6 Functions for creating and Initializing Objects
```
	int        GciTsGetFreeOops(GciSession sess, OopType *buf, int numOopsRequested, GciErrSType *err);
	OopType    GciTsNewObj(GciSession sess, OopType aClass, GciErrSType *err);
	OopType    GciTsNewByteArray(GciSession sess, 
	OopType    GciTsNewString_(GciSession sess, 
	OopType    GciTsNewString(GciSession sess, 
	OopType    GciTsNewSymbol(GciSession sess, 
	OopType    GciTsNewUnicodeString_(GciSession s,
	OopType    GciTsNewUnicodeString(GciSession sess, 
	OopType    GciTsNewUtf8String(GciSession sess, 
	OopType    GciTsNewUtf8String_(GciSession sess, 
	int64      GciTsFetchUnicode(GciSession sess,
	int64      GciTsFetchUtf8(GciSession sess,
```

### Table 7.7 Functions for Converting Objects and Values
```
✓	BoolType   GciTsOopIsSpecial(OopType oop);
2	OopType    GciTsFetchSpecialClass(OopType oop);
✓	int        GciTsOopToChar(OopType oop);
✓	OopType    GciTsCharToOop(uint ch);
✓	OopType    GciTsDoubleToSmallDouble(double aFloat);
	BoolType   GciUtf8To8bit(const char* src, char *dest, ssize_t destSize);
	ssize_t    GciNextUtf8Character(const char* src, size_t len, uint *chOut);
✓	OopType    GciI32ToOop(int arg);
	OopType    GciTsDoubleToOop(GciSession sess, double aDouble, GciErrSType *err);
	BoolType   GciTsOopToDouble(GciSession sess, OopType oop,
	OopType    GciTsI64ToOop(GciSession sess, int64 arg, GciErrSType *err);
	BoolType   GciTsOopToI64(GciSession sess, OopType oop, int64 *result, GciErrSType *err);
```

### Table 7.8 Object Traversal and Path Functions
```
	int        GciTsStoreTravDoTravRefs(GciSession sess,
	BoolType   GciTsForkStoreTravDoTravRefs(GciSession sess,
	int        GciTsFetchTraversal(GciSession sess, 
	BoolType   GciTsStoreTrav(GciSession sess, 
	int        GciTsMoreTraversal(GciSession sess,
```

### Table 7.9 Structural Access Functions
```
	int64      GciTsFetchBytes(GciSession sess,
	int64      GciTsFetchChars(GciSession sess,
	int64      GciTsFetchUtf8Bytes(GciSession sess,
	BoolType   GciTsStoreBytes(GciSession sess,
	int        GciTsFetchOops(GciSession sess,
	BoolType   GciTsStoreOops(GciSession sess,
	int        GciTsRemoveOopsFromNsc(GciSession sess, 
	int64      GciTsFetchObjInfo(GciSession sess, OopType objId, 
2	int64      GciTsFetchSize(GciSession sess, OopType obj, GciErrSType *err);
2	int64      GciTsFetchVaryingSize(GciSession sess, OopType obj, GciErrSType *err);
2	OopType    GciTsFetchClass(GciSession sess, OopType obj, GciErrSType *err);
2	int        GciTsIsKindOf(GciSession sess, 
2	int        GciTsIsSubclassOf(GciSession sess, 
2	int        GciTsIsKindOfClass(GciSession sess, 
	int        GciTsIsSubclassOfClass(GciSession sess, 
2	BoolType   GciTsObjExists(GciSession sess, OopType obj);
```

### Table 7.10 Utility Functions
```
✓	uint       GciTsVersion(char *buf, size_t bufSize);
	int        GciTsWaitForEvent(GciSession sess, int latencyMs,
	BoolType   GciTsCancelWaitForEvent(GciSession sess, GciErrSType *err);
```