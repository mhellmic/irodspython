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
#include "closeCollection.h"
#include "collCreate.h"
#include "collRepl.h"
#include "modColl.h"
#include "openCollection.h"
#include "phyPathReg.h"
#include "readCollection.h"
#include "regDataObj.h"
#include "regColl.h"
#include "regReplica.h"
#include "syncMountedColl.h"
#include "unregDataObj.h"
%}

/*****************************************************************************/


%pythoncode %{


class irodsCollection:

    def __init__(self, conn, collName=None):
        status, myEnv = getRodsEnv()
        self._conn = conn
        
        if collName:
            # Remove the last '/', if len = 1 the user wants the root colection
            if len(collName) > 1 and collName[-1] == '/':
                collName = collName[:-1]
                
            if collName.startswith('/'):
                # If the path starts with '/' we assume a global path
                self.collName = collName
            else:
                # else we assume that it is local to the current working dir
                self.collName = myEnv.rodsCwd + '/' + collName
            
        else:
             ## If no collName, we use the current working directory
            self.collName = myEnv.rodsCwd

    def addUserMetadata(self, name, value, units=""):
        return addUserMetadata(self._conn, "-c", self.collName,
                               name, value, units)

    def create(self, dataName, resc_name=""):
        if not resc_name:
            status, myEnv = getRodsEnv()
            resc_name = myEnv.rodsDefResource
            
        return _irodsOpen(self._conn, self.collName, dataName, "w", resc_name)

    def createCollection(self, child_collName):
        global lastStatus
        collCreateInp = collInp_t()
        collCreateInp.collName = "%s/%s" % (self.collName, child_collName)
        lastStatus = rcCollCreate(self._conn, collCreateInp)
        return lastStatus

    def delete(self, dataName, resc_name=""):
        global lastStatus
        dataObjInp = dataObjInp_t()
        if resc_name:
            replNum = getDataObjReplicaNumber(self._conn, self.collName,
                                              dataName, resc_name);
        else:
            replNum = "0"
        if replNum:
            addKeyVal(dataObjInp.condInput, REPL_NUM_KW, replNum)
        dataObjInp.openFlags = O_RDONLY
        dataObjInp.objPath = "%s/%s" % (self.collName, dataName)
        lastStatus = rcDataObjUnlink(self._conn, dataObjInp)
        return lastStatus

    def deleteCollection(self, child_collName):
        global lastStatus
        collInp = collInp_t()
        collInp.collName = "%s/%s" % (self.collName, child_collName)
        addKeyVal(collInp.condInput, FORCE_FLAG_KW, "")
        addKeyVal(collInp.condInput, RECURSIVE_OPR__KW, "")
        lastStatus = rcRmColl(self._conn, collInp, 0)
        return lastStatus

    def getCollName(self):
        return self.collName

    def getId(self):
        return getCollId(self._conn, self.getCollName())

    def getLenObjects(self):
        queryFlags = DATA_QUERY_FIRST_FG | LONG_METADATA_FG | NO_TRIM_REPL_FG
        nb_el = 0
        
        status, collHandle = rclOpenCollection(self._conn, self.collName, queryFlags)
        status, collEnt = rclReadCollection(self._conn, collHandle)
        while status >= 0:
            if collEnt.objType == DATA_OBJ_T:
                nb_el += 1
            status, collEnt = rclReadCollection(self._conn, collHandle)
        rclCloseCollection(collHandle)
        return nb_el

    def getLenSubCollections(self):
        queryFlags = DATA_QUERY_FIRST_FG
        nb_el = 0
        
        status, collHandle = rclOpenCollection(self._conn, self.collName, queryFlags)
        status, collEnt = rclReadCollection(self._conn, collHandle)
        while status >= 0:
            if collEnt.objType == COLL_OBJ_T:
                nb_el += 1 
            status, collEnt = rclReadCollection(self._conn, collHandle)
        rclCloseCollection(collHandle)
        return nb_el

    def getObjects(self):
        queryFlags = DATA_QUERY_FIRST_FG | LONG_METADATA_FG | NO_TRIM_REPL_FG
        l = []
        
        status, collHandle = rclOpenCollection(self._conn, self.collName, queryFlags)
        status, collEnt = rclReadCollection(self._conn, collHandle)
        while status >= 0:
            if collEnt.objType == DATA_OBJ_T:
                status, srcElement = getLastPathElement(collEnt.dataName)
                if srcElement:
                    l.append((srcElement, collEnt.resource))
            status, collEnt = rclReadCollection(self._conn, collHandle)
        rclCloseCollection(collHandle)
        return l

    def getSubCollections(self):
        queryFlags = DATA_QUERY_FIRST_FG
        l = []
        
        status, collHandle = rclOpenCollection(self._conn, self.collName, queryFlags)
        status, collEnt = rclReadCollection(self._conn, collHandle)
        while status >= 0:
            if collEnt.objType == COLL_OBJ_T:
                status, myColl, myData = splitPathByKey(collEnt.collName, '/')
                if myData:
                    l.append(myData)
            status, collEnt = rclReadCollection(self._conn, collHandle)
        rclCloseCollection(collHandle)
        return l

    def getUserMetadata(self):
        sqlCondInp = inxValPair_t()
        selectInp = inxIvalPair_t()
        selectInp.init([COL_META_COLL_ATTR_NAME, COL_META_COLL_ATTR_VALUE,
                        COL_META_COLL_ATTR_UNITS],
                       [0, 0, 0], 3)
        sqlCondInp.init([COL_COLL_NAME], ["='%s'" % self.collName], 1)
        return queryToTupleList(self._conn, selectInp, sqlCondInp)

    def open(self, dataName, mode="r", resc_name=""):
        if not resc_name:
            status, myEnv = getRodsEnv()
            resc_name = myEnv.rodsDefResource
        return _irodsOpen(self._conn, self.collName, dataName, mode, resc_name)

    def openCollection(self, collName):
        global lastStatus
        lastStatus = CAT_UNKNOWN_COLLECTION
        if collName != '/':   
            collName = collName.rstrip('/')
        # If the path starts with '/' we assume a global path
        if (collName.startswith('/')):
           self.collName = collName
           lastStatus = 0
        else:
            ls_child = self.getSubCollections()
            if collName in ls_child:
                # Special case for the root dir
                if self.collName == '/':
                    fullName = '/' + collName
                else:
                    fullName = "%s/%s" % (self.collName, collName)
                self.collName = fullName
                lastStatus = 0
        return lastStatus

    def rmUserMetadata(self, name, value, units=""):
        return rmUserMetadata(self._conn, "-c", self.collName,
                               name, value, units) 

    def upCollection(self):
        status, myDir, myFile = splitPathByKey(self.collName, "/")
        self.collName = myDir

class irodsFile:

    def __init__(self, conn):
        self._conn = conn
        self.descInx = 0
        self.position = 0
        self.openFlag = O_RDONLY
        self.collName = ""
        self.dataName = ""
        self.resourceName = ""
        self.size = 0

    def __iter__(self):
        return self

    def addUserMetadata(self, name, value, units=""):
        fullName = self.fullPath()
        return addUserMetadata(self._conn, "-d", fullName, name, value, units)

    def copy(self, new_path, force=False, resc=None):
        return irodsCopy(self._conn, self.fullPath(), new_path, force, resc)

    def close(self):
        global lastStatus
        dataObjCloseInp = openedDataObjInp_t()
        dataObjCloseInp.l1descInx = self.descInx
        lastStatus = rcDataObjClose(self._conn, dataObjCloseInp)
        return lastStatus

    def delete(self, force=False):
        global lastStatus
        dataObjInp = dataObjInp_t()
        replNum = getDataObjReplicaNumber(self._conn,
                                          self.collName,
                                          self.dataName,
                                          self.resourceName)
        if replNum:
            addKeyVal(dataObjInp.condInput, REPL_NUM_KW, replNum)
            
        if force:
            addKeyVal(dataObjInp.condInput, FORCE_FLAG_KW, "")
        dataObjInp.openFlags = O_RDONLY
        dataObjInp.objPath = self.fullPath()
        lastStatus = rcDataObjUnlink(self._conn, dataObjInp)
        return lastStatus

    def fileno(self):
        return self.descInx

    def flush(self):
        pass

    def fullPath(self):
        return "%s/%s" % (self.collName, self.dataName)

    def getChecksum(self):
        d = self.getInfos();
        return d.get("data_checksum", "")

    def getCollId(self):
        d = self.getInfos();
        return d.get("coll_id", "")

    def getCollName(self):
        return self.collName

    def getComment(self):
        d = self.getInfos();
        return d.get("r_comment", "")

    def getCreateTs(self):
        d = self.getInfos();
        return d.get("create_ts", "")

    def getDescInx(self):
        return self.descInx

    def getExpiryTs(self):
        d = self.getInfos();
        return d.get("data_expiry_ts", "")

    def getId(self):
        d = self.getInfos();
        return d.get("data_id", "")

    def getInfos(self):
        return getFileInfo(self._conn, self.collName,
                           self.dataName, self.resourceName)

    def getMapId(self):
        d = self.getInfos();
        return d.get("data_map_id", "")

    def getMode(self):
        d = self.getInfos();
        return d.get("data_mode", "")

    def getModifyTs(self):
        d = self.getInfos();
        return d.get("modify_ts", "")

    def getName(self):
        return self.dataName

    def getOwnerName(self):
        d = self.getInfos();
        return d.get("data_owner_name", "")

    def getOwnerZone(self):
        d = self.getInfos();
        return d.get("data_owner_zone", "")

    def getPath(self):
        d = self.getInfos();
        return d.get("data_path", "")

    def getPosition(self):
        return self.position

    def getReplications(self):
        res_list = getDataObjRescNames(self._conn, self.collName,
                                       self.dataName)
        res = []
        for resc_name in res_list:
            if resc_name == self.resourceName:
                res.append(self)
            else:
                f = _irodsOpen(self._conn, self.collName, self.dataName, 
                               "r+", resc_name)
        return res

    def getReplNumber(self):
        d = self.getInfos();
        return d.get("data_repl_num", "")

    def getReplStatus(self):
        d = self.getInfos();
        return d.get("data_is_dirty", "")

    def getResourceGroupName(self):
        d = self.getInfos();
        return d.get("resc_group_name", "")

    def getResourceName(self):
        return self.resourceName

    def getTypeName(self):
        d = self.getInfos();
        return d.get("data_type_name", "")

    def getSize(self):
        d = self.getInfos();
        return int(d.get("data_size", "0"))

    def getStatus(self):
        d = self.getInfos();
        return d.get("data_status", "")

    def getUserMetadata(self):
        sqlCondInp = inxValPair_t()
        selectInp = inxIvalPair_t()
        selectInp.init([COL_META_DATA_ATTR_NAME, COL_META_DATA_ATTR_VALUE,
                        COL_META_DATA_ATTR_UNITS],
                       [0, 0, 0], 3)
        sqlCondInp.init([COL_COLL_NAME, COL_DATA_NAME], 
                        ["='%s'" % self.collName,
                         "='%s'" % self.dataName], 2)
        return queryToTupleList(self._conn, selectInp, sqlCondInp)

    def getVersion(self):
        d = self.getInfos();
        return d.get("data_version", "")

    def isatty(self):
        return false

    def move(self, new_path):
        global lastStatus
        dataObjRenameInp = dataObjCopyInp_t()
        dataObjRenameInp.srcDataObjInp.oprType = RENAME_DATA_OBJ
        dataObjRenameInp.srcDataObjInp.objPath = self.fullPath()
        dataObjRenameInp.destDataObjInp.oprType = RENAME_DATA_OBJ
        dataObjRenameInp.destDataObjInp.objPath = new_path
        lastStatus = rcDataObjRename(self._conn, dataObjRenameInp)
        return lastStatus

    def next(self):
        if self.position >= self.size:
            raise StopIteration
        return self.readline()

    # Optional parameter : number of bytes to read. if not present reads
    # TRANS_BUF_SZ bytes. If the size is greater it has to be refined...
    def read(self, buffSize=TRANS_BUF_SZ):
        if self.openFlag & O_WRONLY != 0:
            return ""
        else:
            dataObjReadInp = openedDataObjInp_t()
            dataObjLseekInp = openedDataObjInp_t()
            dataObjReadInp.len = buffSize
            dataObjReadInp.l1descInx = self.descInx
                
            ## If there are replication, there could be several position for the
            ## same file (due to the fact that irods consider that replications
            ## are the same files), so we ensure before reading that the position
            ## of the cursor for reading match the one we have for the replicate
            ## not 100% sure of that however
            
            dataObjLseekInp.l1descInx = self.descInx
            dataObjLseekInp.offset = self.position
            dataObjLseekInp.whence = SEEK_SET
            
            status, dataObjLseekOut = rcDataObjLseek(self._conn, dataObjLseekInp)
            readSize, outString = rcDataObjRead(self._conn, dataObjReadInp)
            
            self.position += readSize
            return outString

    def readline(self, size=None):
        res = ""
        end = False
        
        c = self.read(1)
        readsize = 1
        end = c == ''
    
        while not end:
            res += c
            c = self.read(1)
            readsize += 1
            if not c or c in ['\r', '\n']:
                res += c
                end = True
            if size:
                if readsize >= size:
                    res += c
                    end = True
    
        return res

    def replicate(self, rescName):
        global lastStatus
        dataObjInp = dataObjInp_t()
        dataObjInp.objPath = self.fullPath()
        addKeyVal(dataObjInp.condInput, RESC_NAME_KW, self.resourceName)
        replNum = getDataObjReplicaNumber(self._conn, self.collName,
                                          self.dataName, self.resourceName)
        if replNum:
            addKeyVal(dataObjInp.condInput, REPL_NUM_KW, replNum)
        addKeyVal(dataObjInp.condInput, DEST_RESC_NAME_KW, rescName)
        lastStatus = rcDataObjRepl(self._conn, dataObjInp)
        return lastStatus

    def rmUserMetadata(self, name, value, units=""):
        fullName = self.fullPath()
        return rmUserMetadata(self._conn, "-d", fullName, name, value, units)

    def seek(self, offset, whence=SEEK_SET):
        global lastStatus
        dataObjLseekInp = openedDataObjInp_t()
        dataObjLseekOut = fileLseekOut_t()
        dataObjLseekInp.l1descInx = self.descInx
        dataObjLseekInp.offset = offset
        dataObjLseekInp.whence = whence
        lastStatus, dataObjLseekOut = rcDataObjLseek(self._conn, dataObjLseekInp)
        if (whence == SEEK_SET):
            self.position = offset
        elif (whence == SEEK_CUR):
            self.position += offset
        elif (whence == SEEK_END):
            self.position = getDataObjSize(self._conn, self.collName, 
                                           self.dataName, self.resourceName) + offset
        return dataObjLseekOut

    def set_size(self):
        self.size = getDataObjSize(self._conn, self.collName, 
                                   self.dataName, self.resourceName)

    def tell(self):
        return self.getPosition()

    def update(self):
        global lastStatus
        dataObjInp = dataObjInp_t()
        dataObjInp.objPath = self.fullPath()
        addKeyVal(dataObjInp.condInput, UPDATE_REPL_KW, "")
        lastStatus = rcDataObjRepl(self._conn, dataObjInp)
        return lastStatus
    
    def write(self, inpBuff):
        global lastStatus
        if self.openFlag == O_RDONLY:
            # If the file is only open for reading and we try to write in it,
            # the call to rcDataObjRead will fail.
            return 0
        else:
            inpLen = len(inpBuff)
            dataObjWriteInpBBuf = bytesBuf_t()
            fileWriteInp = openedDataObjInp_t()
            fileWriteInp.l1descInx = self.descInx
            fileWriteInp.len = inpLen
            dataObjWriteInpBBuf.setBuf(inpBuff, inpLen)
            lastStatus = rcDataObjWrite(self._conn, fileWriteInp, dataObjWriteInpBBuf)
            if lastStatus > 0:
                self.position += lastStatus
                self.size += lastStatus
            return lastStatus

%}



/*****************************************************************************/

typedef struct {
    dataObjInfo_t *srcDataObjInfo;
    dataObjInfo_t *destDataObjInfo;
    keyValPair_t condInput;
} regReplica_t;

typedef struct {
    dataObjInfo_t *dataObjInfo;
    keyValPair_t *condInput;
} unregDataObj_t;

/*****************************************************************************/

int clearRegReplicaInp (regReplica_t *regReplicaInp);

/*****************************************************************************/

int clearUnregDataObj (unregDataObj_t *unregDataObjInp);

/*****************************************************************************/

int rcCloseCollection (rcComm_t *conn, int handleInxInp);

/*****************************************************************************/

int rcCollCreate (rcComm_t *conn, collInp_t *collCreateInp);

/*****************************************************************************/

int rcCollRepl (rcComm_t *conn, collInp_t *collReplInp, int vFlag);

/*****************************************************************************/

int rcModColl (rcComm_t *conn, collInp_t *modCollInp);

/*****************************************************************************/

int rcOpenCollection (rcComm_t *conn, collInp_t *openCollInp);

/*****************************************************************************/

int rcOprComplete (rcComm_t *conn, int retval);

/*****************************************************************************/

int rcPhyPathReg (rcComm_t *conn, dataObjInp_t *phyPathRegInp);

/*****************************************************************************/

int rcReadCollection (rcComm_t *conn, int handleInxInp, collEnt_t **collEnt);

/*****************************************************************************/

int rcRegColl (rcComm_t *conn, collInp_t *regCollInp);

/*****************************************************************************/

%inline %{
dataObjInfo_t * rcRegDataObj(rcComm_t *conn, dataObjInfo_t *dataObjInfo) {
    dataObjInfo_t * outDataObjInfo = NULL;
    rcRegDataObj(conn, dataObjInfo, &outDataObjInfo);
    return outDataObjInfo;
}
%}

/*****************************************************************************/

int rcSyncMountedColl (rcComm_t *conn, dataObjInp_t *syncMountedCollInp);

/*****************************************************************************/

int rcRegReplica (rcComm_t *conn, regReplica_t *regReplicaInp);

/*****************************************************************************/

int rcUnregDataObj (rcComm_t *conn, unregDataObj_t *unregDataObjInp);

/*****************************************************************************/
