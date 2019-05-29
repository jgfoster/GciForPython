# Python FFI for GemStone

[GemStone](https://gemtalksystems.com/products/gs64/) is an object database and application runtime environment. You interact with the database through a dynamically linked C library available for Linux, macOS, and Windows. To use a C library from Python we use [ctypes](https://docs.python.org/3/library/ctypes.html), a foreign function library wrapper that allows us to define C types, structures, and function entry points, then load and call a C library.

GemBuilder for C documentation ([HTML](https://downloads.gemtalksystems.com/docs/GemStone64/3.4.x/GS64-GemBuilderC-3.4/GS64-GemBuilderC-3.4.htm) or [PDF](https://downloads.gemtalksystems.com/docs/GemStone64/3.4.x/GS64-GemBuilderforC-3.4.pdf)) describes the API for the *single-threaded* GCI library. We are using a new *thread-safe* library that has fewer functions (but more features). It is not separately documented, but has a header file, `gcits.hf`, that is the definitive specification (a recent copy is included with this checkout).

The needed C libraries are not included as part of this checkout since there is a different set of libraries for each platform (Linux, macOS, and Windows), and for each GemStone version. You should download a recent version and the appropriate [product](https://gemtalksystems.com/products/gs64/) for your platform. The move the appropriate files into this directory.

* Linux: libfloss-3.4.x-64.so and libgcits-3.4.x-64.so
* macOS: libfloss-3.4.x-64.dynlib and libgcits-3.4.x-64.dynlib
* Windows: libgcits-3.4.x-32.dll and libssl-3.4.x-32.dll