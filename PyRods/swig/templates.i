/* Copyright (c) 2013, University of Liverpool
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *
 * Author       : Jerome Fuselier
 */

%typemap(in, numinputs=0, noblock=1) size_t *len  {
  size_t templen;
  $1 = &templen;
}

/*****************************************************************************/

%typemap(in) int * {
  if (!PySequence_Check($input)) {
    PyErr_SetString(PyExc_ValueError,"Expected a sequence");
    return NULL;
  }
  size_t len = PyList_Size($input);
  size_t i = 0;
  $1 = (int *) malloc((len+1)*sizeof(int));
  for (i = 0; i < len; i++) {
    PyObject *o = PySequence_GetItem($input,i);
    if (PyNumber_Check(o)) {
      $1[i] = (int) PyInt_AsLong(o);
    } else {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be integers");      
      free($1);
      return NULL;
    }
  }
  $1[i] = 0;
}

%typemap(freearg) int * {
   if ($1) free($1);
}

%typemap(out) int * {
  unsigned int i;
  $result = PyList_New(templen);
  for (i = 0; i < templen; i++) {
    PyObject *o = PyInt_FromLong($1[i]);
    PyList_SetItem($result,i,o);
  }
}

/*****************************************************************************/

%typemap(in) char ** {
    /* Check if is a list */
    if (PyList_Check($input)) {
        size_t size = PyList_Size($input);
        size_t i = 0;
        $1 = (char **) malloc((size+1)*sizeof(char *));
        for (i = 0; i < size; i++) {
            PyObject *o = PyList_GetItem($input,i);
            if (PyString_Check(o) || PyUnicode_Check(o))
                $1[i] = PyString_AsString(PyList_GetItem($input,i));
            else {
                PyErr_SetString(PyExc_TypeError,"list must contain strings");
                free($1);
                return NULL;
            }
        }
        $1[size] = 0;
    } else {
        PyErr_SetString(PyExc_TypeError,"not a list");
        return NULL;
    }
}

%typemap(freearg) char ** {
	free((char *)$1);
}

%typemap(out) char ** {
  unsigned int i;
  $result = PyList_New(templen);
  for (i = 0; i < templen; i++) {
    PyObject *o = PyString_FromString($1[i]);
    PyList_SetItem($result,i,o);
  }
}
