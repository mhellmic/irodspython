# Copyright (c) 2013, University of Liverpool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Author       : Jerome Fuselier
#

import unittest
from common import *
from irods import *

USERNAME = "testUser"
GROUPNAME = "testGroup"
ZONENAME = "testZone"
RESCNAME = "testResc"

class testRodsUser(iRODSTestCase):

    def test_authInfo_t(self):
        tmp = create_authInfo_t("authScheme" , 12 , 12 , 12 , "host" , 
                                "authStr")
        self.assertEqual(tmp.authScheme, "authScheme")
        self.assertEqual(tmp.authFlag, 12)
        self.assertEqual(tmp.flag, 12)
        self.assertEqual(tmp.ppid, 12)
        self.assertEqual(tmp.host, "host")
        self.assertEqual(tmp.authStr, "authStr")

    def test_userInfo_t(self):
        authInfo = authInfo_t()
        userOtherInfo = userOtherInfo_t()
        tmp = create_userInfo_t("userName", "rodsZone", "userType", 12, 
                                authInfo, userOtherInfo)
        self.assertEqual(tmp.userName, "userName")
        self.assertEqual(tmp.rodsZone, "rodsZone")
        self.assertEqual(tmp.userType, "userType")
        self.assertEqual(tmp.sysUid, 12)
        #self.assertEqual(tmp.authInfo, authInfo)
        #self.assertEqual(tmp.userOtherInfo, userOtherInfo)

    def test_userOtherInfo_t(self):
        tmp = create_userOtherInfo_t("userInfo", "userComments", "userCreate", 
                                     "userModify")
        self.assertEqual(tmp.userInfo, "userInfo")
        self.assertEqual(tmp.userComments, "userComments")
        self.assertEqual(tmp.userCreate, "userCreate")
        self.assertEqual(tmp.userModify, "userModify")
        
    def testIrodsUserInfos(self):
        user = createUser(self.conn, USERNAME, "rodsadmin")
        infos = [user.getId(), user.getName(), user.getTypeName(), user.getZone(),
                 user.getInfo(), user.getComment(), user.getCreateTs(),
                 user.getModifyTs()]
        user.setInfo("v1")
        user.setComment("v2")
        new_infos = infos[:]
        new_infos[4] = "v1"
        new_infos[5] = "v2"
        
        infos = [user.getId(), user.getName(), user.getTypeName(), user.getZone(),
                 user.getInfo(), user.getComment(), user.getCreateTs(),
                 new_infos[-1]] # The modify time should change
        self.assertTrue(infos == new_infos)
        deleteUser(self.conn, USERNAME)
        
    def testIrodsUserPassword(self):
        status, password = obfGetPw()
        
    def testIrodsUserMeta(self):
        user = getUser(self.conn, self.myEnv.rodsUserName)
    
        user.addUserMetadata("test1", "value1")
        user.addUserMetadata("test2", "value2", "units")
        
        md = user.getUserMetadata()
        self.assertTrue(("test1", "value1", "") in md)
        self.assertTrue(("test2", "value2", "units") in md)
        
        user.rmUserMetadata("test1", "value1")
        user.rmUserMetadata("test2", "value2", "units")
        
    def testIrodsUsers(self):
        users_names = [ user.getName() for user in getUsers(self.conn) ]
        # the actual used user should be in the list of existing users 
        self.assertTrue(self.myEnv.rodsUserName in users_names)
        
    def testIrodsUserGroup(self):
        # just take the first group and check that this group has the user as a 
        # member        
        user = createUser(self.conn, USERNAME, "rodsadmin")
        g_names =  [ group.getName() for group in user.getGroups() ]
        
        group = getGroup(self.conn, g_names[0])
        members_names = [ user.getName() for user in group.getMembers() ] 
        self.assertTrue(USERNAME in members_names)
        
        deleteUser(self.conn, USERNAME)
        
    def testIrodsGroupInfos(self):
        group = createGroup(self.conn, GROUPNAME)
        infos = [group.getId(), group.getName(), group.getTypeName(), group.getZone(),
                 group.getInfo(), group.getComment(), group.getCreateTs(),
                 group.getModifyTs()]
        group.setInfo("v1")
        group.setComment("v2")
        new_infos = infos[:]
        new_infos[4] = "v1"
        new_infos[5] = "v2"
        infos = [group.getId(), group.getName(), group.getTypeName(), group.getZone(),
                 group.getInfo(), group.getComment(), group.getCreateTs(),
                 new_infos[-1]]
        self.assertTrue(infos == new_infos)
        deleteGroup(self.conn, GROUPNAME)
        
    def testIrodsGroupMeta(self):
        group = getGroup(self.conn, "public")
    
        group.addUserMetadata("test1", "value1")
        group.addUserMetadata("test2", "value2", "units")
        
        md = group.getUserMetadata()
        self.assertTrue(("test1", "value1", "") in md)
        self.assertTrue(("test2", "value2", "units") in md)
        
        group.rmUserMetadata("test1", "value1")
        group.rmUserMetadata("test2", "value2", "units")
        
    def testIrodsGroups(self):
        group = createGroup(self.conn, GROUPNAME)
        groups_names = [ group.getName() for group in getGroups(self.conn) ]
        # the public and test groups should be in the list of existing groups 
        self.assertTrue("public" in groups_names)
        self.assertTrue(GROUPNAME in groups_names)
        deleteGroup(self.conn, GROUPNAME)
        
    def testIrodsGroupUser(self):
        group = createGroup(self.conn, GROUPNAME)
        group.addUser(self.myEnv.rodsUserName)
        user_names = [ user.getName() for user in group.getMembers() ]
        self.assertTrue(self.myEnv.rodsUserName in user_names)
        deleteGroup(self.conn, GROUPNAME)
        
    def testIrodsZoneInfos(self):
        zone = getZone(self.conn, self.myEnv.rodsZone)
        infos = [zone.getId(), zone.getName(), zone.getTypeName(), zone.getConnString(),
                 zone.getComment(), zone.getCreateTs(), zone.getModifyTs()]
        tmp1 = zone.getConnString()
        tmp2 = zone.getComment()
        zone.setConnString("v1")
        zone.setComment("v2")
        new_infos = infos[:]
        new_infos[3] = "v1"
        new_infos[4] = "v2"
        infos = [zone.getId(), zone.getName(), zone.getTypeName(), zone.getConnString(),
                 zone.getComment(), zone.getCreateTs(), infos[-1]]
        self.assertTrue(infos == new_infos)
        zone.setConnString(tmp1)
        zone.setComment(tmp2)
        
    def testIrodsZones(self):
        zone = createZone(self.conn, ZONENAME, "remote", comment="test")
        zones_names = [ z.getName() for z in getZones(self.conn) ]
        self.assertTrue(zone.getName() in zones_names)
        self.assertTrue(self.myEnv.rodsZone in zones_names)
        deleteZone(self.conn, ZONENAME) 
        
    def testIrodsResourceInfos(self):
        resc = createResource(self.conn, RESCNAME, "unix file system", "archive", 
                              "localhost", " /tmp")
        
        infos = [resc.getId(), resc.getName(),  resc.getZone(), resc.getTypeName(),
                 resc.getClassName(), resc.getHost(), resc.getPath(), 
                 resc.getFreeSpace(), resc.getFreeSpaceTs(), resc.getInfo(),
                 resc.getComment(), resc.getCreateTs(), resc.getModifyTs()]
        resc.setTypeName("unix file system")
        resc.setClassName("archive")
        resc.setHost("localhost.localdomain")
        resc.setPath("/tmp2")
        resc.setComment("Useful comment")
        resc.setInfo("Useful info")
        resc.setFreeSpace("free comment")
        new_infos = infos[:]
        new_infos[3] = "unix file system"
        new_infos[4] = "archive"
        new_infos[5] = "localhost.localdomain"
        new_infos[6] = "/tmp2"
        new_infos[7] = "free comment"
        new_infos[9] = "Useful info"
        new_infos[10] = "Useful comment"
        
        infos = [resc.getId(), resc.getName(),  resc.getZone(), resc.getTypeName(),
                 resc.getClassName(), resc.getHost(), resc.getPath(), 
                 resc.getFreeSpace(), new_infos[8], resc.getInfo(),
                 resc.getComment(), resc.getCreateTs(), 
                 new_infos[-1]] # The modify time should change
                
        self.assertTrue(infos == new_infos)
        
        deleteResource(self.conn, RESCNAME)
        
    def testIrodsResourceMetas(self):
        resc = getResource(self.conn, self.myEnv.rodsDefResource)
    
        resc.addUserMetadata("test1", "value1")
        resc.addUserMetadata("test2", "value2", "units")
        
        md = resc.getUserMetadata()
        self.assertTrue(("test1", "value1", "") in md)
        self.assertTrue(("test2", "value2", "units") in md)
        
        resc.rmUserMetadata("test1", "value1")
        resc.rmUserMetadata("test2", "value2", "units")
        
    def testIrodsResources(self):
        rescs_names = [ resc.getName() for resc in getResources(self.conn) ]
        self.assertTrue(self.myEnv.rodsDefResource in rescs_names)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsUser))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())