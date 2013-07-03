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

#define PURGE_STRUCT_FILE_CACHE 0x1 
#define DELETE_STRUCT_FILE  0x2 
#define NO_REG_COLL_INFO    0x4 
#define LOGICAL_BUNDLE      0x8
#define CREATE_TAR_OPR      0x0
#define ADD_TO_TAR_OPR          0x10
#define PRESERVE_COLL_PATH      0x20
#define PRESERVE_DIR_CONT   0x40

// We can also use the os module in Python
#define O_RDONLY 0
#define O_WRONLY 1
#define O_RDWR 2
#define O_CREAT 64
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

/*****************************************************************************/


%pythoncode %{
def _irodsOpen(conn, collName, dataName, mode, resc_name):
    ir_file = irodsFile(conn)
    dataObjInp = dataObjInp_t()
    
    ir_file.dataName = dataName
    ir_file.collName = collName
    ir_file.openFlag = O_RDONLY
    
    dataObjInp.objPath = ir_file.fullPath()
    
    # Set the resource
    if resc_name:
        ir_file.resourceName = resc_name
        addKeyVal(dataObjInp.condInput, DEST_RESC_NAME_KW, resc_name)
        
        # Set the replica number (get the info from the icat)
        # returns null if the file does not exist
        replNum = getDataObjReplicaNumber(conn, collName, dataName, resc_name)
    
        if replNum:
            addKeyVal(dataObjInp.condInput, REPL_NUM_KW, replNum)
    
    if mode == "w":
        dataObjInp.openFlags = O_WRONLY | O_CREAT
        ir_file.openFlag = O_WRONLY | O_CREAT
        addKeyVal(dataObjInp.condInput, FORCE_FLAG_KW, "")
        l1descInx = rcDataObjCreate(conn, dataObjInp)
        
    elif mode == "r":
        dataObjInp.openFlags = O_RDONLY
        ir_file.openFlag = O_RDONLY
        l1descInx = rcDataObjOpen(conn, dataObjInp) 
        
    elif mode == "a":  
        dataObjInp.openFlags = O_WRONLY
        ir_file.openFlag = O_WRONLY
        l1descInx = rcDataObjOpen(conn, dataObjInp)
        
        if l1descInx != CAT_NO_ROWS_FOUND: # the file exists => seek to the end
            dataObjLseekInp = openedDataObjInp_t()
            dataObjLseekInp.l1descInx = l1descInx
            dataObjLseekInp.offset = 0
            dataObjLseekInp.whence = SEEK_END

            dataObjLseekOut = rcDataObjLseek(conn, dataObjLseekInp)
            ir_file.position = getDataObjSize(conn, collName, dataName, resc_name)
        else:
            l1descInx = rcDataObjCreate(conn, dataObjInp)
            
    elif mode == "w+":
        dataObjInp.openFlags = O_RDWR
        ir_file.openFlag = O_RDWR
        addKeyVal(dataObjInp.condInput, FORCE_FLAG_KW, "")
        l1descInx = rcDataObjCreate(conn, dataObjInp)
        
    elif mode == "r+":
        dataObjInp.openFlags = O_RDWR
        ir_file.openFlag = O_RDWR
        l1descInx = rcDataObjOpen(conn, dataObjInp) 
        
    elif mode == "a+":
        dataObjInp.openFlags = O_RDWR
        ir_file.openFlag = O_RDWR
        l1descInx = rcDataObjOpen(conn, dataObjInp)
        
        if l1descInx != CAT_NO_ROWS_FOUND: # the file exists => seek to the end
            dataObjLseekInp = openedDataObjInp_t()
            dataObjLseekInp.l1descInx = l1descInx
            dataObjLseekInp.offset = 0
            dataObjLseekInp.whence = SEEK_END

            dataObjLseekOut = rcDataObjLseek(conn, dataObjLseekInp)
            ir_file.position = getDataObjSize(conn, collName, dataName, resc_name)
        else:
            l1descInx = rcDataObjCreate(conn, dataObjInp)
    
    if not resc_name: # If the resc parameter was NULL then we need to find the
                      # resource iRODS used and set the ir_file variable
        ir_resc_name = getDataObjRescNames(conn, collName, dataName)
        ir_file.resourceName = ir_resc_name

    if l1descInx > 0:
        ir_file.descInx = l1descInx
        return ir_file
    else:
        return None
        
def addCollUserMetadata(conn, path, name, value, units=""):
    return addUserMetadata(conn, "-c", path, name, value, units)
    
def addFileUserMetadata(conn, path, name, value, units=""):
    return addUserMetadata(conn, "-d", path, name, value, units)
    
def getCollUserMetadata(conn, path):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
            
    selectInp.init([COL_META_COLL_ATTR_NAME, COL_META_COLL_ATTR_VALUE,
                    COL_META_COLL_ATTR_UNITS],
                   [0, 0, 0], 3)
    
    sqlCondInp.init([COL_COLL_NAME], ["='%s'" % path], 1)
    
    return queryToTupleList(conn, selectInp, sqlCondInp)

def getFileUserMetadata(conn, path):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
    
    status, collName, dataName = splitPathByKey(path, "/")
    
    selectInp.init([COL_META_DATA_ATTR_NAME, COL_META_DATA_ATTR_VALUE,
                    COL_META_DATA_ATTR_UNITS],
                   [0, 0, 0], 3)
    
    sqlCondInp.init([COL_COLL_NAME, COL_DATA_NAME], 
                    ["='%s'" % collName,
                     "='%s'" % dataName], 2)
    
    return queryToTupleList(conn, selectInp, sqlCondInp)

def rmCollUserMetadata(conn, path, name, value, units=""):
    return rmUserMetadata(conn, "-c", path, name, value, units)
    
def rmFileUserMetadata(conn, path, name, value, units=""):
    return rmUserMetadata(conn, "-d", path, name, value, units)

def irodsOpen(conn, path, mode="r", resc_name=""):
    if not resc_name:
        status, myEnv = getRodsEnv()
        resc_name = myEnv.rodsDefResource
    status, collName, dataName = splitPathByKey(path, "/")
    return  _irodsOpen(conn, collName, dataName, mode, resc_name) 
    
    
class irodsFile:
    
    def __init__(self, conn):
        self._conn = conn
        self.descInx = 0
        self.position = 0
        self.openFlag = O_RDONLY
        self.collName = ""
        self.dataName = ""
        self.resourceName = ""
        
    def fullPath(self):
        return "%s/%s" % (self.collName, self.dataName)
        
    def close(self):
        dataObjCloseInp = openedDataObjInp_t()
        dataObjCloseInp.l1descInx = self.descInx
        return rcDataObjClose(self._conn, dataObjCloseInp)
        
    def delete(self, force=False):
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
        return rcDataObjUnlink(self._conn, dataObjInp)
    
    def getCollName(self):
        return self.collName
    
    def getName(self):
        return self.dataName
    
    def getInfos(self):
        return getFileInfoToDict(self._conn, self.collName,
                                 self.dataName, self.resourceName)
        
    def getDescInx(self):
        return self.descInx
    
    def getPosition(self):
        return self.position
    
    def getResourceName(self):
        return self.resourceName
    
    def getResourceGroupName(self):
        d = self.getInfos();
        return d.get("resc_group_name", "")
    
    def getId(self):
        d = self.getInfos();
        return d.get("data_id", "")
    
    def getMapId(self):
        d = self.getInfos();
        return d.get("data_map_id", "")
    
    def getPath(self):
        d = self.getInfos();
        return d.get("data_path", "")
    
    def getTypeName(self):
        d = self.getInfos();
        return d.get("data_type_name", "")
    
    def getComment(self):
        d = self.getInfos();
        return d.get("r_comment", "")
    
    def getMode(self):
        d = self.getInfos();
        return d.get("data_mode", "")
    
    def getOwnerName(self):
        d = self.getInfos();
        return d.get("data_owner_name", "")
    
    def getOwnerZone(self):
        d = self.getInfos();
        return d.get("data_owner_zone", "")
    
    def getChecksum(self):
        d = self.getInfos();
        return d.get("data_checksum", "")
    
    def getVersion(self):
        d = self.getInfos();
        return d.get("data_version", "")
    
    def getExpiryTs(self):
        d = self.getInfos();
        return d.get("data_expiry_ts", "")
    
    def getModifyTs(self):
        d = self.getInfos();
        return d.get("modify_ts", "")
    
    def getCreateTs(self):
        d = self.getInfos();
        return d.get("create_ts", "")
    
    def getStatus(self):
        d = self.getInfos();
        return d.get("data_status", "")
    
    def getCollId(self):
        d = self.getInfos();
        return d.get("coll_id", "")
    
    def getReplStatus(self):
        d = self.getInfos();
        return d.get("data_is_dirty", "")
    
    def getSize(self):
        d = self.getInfos();
        return int(d.get("data_size", "0"))
    
    def getReplNumber(self):
        d = self.getInfos();
        return d.get("data_repl_num", "")
    
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
            
            dataObjLseekOut = rcDataObjLseek(self._conn, dataObjLseekInp)
            readSize, outString = rcDataObjRead(self._conn, dataObjReadInp)
            
            self.position += readSize
            
            return outString
          
    def seek(self, offset, whence=SEEK_SET):
        dataObjLseekInp = openedDataObjInp_t()
        dataObjLseekOut = fileLseekOut_t()
        
        dataObjLseekInp.l1descInx = self.descInx
        dataObjLseekInp.offset = offset
        dataObjLseekInp.whence = whence
        
        dataObjLseekOut = rcDataObjLseek(self._conn, dataObjLseekInp)
        
        if (whence == SEEK_SET):
            self.position = offset
        elif (whence == SEEK_CUR):
            self.position += offset
        elif (whence == SEEK_END):
            self.position = getDataObjSize(self._conn, self.collName, 
                                           self.dataName, self.resourceName) - offset
                                           
        return dataObjLseekOut
    
    def write(self, inpBuff):
        if self.openFlag == O_RDONLY:
            # If the file is only open for reading and we try to write in it,
            # the call to rcDataObjRead will fail.
            return 0
        else:
            inpLen = len(inpBuff)
            dataObjWriteInpBBuf = bytesBuf_t();
            
            fileWriteInp = openedDataObjInp_t()
            fileWriteInp.l1descInx = self.descInx
            fileWriteInp.len = inpLen
            
            dataObjWriteInpBBuf.setBuf(inpBuff, inpLen)
            
            status = rcDataObjWrite(self._conn, fileWriteInp, dataObjWriteInpBBuf)
            
            if status > 0:
                self.position += status
            
            return status
        
    def update(self):
        dataObjInp = dataObjInp_t()
        
        dataObjInp.objPath = self.fullPath()
        addKeyVal(dataObjInp.condInput, UPDATE_REPL_KW, "")
        status = rcDataObjRepl(self._conn, dataObjInp)
        return status
    
    def replicate(self, rescName):
        dataObjInp = dataObjInp_t()
        
        dataObjInp.objPath = self.fullPath()
        addKeyVal(dataObjInp.condInput, RESC_NAME_KW, self.resourceName)
        
        replNum = getDataObjReplicaNumber(self._conn, self.collName,
                                          self.dataName, self.resourceName);
                                          
        if replNum:
            addKeyVal(dataObjInp.condInput, REPL_NUM_KW, replNum)

        addKeyVal(dataObjInp.condInput, DEST_RESC_NAME_KW, rescName)
        return rcDataObjRepl(self._conn, dataObjInp)
        
    def addUserMetadata(self, name, value, units=""):
        fullName = self.fullPath()
        return addUserMetadata(self._conn, "-d", fullName, name, value, units)
        
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
        
    def rmUserMetadata(self, name, value, units=""):
        fullName = self.fullPath()
        return rmUserMetadata(self._conn, "-d", fullName, name, value, units)



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
        collCreateInp = collInp_t()
        collCreateInp.collName = "%s/%s" % (self.collName, child_collName)
        status = rcCollCreate(self._conn, collCreateInp)
        return status
    
    def delete(self, dataName, resc_name=""):
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
        
        status = rcDataObjUnlink(self._conn, dataObjInp)
        return status
    
    def deleteCollection(self, child_collName):
        collInp = collInp_t()
        collInp.collName = "%s/%s" % (self.collName, child_collName)
        addKeyVal(collInp.condInput, FORCE_FLAG_KW, "")
        addKeyVal(collInp.condInput, RECURSIVE_OPR__KW, "")
        status = rcRmColl(self._conn, collInp, 0)
        return status

    def getCollName(self):
        return self.collName
    
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
        status = CAT_UNKNOWN_COLLECTION
        if collName != '/':   
            collName = collName.rstrip('/')
        # If the path starts with '/' we assume a global path
        if (collName.startswith('/')):
           self.collName = collName
           status = 0
        else:
            ls_child = self.getSubCollections()
            if collName in ls_child:
                # Special case for the root dir
                if self.collName == '/':
                    fullName = '/' + collName
                else:
                    fullName = "%s/%s" % (self.collName, collName)
                self.collName = fullName
                status = 0
        return status
        
    def rmUserMetadata(self, name, value, units=""):
        return rmUserMetadata(self._conn, "-c", self.collName,
                               name, value, units) 
        
    def upCollection(self):
        status, myDir, myFile = splitPathByKey(self.collName, "/")
        self.collName = myDir
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
