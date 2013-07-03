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

class testMiscUtil(iRODSTestCase):

    def test_collEnt_t(self):
        objType = UNKNOWN_OBJ_T
        specColl = specColl_t()
        tmp = create_collEnt_t(objType, 12, 12, 12, 12, "collName", 
                     "dataName", "dataId", "createTime", "modifyTime", "chksum", "resource", 
                     "rescGrp", "phyPath", "ownerName", specColl)
        self.assertEqual(tmp.objType, objType)
        self.assertEqual(tmp.replNum, 12)
        self.assertEqual(tmp.replStatus, 12)
        self.assertEqual(tmp.dataMode, 12)
        self.assertEqual(tmp.dataSize, 12)
        self.assertEqual(tmp.collName, "collName")
        self.assertEqual(tmp.dataName, "dataName")
        self.assertEqual(tmp.dataId, "dataId")
        self.assertEqual(tmp.createTime, "createTime")
        self.assertEqual(tmp.modifyTime, "modifyTime")
        self.assertEqual(tmp.chksum, "chksum")
        self.assertEqual(tmp.resource, "resource")
        self.assertEqual(tmp.rescGrp, "rescGrp")
        self.assertEqual(tmp.phyPath, "phyPath")
        self.assertEqual(tmp.ownerName, "ownerName")
        #self.assertEqual(tmp.specColl, specColl)

    def test_collHandle_t(self):
        state = COLL_CLOSED
        rodsObjStat = rodsObjStat_t()
        genQueryInp = genQueryInp_t()
        dataObjInp = dataObjInp_t()
        dataObjSqlResult = dataObjSqlResult_t()
        collSqlResult = collSqlResult_t()
        
        tmp = create_collHandle_t(state, 12, 12, 12, rodsObjStat, 
                        genQueryInp, dataObjInp, dataObjSqlResult, 
                        collSqlResult, "linkedObjPath", "prevdataId")
        self.assertEqual(tmp.state, state)
        self.assertEqual(tmp.inuseFlag, 12)
        self.assertEqual(tmp.flags, 12)
        self.assertEqual(tmp.rowInx, 12)
        #self.assertEqual(tmp.rodsObjStat, rodsObjStat)
        #self.assertEqual(tmp.queryHandle, queryHandle)
        #self.assertEqual(tmp.genQueryInp, genQueryInp)
        #self.assertEqual(tmp.dataObjInp, dataObjInp)
        #self.assertEqual(tmp.dataObjSqlResult, dataObjSqlResult)
        #self.assertEqual(tmp.collSqlResult, collSqlResult)
        self.assertEqual(tmp.linkedObjPath, "linkedObjPath")
        self.assertEqual(tmp.prevdataId, "prevdataId")

    def test_dataObjSqlResult_t(self):
        collName = sqlResult_t()
        collType = sqlResult_t()
        collInfo1 = sqlResult_t()
        collInfo2 = sqlResult_t()
        collOwner = sqlResult_t()
        collCreateTime = sqlResult_t()
        collModifyTime = sqlResult_t()
        tmp = create_collSqlResult_t(12, 12, 12, 12, collName, collType, 
                                     collInfo1, collInfo2, collOwner, 
                                     collCreateTime, collModifyTime)
        self.assertEqual(tmp.rowCnt, 12)
        self.assertEqual(tmp.attriCnt, 12)
        self.assertEqual(tmp.continueInx, 12)
        self.assertEqual(tmp.totalRowCount, 12)
#        self.assertEqual(tmp.collName, collName)
#        self.assertEqual(tmp.collType, collType)
#        self.assertEqual(tmp.collInfo1, collInfo1)
#        self.assertEqual(tmp.collInfo2, collInfo2)
#        self.assertEqual(tmp.collOwner, collOwner)
#        self.assertEqual(tmp.collCreateTime, collCreateTime)
#        self.assertEqual(tmp.collModifyTime, collModifyTime)

    def test_dataObjSqlResult_t(self):
        collName = sqlResult_t()
        dataName = sqlResult_t()
        dataMode = sqlResult_t()
        dataSize = sqlResult_t()
        createTime = sqlResult_t()
        modifyTime = sqlResult_t()
        chksum = sqlResult_t()
        replStatus = sqlResult_t()
        dataId = sqlResult_t()
        resource = sqlResult_t()
        phyPath = sqlResult_t()
        ownerName = sqlResult_t()
        replNum = sqlResult_t()
        rescGrp = sqlResult_t()
        dataType = sqlResult_t()
        tmp = create_dataObjSqlResult_t(12, 12, 12, 12, collName, dataName, 
                                        dataMode, dataSize, createTime, 
                                        modifyTime, chksum, replStatus, dataId, 
                                        resource, phyPath, ownerName, replNum, 
                                        rescGrp, dataType)
        self.assertEqual(tmp.rowCnt, 12)
        self.assertEqual(tmp.attriCnt, 12)
        self.assertEqual(tmp.continueInx, 12)
        self.assertEqual(tmp.totalRowCount, 12)
#        self.assertEqual(tmp.collName, collName)
#        self.assertEqual(tmp.dataName, dataName)
#        self.assertEqual(tmp.dataMode, dataMode)
#        self.assertEqual(tmp.dataSize, dataSize)
#        self.assertEqual(tmp.createTime, createTime)
#        self.assertEqual(tmp.modifyTime, modifyTime)
#        self.assertEqual(tmp.chksum, chksum)
#        self.assertEqual(tmp.replStatus, replStatus)
#        self.assertEqual(tmp.dataId, dataId)
#        self.assertEqual(tmp.resource, resource)
#        self.assertEqual(tmp.phyPath, phyPath)
#        self.assertEqual(tmp.ownerName, ownerName)
#        self.assertEqual(tmp.replNum, replNum)
#        self.assertEqual(tmp.rescGrp, rescGrp)
#        self.assertEqual(tmp.dataType, dataType)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testMiscUtil))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())