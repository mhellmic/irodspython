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

%pythoncode %{

def addObject(conn, objType, objName, arg3, arg4, arg5, arg6):
    generalAdminInp = generalAdminInp_t ()

    generalAdminInp.arg0 = "add"
    generalAdminInp.arg1 = objType
    generalAdminInp.arg2 = objName
    generalAdminInp.arg3 = arg3
    generalAdminInp.arg4 = arg4
    generalAdminInp.arg5 = arg5
    generalAdminInp.arg6 = arg6
    generalAdminInp.arg7 = ""
    generalAdminInp.arg8 = ""
    generalAdminInp.arg9 = ""

    return rcGeneralAdmin(conn, generalAdminInp)

# Parse a genQueryOut result parameter which comes from a genQuery call.
# Add the output to the python list passed in parameter. Each row becomes an
# element of the list and each element is a dictionary created with the keys
# passed in parameter. The order should be compliant with the order in genQueryInp
# if len(formatStr) < len(genQueryOut->sqlResult[a].attriInx) => segfault, that's
# why this function is not accessible from anywhere else
def addResultToFormatDictList(genQueryOut, formatStr, l):
    if not genQueryOut:
        return 0
    
    for r in xrange(genQueryOut.rowCnt):
        t = genQueryOut.getSqlResultIdx(r)
        d = {}
        
        for idx in xrange(len(formatStr)):
            name = formatStr[idx]
            tResult = t[idx]
            if name.endswith("_ts"):    # Pretty print of time values
                localTime = getLocalTimeFromRodsTime(tResult)
                d[name] = localTime
            else:
                d[name] = tResult
        l.append(d)
    
    return 0
    
##
## Parse a genQueryOut result parameter which comes from a genQuery call.
## Add the output to the python list passed in parameter. Each row becomes an
## element of the list and each element is a tuple created by selected attributes
## in the genQueryInp parameter.
## If attriCnt = 1 we do not create a list of tuple of str but a list of str
def addResultToTupleList(genQueryOut, l):
    if not genQueryOut:
        return 0
    
    for r in xrange(genQueryOut.rowCnt):
        l.append(genQueryOut.getSqlResultIdx(r))
    
    return 0
    
def addUserMetadata(conn, obj_type, name, attName, attValue, attUnits):
    return procUserMetadata(conn, "add", obj_type, name, attName, attValue, 
                            attUnits)

## Returns the number of a replica for a specific file when you only know the
## resource name. This is used by REPL_NUM_KW when you want to open a file for
## instance
def getDataObjReplicaNumber(conn, coll_name, data_name, resc_name):
    genQueryInp = genQueryInp_t()
    
    addInxVal(genQueryInp.sqlCondInp, COL_COLL_NAME, "='%s'" % coll_name)
    addInxVal(genQueryInp.sqlCondInp, COL_DATA_NAME, "='%s'" % data_name)
    addInxVal(genQueryInp.sqlCondInp, COL_D_RESC_NAME, "='%s'" % resc_name)
    addInxIval(genQueryInp.selectInp, COL_DATA_REPL_NUM, 1)
    genQueryInp.maxRows = MAX_SQL_ROWS
    
    genQueryOut = rcGenQuery(conn, genQueryInp)
    rescNum = getSqlResultByInx(genQueryOut, COL_DATA_REPL_NUM)
    
    if genQueryOut and genQueryOut.rowCnt >= 0:
        # Should only have one row as output
        rescNum = getSqlResultByInx(genQueryOut, COL_DATA_REPL_NUM)
        res = rescNum.value[0]
    else:
        return ""
    
    return res

# Returns a PyList of the resource names of an irods data object given its
# collection and its name. The order is given by resource ids.
# It will fail if there are more than MAX_SQL_ROWS as I did not loop if
# continueInx > 0 after genQuery call
def getDataObjRescNames(conn, coll_name, data_name):
    genQueryInp = genQueryInp_t()
    
    addInxVal(genQueryInp.sqlCondInp, COL_COLL_NAME, "='%s'" % coll_name)
    addInxVal(genQueryInp.sqlCondInp, COL_DATA_NAME, "='%s'" % data_name)
    addInxIval(genQueryInp.selectInp, COL_D_RESC_NAME, 1)
    addInxIval(genQueryInp.selectInp, COL_R_RESC_ID, ORDER_BY)
    genQueryInp.maxRows = MAX_SQL_ROWS
    
    genQueryOut = rcGenQuery(conn, genQueryInp)
    rescNum = getSqlResultByInx(genQueryOut, COL_DATA_REPL_NUM)
    
    res = []
    if genQueryOut and genQueryOut.rowCnt >= 0:
        for i in xrange(genQueryOut.rowCnt):
            res.append(genQueryOut.getSqlResultByInxIdx(COL_D_RESC_NAME, i))
    else:
        return ""
    
    return res

# Returns the size of a data object
def getDataObjSize(conn, coll_name, data_name, resc_name):
    genQueryInp = genQueryInp_t()
    
    addInxVal(genQueryInp.sqlCondInp, COL_COLL_NAME, "='%s'" % coll_name)
    addInxVal(genQueryInp.sqlCondInp, COL_DATA_NAME, "='%s'" % data_name)  
    addInxVal(genQueryInp.sqlCondInp, COL_D_RESC_NAME, "='%s'" % resc_name)
    addInxIval(genQueryInp.selectInp, COL_DATA_SIZE, 1)
    genQueryInp.maxRows = MAX_SQL_ROWS
    
    genQueryOut = rcGenQuery(conn, genQueryInp)
    if genQueryOut and genQueryOut.rowCnt >= 0:
        sizeNum = getSqlResultByInx(genQueryOut, COL_DATA_SIZE)
        return int(sizeNum.value)
    else:
        return 0

# Get the file Info with the name and resource, query the ICAT database and
# create a dictionary with the returned information. Need the connection to
# iRODS
def getFileInfo(conn, coll_name, data_name, resc_name):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
    
    selectInp.init([COL_D_DATA_ID, COL_D_COLL_ID, COL_DATA_NAME, 
                    COL_DATA_REPL_NUM, COL_DATA_VERSION, COL_DATA_TYPE_NAME, 
                    COL_DATA_SIZE, COL_D_RESC_GROUP_NAME, COL_D_RESC_NAME, 
                    COL_D_DATA_PATH, COL_D_OWNER_NAME, COL_D_OWNER_ZONE, 
                    COL_D_REPL_STATUS, COL_D_DATA_STATUS, COL_D_DATA_CHECKSUM, 
                    COL_D_EXPIRY, COL_D_MAP_ID, COL_D_COMMENTS, 
                    COL_D_CREATE_TIME, COL_D_MODIFY_TIME, COL_DATA_MODE],
                   [0, 0, 0, 0, 0, 
                    0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 
                    0, 0, 0, 0, 0,
                    0], 
                   21)
    
    sqlCondInp.init([COL_DATA_NAME, COL_COLL_NAME, COL_D_RESC_NAME], 
                    ["='%s'" % data_name,
                     "='%s'" % coll_name,
                     "='%s'" % resc_name], 
                    3)
    
    columnNames = ["data_id", "coll_id", "data_name", "data_repl_num",
                   "data_version", "data_type_name", "data_size",
                   "resc_group_name", "resc_name", "data_path",
                   "data_owner_name", "data_owner_zone", "data_is_dirty",
                   "data_status", "data_checksum", "data_expiry_ts",
                   "data_map_id", "r_comment", "create_ts", "modify_ts",
                   "data_mode"]
    
    l =  queryToFormatDictList(conn, selectInp, sqlCondInp, columnNames);
    
    if len(l) > 0:
        return l[0]
    else:
        return {columnNames[0] : "mountP",          # "data_id"
                columnNames[1] : "",                # "coll_id"
                columnNames[2] : data_name,         # "data_name"
                columnNames[3] : "1",               # "data_repl_num"
                columnNames[4] : "",                # "data_version"
                columnNames[5] :  "mountP",         # "data_type_name"
                columnNames[6] : "       ",         # "data_size"
                columnNames[7] : "",                # "resc_group_name"
                columnNames[8] : resc_name,         # "resc_name"
                columnNames[9] : coll_name,         # "data_path"
                columnNames[10] : "        ",       # "data_owner_name"
                columnNames[11] : "            ",   # "data_owner_zone"
                columnNames[12] : "",               # "data_is_dirty" 
                columnNames[13] : "",               # "data_status"
                columnNames[14] : "",               # "data_checksum"
                columnNames[15] : "              ", # "data_expiry_ts"
                columnNames[16] : "",               # "data_map_id"
                columnNames[17] : "",               # "r_comment"
                columnNames[18] : "              ", # "create_ts"
                columnNames[19] : "              ", # "modify_ts"
                columnNames[20] : ""}               # "data_mode"

# Get a python list of names of members of a group 
def getGroupMembers(conn, group_name):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
                
    selectInp.init([COL_USER_NAME, COL_USER_ZONE,],
                   [0, 0], 
                   2)
    sqlCondInp.init([COL_USER_GROUP_NAME], 
                    ["='%s'" % group_name], 
                    1)
    
    return queryToTupleList(conn, selectInp, sqlCondInp)

def getRescInfoToDict(conn, resc_name):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
                
    selectInp.init([COL_R_RESC_ID, COL_R_RESC_NAME, COL_R_ZONE_NAME, 
                    COL_R_TYPE_NAME, COL_R_CLASS_NAME, COL_R_LOC, 
                    COL_R_VAULT_PATH, COL_R_FREE_SPACE, COL_R_FREE_SPACE_TIME, 
                    COL_R_RESC_INFO, COL_R_RESC_COMMENT, COL_R_CREATE_TIME, 
                    COL_R_MODIFY_TIME],
                   [0, 0, 0, 0, 0, 
                    0, 0, 0, 0, 0,
                    0, 0, 0], 
                   13)
    
    sqlCondInp.init([COL_R_RESC_NAME], 
                    ["='%s'" % resc_name], 
                    1)
    
    columnNames = ["resc_id", "resc_name", "zone_name", "resc_type_name",
                   "resc_class_name", "resc_net", "resc_def_path",
                   "free_space", "free_space_ts", "resc_info",
                   "r_comment", "create_ts", "modify_ts"]

    l =  queryToFormatDictList(conn, selectInp, sqlCondInp, columnNames);
    
    if len(l) > 0:
        return l[0]
    else:
        return {}

def getResources(conn):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
    
    selectInp.init([COL_R_RESC_NAME], [0], 1)
    sqlCondInp.init([], [], 0)
    
    return [ irodsResource(conn, name) for name in queryToTupleList(conn, selectInp, sqlCondInp) ]

def getUserInfoToDict(conn, user_name, zone=""):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
                
    selectInp.init([COL_USER_NAME, COL_USER_ID, COL_USER_TYPE, COL_USER_ZONE,
                    COL_USER_INFO, COL_USER_COMMENT, COL_USER_CREATE_TIME,
                    COL_USER_MODIFY_TIME],
                   [0, 0, 0, 0, 0, 
                    0, 0, 0], 
                   8)
    if zone:
        sqlCondInp.init([COL_USER_NAME, COL_USER_ZONE], 
                        ["='%s'" % user_name,
                         "='%s'" % zone], 
                        2)
    else:
        sqlCondInp.init([COL_USER_NAME], 
                        ["='%s'" % user_name], 
                        1)
    
    columnNames = ["user_name", "user_id", "user_type_name", "zone_name",
                   "user_info", "r_comment", "create_ts",
                   "modify_ts"]
    
    l =  queryToFormatDictList(conn, selectInp, sqlCondInp, columnNames)
    
    if len(l) > 0:
        return l[0]
    else:
        return {}

def getZoneInfoToDict(conn, zone_name, zone=""):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
                
    selectInp.init([COL_ZONE_ID, COL_ZONE_NAME, COL_ZONE_TYPE, 
                    COL_ZONE_CONNECTION, COL_ZONE_COMMENT, COL_ZONE_CREATE_TIME,
                    COL_ZONE_MODIFY_TIME],
                   [0, 0, 0, 0, 0, 0, 0], 
                   7)

    sqlCondInp.init([COL_ZONE_NAME], ["='%s'" % zone_name], 1)
    
    columnNames = ["zone_id", "zone_name", "zone_type_name", 
                   "zone_conn_string", "r_comment", "create_ts", "modify_ts"]
    
    l =  queryToFormatDictList(conn, selectInp, sqlCondInp, columnNames)
    
    if len(l) > 0:
        return l[0]
    else:
        return {}

def modifyObject(conn, objType, objName, fieldName, fieldValue):
    generalAdminInp = generalAdminInp_t ()
    
    generalAdminInp.arg0 = "modify"
    generalAdminInp.arg1 = objType
    generalAdminInp.arg2 = objName
    generalAdminInp.arg3 = fieldName
    generalAdminInp.arg4 = fieldValue
    generalAdminInp.arg5 = ""
    generalAdminInp.arg6 = ""
    generalAdminInp.arg7 = ""
    generalAdminInp.arg8 = ""
    generalAdminInp.arg9 = ""

    return rcGeneralAdmin(conn, generalAdminInp)

## Factorize the call to modAVUMetadata
## objType = -d -C, -R, -u,...
## action = add, rm
def procUserMetadata(conn, action, objType, name, attName, attValue, attUnits):
    modAVUMetadataInp = modAVUMetadataInp_t()   
    
    modAVUMetadataInp.arg0 = action
    modAVUMetadataInp.arg1 = objType
    modAVUMetadataInp.arg2 = name
    modAVUMetadataInp.arg3 = attName
    modAVUMetadataInp.arg4 = attValue
    modAVUMetadataInp.arg5 = attUnits
    modAVUMetadataInp.arg6 = ""
    modAVUMetadataInp.arg7 = ""
    modAVUMetadataInp.arg8 = ""
    modAVUMetadataInp.arg9 = ""
    
    return rcModAVUMetadata(conn, modAVUMetadataInp)

def queryToFormatDictList(conn, selectInp, sqlCondInp, formatStr):
    genQueryInp = genQueryInp_t()
    l = []
    
    genQueryInp.maxRows = MAX_SQL_ROWS
    genQueryInp.continueInx = 0
    genQueryInp.condInput.len = 0
    genQueryInp.selectInp = selectInp
    genQueryInp.sqlCondInp = sqlCondInp
    
    genQueryOut = rcGenQuery(conn, genQueryInp)
    
    if not genQueryOut:
        return l;
    addResultToFormatDictList(genQueryOut, formatStr, l)
    
    while genQueryOut and genQueryOut.continueInx > 0:
        genQueryInp.continueInx = genQueryOut.continueInx
        genQueryOut = rcGenQuery(conn, genQueryInp)
        if genQueryOut:
            addResultToFormatDictList(genQueryOut, l)
    
    return l

def queryToTupleList(conn, selectInp, sqlCondInp):
    genQueryInp = genQueryInp_t()
    l = []
    
    genQueryInp.maxRows = MAX_SQL_ROWS
    #genQueryInp.maxRows = 5
    genQueryInp.continueInx = 0
    genQueryInp.condInput.len = 0
    genQueryInp.selectInp = selectInp
    genQueryInp.sqlCondInp = sqlCondInp
    
    genQueryOut = rcGenQuery(conn, genQueryInp)
    
    if not genQueryOut:
        return l;
    
    addResultToTupleList(genQueryOut, l)
    
    while genQueryOut and genQueryOut.continueInx > 0:
        genQueryInp.continueInx = genQueryOut.continueInx
    
        genQueryOut = rcGenQuery(conn, genQueryInp)
    
        if genQueryOut:
            addResultToTupleList(genQueryOut, l);
    
    return l;

def rmObject(conn, objType, objName, arg3):
    generalAdminInp = generalAdminInp_t ()
    
    generalAdminInp.arg0 = "rm"
    generalAdminInp.arg1 = objType
    generalAdminInp.arg2 = objName
    generalAdminInp.arg3 = arg3
    generalAdminInp.arg4 = ""
    generalAdminInp.arg5 = ""
    generalAdminInp.arg6 = ""
    generalAdminInp.arg7 = ""
    generalAdminInp.arg8 = ""
    generalAdminInp.arg9 = ""
    
    return rcGeneralAdmin(conn, generalAdminInp)

def rmUserMetadata(conn, obj_type, name, attName, attValue, attUnits):
    return procUserMetadata(conn, "rm", obj_type, name, attName, attValue, 
                            attUnits)

## return a list of dictionaries:
##   keys: 
##     resource: Resource name
##     user: User name
##     zone: zone name
##     usage: nb bits used
##     time: time set
def getUserUsage(userName, usersZone):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
    
    selectInp.init([COL_QUOTA_USAGE_MODIFY_TIME,
                    COL_QUOTA_RESC_NAME,
                    COL_QUOTA_USER_NAME,
                    COL_QUOTA_USER_ZONE,
                    COL_QUOTA_USAGE],
                   [0,0,0,0,0],
                   5)
    
    colName = ["time", "resource", "user", "zone", "usage"]
    
    if userName:
        sqlCondInp.init([COL_QUOTA_USER_NAME],
                        ["='%s'" % userName],
                        1)
    else:
        sqlCondInp.init([], [], 0)
    
    l =  queryToTupleList(conn, selectInp, sqlCondInp)
    
    res = []
    
    for el in l:
        d = dict(zip(colName, el))
        d['time'] = getLocalTimeFromRodsTime(d['time'])
        d['usage'] = int(d['usage'])
        res.append(d)
    
    return res

## return the list of groups for the user
def getUserGroupMembership(conn, userName, zoneName):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
    
    selectInp.init([COL_USER_GROUP_NAME],
                   [0],
                   1)
    
    sqlCondInp.init([COL_USER_NAME, COL_USER_ZONE],
                    ["='%s'" % userName, "='%s'" % zoneName],
                    2)
    
    l =  queryToTupleList(conn, selectInp, sqlCondInp)
    
    return l

## userQ = boolean (true means user, false means group)
## GlobalQ = boolean (true means global, false means resource)
## return a list of dictionaries:
##   keys: 
##     resource: Resource name
##     user/group: User or Group name
##     zone: zone name
##     quota: set quota (in bits)
##     over: nb bits over quota (<0 means under quota)
##     time: time set
def getQuota(conn, userName, userQ, globalQ):
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
    
    printCount = 0
    i = 0
    
    colName = []
    inputInx = []
    inputVal = []
    
    if not globalQ:
        colName.append("resource")
        inputInx.append(COL_QUOTA_RESC_NAME)
        inputVal.append(0)
    else:
        colName.append("resource")
        inputInx.append(COL_QUOTA_RESC_ID)
        inputVal.append(0)
    
    if userQ:
        colName.append("user")
    else:
        colName.append("group")
    inputInx.append(COL_QUOTA_USER_NAME)
    inputVal.append(0)
    
    colName.append("zone")
    inputInx.append(COL_QUOTA_USER_ZONE)
    inputVal.append(0)
    
    colName.append("quota")
    inputInx.append(COL_QUOTA_LIMIT)
    inputVal.append(0)
    
    colName.append("over")
    inputInx.append(COL_QUOTA_OVER)
    inputVal.append(0)
    
    colName.append("time")
    inputInx.append(COL_QUOTA_MODIFY_TIME)
    inputVal.append(0)
    
    selectInp.init(inputInx, inputVal, len(inputInx))
    
    inputCond = []
    condVal = []
    
    if userName:
        userName2 = ""
        userZone = ""
        status, userName2, userZone = parseUserName(userName)
        
        if not userZone:
            inputCond.append(COL_QUOTA_USER_NAME)
            condVal.append("='%s'" % userName)
        else:
            inputCond.append(COL_QUOTA_USER_NAME)
            condVal.append("='%s'" % userName2)
            inputCond.append(COL_QUOTA_USER_ZONE)
            condVal.append("='%s'" % userZone)
    
    inputCond.append(COL_QUOTA_USER_TYPE)
    if userQ:
        condVal.append("!='rodsgroup'")
    else:
        condVal.append("='rodsgroup'")
    
    if globalQ:
        inputCond.append(COL_QUOTA_RESC_ID)
        condVal.append("='0'")
    
    sqlCondInp.init(inputCond, condVal, len(inputCond))
    
    l =  queryToTupleList(conn, selectInp, sqlCondInp)
    
    res = []
    
    for el in l:
        d = dict(zip(colName, el))
        if globalQ:
            d['resource'] = "All"
        d['time'] = getLocalTimeFromRodsTime(d['time'])
        d['over'] = int(d['over'])
        d['quota'] = int(d['quota'])
        res.append(d)
    
    return res

def getUserQuotaGlobal(conn, userName):
    return getQuota(conn, userName, True, True)

def getUserQuotaResources(conn, userName):
    return getQuota(conn, userName, True, False)

def getGroupsQuotaGlobal(conn):
    return getQuota(conn, "", False, True)

def getGroupsQuotaResources(conn):
    return getQuota(conn, "", False, False)

def getUsersQuotaGlobal(conn):
    return getQuota(conn, "", True, True)

def getUsersQuotaResources(conn):
    return getQuota(conn, "", True, False)

%}