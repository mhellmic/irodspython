irodspython
===========

This is a fork of https://code.google.com/p/irodspython/, the SWIG python bindings for iRODS with additional patches.
The patches are listed below.

### patches

* add cleanup functions for the genQueryOut_t struct to reduce memory leaks
* save the status of sendApiRequest in the connection object to make it accessible from python

