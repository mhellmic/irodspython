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
#include "dataCopy.h"
#include "dataGet.h"
#include "dataPut.h"
#include "dataObjChksum.h"
#include "dataObjClose.h"
#include "dataObjCreate.h"
#include "dataObjCreateAndStat.h"
#include "dataObjGet.h"
#include "dataObjInpOut.h"
#include "dataObjLock.h"
#include "dataObjLseek.h"
#include "dataObjOpen.h"
#include "dataObjOpenAndStat.h"
#include "dataObjPhymv.h"
#include "dataObjPut.h"
#include "dataObjRead.h"
#include "dataObjRename.h"
#include "dataObjRepl.h"
#include "dataObjRsync.h"
#include "dataObjTrim.h"
#include "dataObjTruncate.h"
#include "dataObjUnlink.h"
#include "dataObjWrite.h"
%}

/* definition for oprType in dataObjInp_t, portalOpr_t and l1desc_t */

#define DONE_OPR            9999
#define PUT_OPR             1
#define GET_OPR             2
#define SAME_HOST_COPY_OPR      3
#define COPY_TO_LOCAL_OPR   4
#define COPY_TO_REM_OPR     5
#define REPLICATE_OPR       6
#define REPLICATE_DEST          7
#define REPLICATE_SRC           8
#define COPY_DEST               9
#define COPY_SRC                10
#define RENAME_DATA_OBJ         11
#define RENAME_COLL             12
#define MOVE_OPR                13
#define RSYNC_OPR               14
#define PHYMV_OPR               15
#define PHYMV_SRC               16
#define PHYMV_DEST              17
#define QUERY_DATA_OBJ          18
#define QUERY_DATA_OBJ_RECUR    19
#define QUERY_COLL_OBJ          20
#define QUERY_COLL_OBJ_RECUR    21
#define RENAME_UNKNOWN_TYPE     22
#define REMOTE_ZONE_OPR         24
#define UNREG_OPR           26

/* NETCDF type operation */
#define NC_OPR          1000    /* netcdf operation */
#define NC_OPEN_FOR_WRITE   1000    /* open/create NETCDF for write */
#define NC_OPEN_FOR_READ    1001    /* open NETCDF for read */
#define NC_CREATE       1002    /* create NETCDF */
#define NC_OPEN_GROUP       1003    /* create NETCDF */

/* definition for openType in l1desc_t */
#define CREATE_TYPE             1
#define OPEN_FOR_READ_TYPE      2
#define OPEN_FOR_WRITE_TYPE     3

/* definition for flags */
#define STREAMING_FLAG      0x1
#define NO_CHK_COPY_LEN_FLAG    0x2

/* lock type definition */
#define READ_LOCK_TYPE  "readLockType"
#define WRITE_LOCK_TYPE "writeLockType"
#define UNLOCK_TYPE "unlockType"

/* lock command definition */
#define SET_LOCK_CMD    "setLockCmd"
#define SET_LOCK_WAIT_CMD "setLockWaitCmd"
#define GET_LOCK_CMD    "getLockCmd"

/*****************************************************************************/

typedef struct CollInp {
    char collName[MAX_NAME_LEN];
    int flags;
    int oprType;
    keyValPair_t condInput;
} collInp_t;

typedef struct DataCopyInp {
    dataOprInp_t dataOprInp;
    portalOprOut_t portalOprOut;
} dataCopyInp_t;

typedef struct DataObjCopyInp {
    dataObjInp_t srcDataObjInp;
    dataObjInp_t destDataObjInp;
} dataObjCopyInp_t;

typedef struct DataObjInp {
    char objPath[MAX_NAME_LEN];
    int createMode;
    int openFlags;
    rodsLong_t offset;
    rodsLong_t dataSize;
    int numThreads;
    int oprType;
    specColl_t *specColl;
    keyValPair_t condInput;
} dataObjInp_t;

typedef struct DataOprInp {
    int oprType;
    int numThreads;
    int srcL3descInx;
    int destL3descInx;
    int srcRescTypeInx;
    int destRescTypeInx;
    rodsLong_t offset;
    rodsLong_t dataSize;
    keyValPair_t condInput;
} dataOprInp_t;

typedef struct OpenedDataObjInp {
    int l1descInx;
    int len;
    int whence;
    int oprType;
    rodsLong_t offset;
    rodsLong_t bytesWritten;
    keyValPair_t condInput;
} openedDataObjInp_t;

typedef struct OpenStat {
    rodsLong_t dataSize;
    char dataType[NAME_LEN];
    char dataMode[SHORT_STR_LEN];
    int l3descInx;
    int replStatus;
    int rescTypeInx;
    int replNum;
} openStat_t;

typedef struct portalOprOut {
    int status;
    int l1descInx;
    int numThreads;
    char chksum[NAME_LEN];
    portList_t portList;
} portalOprOut_t;

typedef struct {
    int portNum;
    int cookie;
    int windowSize;
    char hostAddr[LONG_NAME_LEN];
} portList_t;


/*****************************************************************************/

int clearDataObjCopyInp (dataObjCopyInp_t *dataObjCopyInp);

/*****************************************************************************/

int rcDataCopy (rcComm_t *conn, dataCopyInp_t *dataCopyInp);

/*****************************************************************************/

//int
//rcDataGet (rcComm_t *conn, dataOprInp_t *dataGetInp,
//portalOprOut_t **portalOprOut);

%inline %{
PyObject * rcDataGet(rcComm_t *conn, dataOprInp_t *dataGetInp) {
    portalOprOut_t *portalOprOut = NULL;
    int status = rcDataGet(conn, dataGetInp, &portalOprOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(portalOprOut), 
                                            SWIGTYPE_p_portalOprOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * rcDataPut(rcComm_t *conn, dataOprInp_t *dataPutInp) {
    portalOprOut_t *portalOprOut = NULL;
    int status = rcDataPut(conn, dataPutInp, &portalOprOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(portalOprOut), 
                                            SWIGTYPE_p_portalOprOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * rcDataObjChksum(rcComm_t *conn, dataObjInp_t *dataObjChksumInp) {
    char *outChksum = NULL;
    int status = rcDataObjChksum(conn, dataObjChksumInp, &outChksum);
    return Py_BuildValue("(is)", 
                         status, 
                         outChksum);
}
%}

/*****************************************************************************/

int rcDataObjClose (rcComm_t *conn, openedDataObjInp_t *dataObjCloseInp);

/*****************************************************************************/

int rcDataObjCopy (rcComm_t *conn, dataObjCopyInp_t *dataObjCopyInp);

/*****************************************************************************/

int rcDataObjCreate (rcComm_t *conn, dataObjInp_t *dataObjInp);

/*****************************************************************************/

%inline %{
PyObject * rcDataObjCreateAndStat(rcComm_t *conn, dataObjInp_t *dataObjInp) {
    openStat_t *openStat = NULL;
    int status = rcDataObjCreateAndStat(conn, dataObjInp, &openStat);
    return Py_BuildValue("(is)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(openStat), 
                                            SWIGTYPE_p_OpenStat, 0 |  0 ));
}
%}

/*****************************************************************************/

int rcDataObjGet (rcComm_t *conn, dataObjInp_t *dataObjInp, char *locFilePath);

/*****************************************************************************/

int rcDataObjLock (rcComm_t *conn, dataObjInp_t *dataObjInp);

/*****************************************************************************/

%inline %{
PyObject * rcDataObjLseek(rcComm_t *conn, openedDataObjInp_t *dataObjLseekInp) {
    fileLseekOut_t *dataObjLseekOut = NULL;
    int status = rcDataObjLseek(conn, dataObjLseekInp, &dataObjLseekOut);
    return Py_BuildValue("(is)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(dataObjLseekOut), 
                                            SWIGTYPE_p_FileLseekOut, 0 |  0 ));
}
%}

/*****************************************************************************/

int rcDataObjOpen (rcComm_t *conn, dataObjInp_t *dataObjInp);

/*****************************************************************************/

%inline %{
PyObject * rcDataObjOpenAndStat(rcComm_t *conn, dataObjInp_t *dataObjInp) {
    openStat_t *openStat = NULL;
    int status = rcDataObjOpenAndStat(conn, dataObjInp, &openStat);
    return Py_BuildValue("(is)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(openStat), 
                                            SWIGTYPE_p_OpenStat, 0 |  0 ));
}
%}

/*****************************************************************************/

int rcDataObjPhymv (rcComm_t *conn, dataObjInp_t *dataObjInp);

/*****************************************************************************/

int rcDataObjPut (rcComm_t *conn, dataObjInp_t *dataObjInp,
char *locFilePath);

/*****************************************************************************/

int rcDataObjRead (rcComm_t *conn, openedDataObjInp_t *dataObjReadInp,
bytesBuf_t *dataObjReadOutBBuf);

%pythoncode %{
def rcDataObjRead(conn, fileReadInp):
    dataObjReadOutBBuf = bytesBuf_t()
    dataObjReadOutBBuf.malloc(fileReadInp.len)
    readSize = _irods.rcDataObjRead(conn, fileReadInp, dataObjReadOutBBuf)
    outString = dataObjReadOutBBuf.getBuf()
    return (readSize, outString)
%}

/*****************************************************************************/

int rcDataObjRename (rcComm_t *conn, dataObjCopyInp_t *dataObjRenameInp);

/*****************************************************************************/

int rcDataObjRepl (rcComm_t *conn, dataObjInp_t *dataObjInp);

/*****************************************************************************/

int rcDataObjRsync (rcComm_t *conn, dataObjInp_t *dataObjInp); 

/*****************************************************************************/

int rcDataObjTrim (rcComm_t *conn, dataObjInp_t *dataObjInp);

/*****************************************************************************/

int rcDataObjTruncate (rcComm_t *conn, dataObjInp_t *dataObjInp);

/*****************************************************************************/

int rcDataObjUnlink (rcComm_t *conn, dataObjInp_t *dataObjUnlinkInp);

/*****************************************************************************/

int rcDataObjWrite (rcComm_t *conn, openedDataObjInp_t *dataObjWriteInp,
bytesBuf_t *dataObjWriteInpBBuf);

/*****************************************************************************/
