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
#include "rodsPath.h"
%}

/*****************************************************************************/

typedef struct RodsPath {
    objType_t objType;
    objStat_t objState;
    rodsLong_t size;
    unsigned int objMode;
    char inPath[MAX_NAME_LEN];
    char outPath[MAX_NAME_LEN];
    char dataId[NAME_LEN];
    char chksum[NAME_LEN];
    rodsObjStat_t *rodsObjStat;
} rodsPath_t;

typedef struct RodsPathInp {
    int numSrc;
    rodsPath_t *srcPath;
    rodsPath_t *destPath;
    rodsPath_t *targPath;
    int resolved;
} rodsPathInp_t;

%extend rodsPathInp_t {
    rodsPath_t * getSrcPath(int n) {
        if ( (n >= 0) && (n < $self->numSrc) )
            return &$self->srcPath[n];
        else
            return NULL;
    }
    
    rodsPath_t * getDestPath(int n) {
        if ( (n >= 0) && (n < $self->numSrc) )
            return &$self->destPath[n];
        else
            return NULL;
    }
    
    rodsPath_t * getTargPath(int n) {
        if ( (n >= 0) && (n < $self->numSrc) )
            return &$self->targPath[n];
        else
            return NULL;
    }
}


/*****************************************************************************/

int addSrcInPath (rodsPathInp_t *rodsPathInp, char *inPath);

/*****************************************************************************/

%cstring_mutable(char **lastElement);
int
getLastPathElement (char *inPath, char *lastElement);


%pythoncode %{
def getLastPathElement(inPath):
    """getLastPathElement - 
  Input -
    str inPath -
  OutPut - (str, int)
    str lastElement
    int status - status of the operation."""
    global lastStatus
    # TO IMPROVE: irods doesn't manage this out string well
    lastElement = "_" * MAX_NAME_LEN
    lastStatus = _irods.getLastPathElement(inPath, lastElement)
    lastElement = lastElement[:lastElement.find('\0')]
    return (lastStatus, lastElement)
%}

/*****************************************************************************/

int parseCmdLinePath(int argc, char **argv, int optInd, rodsEnv *myRodsEnv,
int srcFileType, int destFileType, int flag, rodsPathInp_t *rodsPathInp);

/*****************************************************************************/

int parseRodsPath(rodsPath_t *rodsPath, rodsEnv *myRodsEnv);

/*****************************************************************************/

int parseRodsPathStr(char *inPath, rodsEnv *myRodsEnv, char *outPath);

/*****************************************************************************/

int resolveRodsTarget(rcComm_t *conn, rodsEnv *myRodsEnv,
rodsPathInp_t *rodsPathInp, int oprType);

/*****************************************************************************/