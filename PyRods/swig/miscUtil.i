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
#include "miscUtil.h"
%}

typedef struct CollEnt {
    objType_t objType;
    int replNum;
    int replStatus;
    unsigned int dataMode;
    rodsLong_t dataSize;
    char *collName;
    char *dataName;
    char *dataId;
    char *createTime;
    char *modifyTime;
    char *chksum;
    char *resource;
    char *rescGrp;
    char *phyPath;
    char *ownerName;
    specColl_t specColl; 
} collEnt_t;

typedef enum {
    COLL_CLOSED,
    COLL_OPENED,
    COLL_DATA_OBJ_QUERIED,
    COLL_COLL_OBJ_QUERIED
} collState_t;

typedef struct CollHandle {
    collState_t state;
    int inuseFlag;
    int flags;
    int rowInx;
    rodsObjStat_t *rodsObjStat;
    queryHandle_t queryHandle;
    genQueryInp_t genQueryInp;
    dataObjInp_t dataObjInp;
    dataObjSqlResult_t dataObjSqlResult;
    collSqlResult_t collSqlResult;
    char linkedObjPath[MAX_NAME_LEN];
    char prevdataId[NAME_LEN];
} collHandle_t;

typedef struct CollSqlResult {
    int rowCnt;
    int attriCnt;
    int continueInx;
    int totalRowCount;
    sqlResult_t collName; 
    sqlResult_t collType; 
    sqlResult_t collInfo1; 
    sqlResult_t collInfo2;
    sqlResult_t collOwner;
    sqlResult_t collCreateTime;
    sqlResult_t collModifyTime;
} collSqlResult_t;

typedef struct DataObjSqlResult {
    int rowCnt;
    int attriCnt;
    int continueInx;
    int totalRowCount;
    sqlResult_t collName;
    sqlResult_t dataName;
    sqlResult_t dataMode;
    sqlResult_t dataSize;
    sqlResult_t createTime;
    sqlResult_t modifyTime;
    sqlResult_t chksum;
    sqlResult_t replStatus;
    sqlResult_t dataId;
    sqlResult_t resource;
    sqlResult_t phyPath;
    sqlResult_t ownerName;
    sqlResult_t replNum;
    sqlResult_t rescGrp;
    sqlResult_t dataType;
} dataObjSqlResult_t;

typedef struct QueryHandle {
    void *conn;
    connType_t connType;
    funcPtr querySpecColl;
    funcPtr genQuery;
} queryHandle_t;

/*****************************************************************************/

int getRodsObjType (rcComm_t *conn, rodsPath_t *rodsPath);

/*****************************************************************************/

int mkColl (rcComm_t *conn, char *collection);

/*****************************************************************************/

int mkCollR (rcComm_t *conn, char *startColl, char *destColl);

/*****************************************************************************/

int mkdirR (char *startDir, char *destDir, int mode);

/*****************************************************************************/

int myChmod (char *inPath, uint dataMode);

/*****************************************************************************/

%inline %{
PyObject * queryCollAcl(rcComm_t *conn, char *collName, char *zoneHint) {
    genQueryOut_t *genQueryOut = NULL;
    int status = queryCollAcl(conn, collName, zoneHint, &genQueryOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(genQueryOut), 
                                            SWIGTYPE_p_GenQueryOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * queryCollAclSpecific(rcComm_t *conn, char *collName, 
                                char *zoneHint) {
    genQueryOut_t *genQueryOut = NULL;
    int status = queryCollAclSpecific (conn, collName, zoneHint, &genQueryOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(genQueryOut), 
                                            SWIGTYPE_p_GenQueryOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * queryCollInColl(queryHandle_t *queryHandle, char *collection,
                           int flags, genQueryInp_t *genQueryInp) {
    genQueryOut_t *genQueryOut = NULL;
    int status = queryCollInColl(queryHandle, collection, flags, genQueryInp, &genQueryOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(genQueryOut), 
                                            SWIGTYPE_p_GenQueryOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * queryCollInheritance(rcComm_t *conn, char *collName) {
    genQueryOut_t *genQueryOut = NULL;
    int status = queryCollInheritance(conn, collName, &genQueryOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(genQueryOut), 
                                            SWIGTYPE_p_GenQueryOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * queryDataObjInColl(queryHandle_t *queryHandle, char *collection,
                                   int flags, genQueryInp_t *genQueryInp, 
                                   keyValPair_t *condInput) {
    genQueryOut_t *genQueryOut = NULL;
    int status = queryDataObjInColl(queryHandle, collection, flags, genQueryInp, 
                       &genQueryOut, condInput);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(genQueryOut), 
                                            SWIGTYPE_p_GenQueryOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * queryDataObjAcl(rcComm_t *conn, char *dataId, char *zoneHint) {
    genQueryOut_t *genQueryOut = NULL;
    int status = queryDataObjAcl(conn, dataId, zoneHint, &genQueryOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(genQueryOut), 
                                            SWIGTYPE_p_GenQueryOut, 0 |  0 ));
}
%}

/*****************************************************************************/

int rclCloseCollection(collHandle_t *collHandle);

/*****************************************************************************/

int rclInitQueryHandle(queryHandle_t *queryHandle, rcComm_t *conn);

/*****************************************************************************/

int rclOpenCollection (rcComm_t *conn, char *collection, 
int flag, collHandle_t *collHandle);

%pythoncode %{
def rclOpenCollection(conn, collection, flag):
    collHandle = collHandle_t()
    status = _irods.rclOpenCollection(conn, collection, flag, collHandle)
    return (status, collHandle)
%}

/*****************************************************************************/

%inline %{
PyObject * rclReadCollection(rcComm_t *conn, collHandle_t *collHandle) {
    collEnt_t * collEnt = (collEnt_t*) malloc(sizeof(collEnt_t));
    memset(collEnt, 0, sizeof(collEnt_t));
    int status = rclReadCollection(conn, collHandle, collEnt);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(collEnt), 
                                            SWIGTYPE_p_CollEnt, 0 |  0 ));
}
%}

/*****************************************************************************/

int setQueryFlag(rodsArguments_t *rodsArgs);

/*****************************************************************************/

int setQueryInpForData(int flags, genQueryInp_t *genQueryInp);

/*****************************************************************************/
