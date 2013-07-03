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

class testRodsInfo(iRODSTestCase):

    def test_dataObjInfo_t(self):
        #rescInfo = rescInfo_t()
        specColl = specColl_t()
        condInput = keyValPair_t()
        next = None
        tmp = create_dataObjInfo_t("objPath", "rescName", "rescGroupName", 
                                   "dataType", 12, "chksum", "version", 
                                   "filePath", #rescInfo, 
                                   "dataOwnerName", 
                                   "dataOwnerZone", 12, 12, "statusString", 
                                   12, 12, 12, 12, "dataComments", "dataMode", 
                                   "dataExpiry", "dataCreate", "dataModify", 
                                   "dataAccess", 12, 12, "destRescName", 
                                   "backupRescName", "subPath", specColl, 12, 
                                   12, condInput, next)
        self.assertEqual(tmp.objPath, "objPath")
        self.assertEqual(tmp.rescName, "rescName")
        self.assertEqual(tmp.rescGroupName, "rescGroupName")
        self.assertEqual(tmp.dataType, "dataType")
        self.assertEqual(tmp.dataSize, 12)
        self.assertEqual(tmp.chksum, "chksum")
        self.assertEqual(tmp.version, "version")
        self.assertEqual(tmp.filePath, "filePath")
        #self.assertEqual(tmp.rescInfo, rescInfo)
        self.assertEqual(tmp.dataOwnerName, "dataOwnerName")
        self.assertEqual(tmp.dataOwnerZone, "dataOwnerZone")
        self.assertEqual(tmp.replNum, 12)
        self.assertEqual(tmp.replStatus, 12)
        self.assertEqual(tmp.statusString, "statusString")
        self.assertEqual(tmp.dataId, 12)
        self.assertEqual(tmp.collId, 12)
        self.assertEqual(tmp.dataMapId, 12)
        self.assertEqual(tmp.flags, 12)
        self.assertEqual(tmp.dataComments, "dataComments")
        self.assertEqual(tmp.dataMode, "dataMode")
        self.assertEqual(tmp.dataExpiry, "dataExpiry")
        self.assertEqual(tmp.dataCreate, "dataCreate")
        self.assertEqual(tmp.dataModify, "dataModify")
        self.assertEqual(tmp.dataAccess, "dataAccess")
        self.assertEqual(tmp.dataAccessInx, 12)
        self.assertEqual(tmp.writeFlag, 12)
        self.assertEqual(tmp.destRescName, "destRescName")
        self.assertEqual(tmp.backupRescName, "backupRescName")
        self.assertEqual(tmp.subPath, "subPath")
        #self.assertEqual(tmp.specColl, specColl)
        self.assertEqual(tmp.regUid, 12)
        self.assertEqual(tmp.otherFlags, 12)
        #self.assertEqual(tmp.condInput, condInput)
        #self.assertEqual(tmp.next, next)

    def test_inxValPair_t(self):
        l1 = [1, 2, 3]
        l2 = ["1", "2", "3"]
        tmp = create_inxValPair_t(l1, l2, len(l1))
        self.assertEqual(tmp.getInx(), l1)
        self.assertEqual(tmp.getValue(), l2)

    def test_inxIvalPair_t(self):
        l1 = [1, 2, 3]
        l2 = [12, 13, 14]
        tmp = create_inxIvalPair_t(l1, l2, len(l1))
        self.assertEqual(tmp.getInx(), l1)
        self.assertEqual(tmp.getValue(), l2)

    def test_keyValPair_t(self):
        l1 = ["one", "two", "three"]
        l2 = ["1", "2", "3"]
        tmp = create_keyValPair_t(l1, l2, len(l1))
        self.assertEqual(tmp.getKeyWord(), l1)
        self.assertEqual(tmp.getValue(), l2)

    def test_miscSvrInfo_t(self):
        tmp = create_miscSvrInfo_t(12, 12, "relVersion", "apiVersion", 
                                   "rodsZone")
        self.assertEqual(tmp.serverType, 12)
        self.assertEqual(tmp.serverBootTime, 12)
        self.assertEqual(tmp.relVersion, "relVersion")
        self.assertEqual(tmp.apiVersion, "apiVersion")
        self.assertEqual(tmp.rodsZone, "rodsZone")

    def test_rodsObjStat_t(self):
        objType = UNKNOWN_OBJ_T
        specColl = specColl_t()
        tmp = create_rodsObjStat_t(12, objType, 12, "dataId", "chksum", 
                                   "ownerName", "ownerZone", "createTime", 
                                   "modifyTime", specColl)
        self.assertEqual(tmp.objSize, 12)
        self.assertEqual(tmp.objType, objType)
        self.assertEqual(tmp.dataMode, 12)
        self.assertEqual(tmp.dataId, "dataId")
        self.assertEqual(tmp.chksum, "chksum")
        self.assertEqual(tmp.ownerName, "ownerName")
        self.assertEqual(tmp.ownerZone, "ownerZone")
        self.assertEqual(tmp.createTime, "createTime")
        self.assertEqual(tmp.modifyTime, "modifyTime")
        #self.assertEqual(tmp.specColl, specColl)

    def test_specColl_t(self):
        #collClass = specCollClass_t
        #type = HAAW_STRUCT_FILE_T
        tmp = create_specColl_t(#collClass, 
                                #type, 
                                "collection", "objPath", 
                                "resource", "phyPath", "cacheDir", 12, 12)
        #self.assertEqual(tmp.collClass, collClass)
        #self.assertEqual(tmp.type, type)
        self.assertEqual(tmp.collection, "collection")
        self.assertEqual(tmp.objPath, "objPath")
        self.assertEqual(tmp.resource, "resource")
        self.assertEqual(tmp.phyPath, "phyPath")
        self.assertEqual(tmp.cacheDir, "cacheDir")
        self.assertEqual(tmp.cacheDirty, 12)
        self.assertEqual(tmp.replNum, 12)

    def test_subFile_t(self):
        addr = rodsHostAddr_t()
        specColl = specColl_t()
        tmp = create_subFile_t(addr, "subFilePath", 12, 12, 12, specColl)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.subFilePath, "subFilePath")
        self.assertEqual(tmp.mode, 12)
        self.assertEqual(tmp.flags, 12)
        self.assertEqual(tmp.offset, 12)
        #self.assertEqual(tmp.specColl, specColl)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsInfo))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())