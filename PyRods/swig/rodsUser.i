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

%pythoncode %{

class irodsGroup:

    def __init__(self, conn, groupName):
        self._conn = conn
        self.groupName = groupName

    def addUser(self, name, zone=""):
        if zone:
            namezone = "%s#%s" % (name, zone)
        else:
            namezone = name
        return modifyObject(self._conn, "group", self.groupName,
                            "add", namezone)

    def addUserMetadata(self, name, value, units=""):
        return addUserMetadata(self._conn, "-u", self.groupName, name, value, units)

    def getComment(self):
        d = self.getInfos()
        return d.get("r_comment", "")

    def getCreateTs(self):
        d = self.getInfos()
        return d.get("create_ts", "")

    def getId(self):
        d = self.getInfos()
        return d.get("user_id", "")

    def getInfo(self):
        d = self.getInfos()
        return d.get("user_info", "")

    def getInfos(self):
        return getUserInfoToDict(self._conn, self.groupName)

    def getMembers(self):
        l = getGroupMembers(self._conn, self.groupName)
        return [ irodsUser(self._conn, name, zone) for (name, zone) in l ]

    def getModifyTs(self):
        d = self.getInfos()
        return d.get("modify_ts", "")

    def getName(self):
        return self.groupName

    def getTypeName(self):
        d = self.getInfos()
        return d.get("user_type_name", "")

    def getUserMetadata(self):
        sqlCondInp = inxValPair_t()
        selectInp = inxIvalPair_t()
        selectInp.init([COL_META_USER_ATTR_NAME, COL_META_USER_ATTR_VALUE,
                        COL_META_USER_ATTR_UNITS],
                       [0, 0, 0], 3)
        sqlCondInp.init([COL_USER_NAME], ["='%s'" % self.groupName], 1)
        return queryToTupleList(self._conn, selectInp, sqlCondInp)

    def getZone(self):
        d = self.getInfos()
        return d.get("zone_name", "")

    def rmUser(self, userName, userZone=""):
        if userZone:
            namezone = "%s#%s" % (name, userZone)
        else:
            namezone = userName
        return modifyObject(self._conn, "group", self.groupName,
                            "remove", namezone)

    def rmUserMetadata(self, name, value, units=""):
        return rmUserMetadata(self._conn, "-u", self.groupName,
                               name, value, units) 

    def setComment(self, value):
        return modifyObject(self._conn, "user", self.groupName, "comment", value)

    def setInfo(self, value):
        return modifyObject(self._conn, "user", self.groupName, "info", value)

class irodsResource:

    def __init__(self, conn, resc_name):
        self._conn = conn
        self.name = resc_name

    def addUserMetadata(self, name, value, units=""):
        return addUserMetadata(self._conn, "-r", self.name, name, value, units)

    def getClassName(self):
        d = self.getInfos()
        return d.get("resc_class_name", "")

    def getComment(self):
        d = self.getInfos()
        return d.get("r_comment", "")

    def getCreateTs(self):
        d = self.getInfos()
        return d.get("create_ts", "")

    def getFreeSpace(self):
        d = self.getInfos()
        return d.get("free_space", "")

    def getFreeSpaceTs(self):
        d = self.getInfos()
        return d.get("free_space_ts", "")

    def getHost(self):
        d = self.getInfos()
        return d.get("resc_net", "")

    def getId(self):
        d = self.getInfos()
        return d.get("resc_id", "")

    def getInfo(self):
        d = self.getInfos()
        return d.get("resc_info", "")

    def getInfos(self):
        return getRescInfoToDict(self._conn, self.name)

    def getModifyTs(self):
        d = self.getInfos()
        return d.get("modify_ts", "")

    def getName(self):
        return self.name

    def getPath(self):
        d = self.getInfos()
        return d.get("resc_def_path", "")
    
    def getTypeName(self):
        d = self.getInfos()
        return d.get("resc_type_name", "")

    def getUserMetadata(self):
        sqlCondInp = inxValPair_t()
        selectInp = inxIvalPair_t()
        selectInp.init([COL_META_RESC_ATTR_NAME, COL_META_RESC_ATTR_VALUE,
                        COL_META_RESC_ATTR_UNITS],
                       [0, 0, 0], 3)
        sqlCondInp.init([COL_R_RESC_NAME], ["='%s'" % self.name], 1)
        return queryToTupleList(self._conn, selectInp, sqlCondInp)

    def getZone(self):
        d = self.getInfos()
        return d.get("zone_name", "")

    def rmUserMetadata(self, name, value, units=""):
        return rmUserMetadata(self._conn, "-r", self.name,
                               name, value, units) 

    def setClassName(self, value):
        return modifyObject(self._conn, "resource", self.name, "class", value)

    def setComment(self, value):
        return modifyObject(self._conn, "resource", self.name, "comment", value)

    def setFreeSpace(self, value):
        return modifyObject(self._conn, "resource", self.name, "freespace", value)

    def setHost(self, value):
        return modifyObject(self._conn, "resource", self.name, "host", value)

    def setInfo(self, value):
        return modifyObject(self._conn, "resource", self.name, "info", value)

    def setPath(self, value):
        return modifyObject(self._conn, "resource", self.name, "path", value)

    def setTypeName(self, value):
        return modifyObject(self._conn, "resource", self.name, "type", value)

class irodsUser:

    def __init__(self, conn, userName, userZone):
        self._conn = conn
        self.userName = userName
        self.userZone = userZone

    def addUserMetadata(self, name, value, units=""):
        return addUserMetadata(self._conn, "-u", self.userName, name, value, units)

    def getComment(self):
        d = self.getInfos()
        return d.get("r_comment", "")

    def getCreateTs(self):
        d = self.getInfos()
        return d.get("create_ts", "")

    def getFullName(self):
        return "%s#%s" % (self.userName, self.userZone)

    def getGroups(self):
        sqlCondInp = inxValPair_t()
        selectInp = inxIvalPair_t()
        selectInp.init([COL_USER_GROUP_NAME],
                       [0], 1)
        sqlCondInp.init([COL_USER_NAME], 
                        ["='%s'" % self.userName], 1)
        l = queryToTupleList(self._conn, selectInp, sqlCondInp)
        return [ irodsGroup(self._conn, name) for name in l ]

    def getId(self):
        d = self.getInfos()
        return d.get("user_id", "")

    def getInfo(self):
        d = self.getInfos()
        return d.get("user_info", "")

    def getInfos(self):
        return getUserInfoToDict(self._conn, self.userName)

    def getModifyTs(self):
        d = self.getInfos()
        return d.get("modify_ts", "")

    def getName(self):
        return self.userName

    def getQuotaGlobal(self):
        return getQuota(self._conn, self.getFullName(), True, True)

    def getQuotaResources(self):
        return getQuota(self._conn, self.getFullName(), True, False)

    def getTypeName(self):
        d = self.getInfos()
        return d.get("user_type_name", "")

    def getUserMetadata(self):
        sqlCondInp = inxValPair_t()
        selectInp = inxIvalPair_t()
        selectInp.init([COL_META_USER_ATTR_NAME, COL_META_USER_ATTR_VALUE,
                        COL_META_USER_ATTR_UNITS],
                       [0, 0, 0], 3)
        sqlCondInp.init([COL_USER_NAME, COL_USER_ZONE], 
                        ["='%s'" % self.userName,
                         "='%s'" % self.userZone], 2)
        return queryToTupleList(self._conn, selectInp, sqlCondInp)

    def getZone(self):
        return self.userZone

    def rmUserMetadata(self, name, value, units=""):
        return rmUserMetadata(self._conn, "-u", self.userName,
                               name, value, units)

    def setComment(self, value):
        return modifyObject(self._conn, "user", self.userName, "comment", value)

    def setInfo(self, value):
        return modifyObject(self._conn, "user", self.userName, "info", value)

    def setPassword(self, new_pw):
        return setPassword(self._conn, self.userName, new_pw)

    def setTypeName(self, value):
        return modifyObject(self._conn, "user", self.userName, "type", value)

    def setZone(self, value):
        return modifyObject(self._conn, "user", self.userName, "zone", value)


class irodsZone:

    def __init__(self, conn, name):
        self._conn = conn
        self.name = name

    def __str__(self):
        return self.name

    def getComment(self):
        d = self.getInfos()
        return d.get("r_comment", "")

    def getConnString(self):
        d = self.getInfos()
        return d.get("zone_conn_string", "")

    def getCreateTs(self):
        d = self.getInfos()
        return d.get("create_ts", "")

    def getId(self):
        d = self.getInfos()
        return d.get("zone_id", "")

    def getInfos(self):
        return getZoneInfoToDict(self._conn, self.name)

    def getModifyTs(self):
        d = self.getInfos()
        return d.get("modify_ts", "")

    def getName(self):
        return self.name

    def getTypeName(self):
        d = self.getInfos()
        return d.get("zone_type_name", "")

    def setComment(self, value):
        return modifyObject(self._conn, "zone", self.name, "comment", value)

    def setConnString(self, value):
        return modifyObject(self._conn, "zone", self.name, "conn", value)


%}

/*****************************************************************************/

typedef struct {
    char authScheme[NAME_LEN];     /* Authentication scheme */
    int authFlag;   /* the status of authentication */
    int flag;       
    int ppid;       /* session ppid */
    char host[NAME_LEN]; /* session host */
    char authStr[NAME_LEN];      /* for gsi, the dn */
} authInfo_t;

typedef struct {
    char userName[NAME_LEN];
    char rodsZone[NAME_LEN];
    char userType[NAME_LEN];
    int sysUid;     /* the unix system uid */
    authInfo_t authInfo;
    userOtherInfo_t userOtherInfo;
} userInfo_t;

typedef struct {
    char userInfo[NAME_LEN]; 
    char userComments[NAME_LEN]; 
    char userCreate[TIME_LEN]; 
    char userModify[TIME_LEN];
} userOtherInfo_t;

/*****************************************************************************/
