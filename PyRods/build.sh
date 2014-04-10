#!/bin/sh

# Create irodsswig_wrap.c
swig -python -Iswig irods.i

# apply patch to fix a function
# my swig version always creates the function wrongly
# this happens:
#    lastStatus = _irods.splitPathByKey(srcPath, coll, data, key)
#       TypeError: in method 'splitPathByKey', argument 1 of type 'char *'
patch -R -p0 irods_wrap.c < SWIG_AsCharPtrAndSize_function.patch

# create _irods.so
python setup.py build_ext

