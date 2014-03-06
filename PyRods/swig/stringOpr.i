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

%{
#include "stringOpr.h"
%}


/*****************************************************************************/

%cstring_mutable(char **dir);
%cstring_mutable(char **file);
int
splitPathByKey (char *srcPath, char *dir, char *file, char key);

%pythoncode %{
def splitPathByKey(srcPath, key):
    """splitPathByKey - 
  Input -
    str srcPath -
    char key -
  OutPut - (str, str, int)
    str coll - directory
    str data - file
    int status - status of the operation."""
    global lastStatus
    # TO IMPROVE: irods doesn't manage this out string well
    coll = "_" * MAX_NAME_LEN
    data = "_" * MAX_NAME_LEN
    lastStatus = _irods.splitPathByKey(srcPath, coll, data, key)
    coll = coll[:coll.find('\0')]
    data = data[:data.find('\0')]
    return (lastStatus, coll, data)
%}

/*****************************************************************************/