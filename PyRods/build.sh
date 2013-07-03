#!/bin/sh

# Create irodsswig_wrap.c
swig -python -Iswig irods.i

# create _irods.so
python setup.py build_ext

