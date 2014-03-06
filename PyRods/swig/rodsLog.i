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

/*****************************************************************************/

%inline %{
PyObject * rodsErrorName(int errorValue) {
    char *mySubName;
    char *myName;
    PyObject *tuple = PyTuple_New(2);
    myName = rodsErrorName(errorValue, &mySubName);
    
    PyTuple_SetItem(tuple, 0, Py_BuildValue("s", myName));
    PyTuple_SetItem(tuple, 1, Py_BuildValue("s", mySubName));
    
    return tuple;
}
%}

/*****************************************************************************/

void rodsLog(int level, char *formatStr, ...);

/*****************************************************************************/

void rodsLogError(int level, int errCode, char *formatStr, ...);

/*****************************************************************************/

void rodsLogLevel(int level);

/*****************************************************************************/
