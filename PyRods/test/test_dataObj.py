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

class testDataObj(iRODSTestCase):

    def test_collInp_t(self):
        condInput = keyValPair_t()
        tmp = create_collInp_t("collName", 12, 12, condInput)
        self.assertEqual(tmp.collName, "collName")
        self.assertEqual(tmp.flags, 12)
        self.assertEqual(tmp.oprType, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_dataCopyInp_t(self):
        dataOprInp = dataOprInp_t()
        portalOprOut = portalOprOut_t()
        tmp = create_dataCopyInp_t(dataOprInp, portalOprOut)
        self.assertIsNotNone(tmp)
        #self.assertEqual(tmp.dataOprInp, dataOprInp)
        #self.assertEqual(tmp.portalOprOut, portalOprOut)

    def test_dataObjCopyInp_t(self):
        srcDataObjInp = dataObjInp_t()
        destDataObjInp = dataObjInp_t()
        tmp = create_dataObjCopyInp_t(srcDataObjInp, destDataObjInp)

    def test_dataObjInp_t(self):
        specColl = specColl_t()
        condInput = keyValPair_t()
        tmp = create_dataObjInp_t("objPath", 12, 12, 12, 12, 12, 12, specColl,
                                  condInput)
        self.assertEqual(tmp.objPath, "objPath")
        self.assertEqual(tmp.createMode, 12)
        self.assertEqual(tmp.openFlags, 12)
        self.assertEqual(tmp.offset, 12)
        self.assertEqual(tmp.dataSize, 12)
        self.assertEqual(tmp.numThreads, 12)
        self.assertEqual(tmp.oprType, 12)
        #self.assertEqual(tmp.specColl, specColl)
        #self.assertEqual(tmp.condInput, condInput)

    def test_dataOprInp_t(self):
        condInput = keyValPair_t()
        tmp =  create_dataOprInp_t(12, 12, 12, 12, 12, 12, 12, 12, condInput)
        self.assertEqual(tmp.oprType, 12)
        self.assertEqual(tmp.numThreads, 12)
        self.assertEqual(tmp.srcL3descInx, 12)
        self.assertEqual(tmp.destL3descInx, 12)
        self.assertEqual(tmp.srcRescTypeInx, 12)
        self.assertEqual(tmp.destRescTypeInx, 12)
        self.assertEqual(tmp.offset, 12)
        self.assertEqual(tmp.dataSize, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_openedDataObjInp_t(self):
        condInput = keyValPair_t()
        tmp =  create_openedDataObjInp_t(12, 12, 12, 12, 12, 12, condInput)
        self.assertEqual(tmp.l1descInx, 12)
        self.assertEqual(tmp.len, 12)
        self.assertEqual(tmp.whence, 12)
        self.assertEqual(tmp.oprType, 12)
        self.assertEqual(tmp.offset, 12)
        self.assertEqual(tmp.bytesWritten, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_openStat_t(self):
        tmp = create_openStat_t(12, "dataType", "dataMode", 12, 12, 12, 12)
        self.assertEqual(tmp.dataSize, 12)
        self.assertEqual(tmp.dataType, "dataType")
        self.assertEqual(tmp.dataMode, "dataMode")
        self.assertEqual(tmp.l3descInx, 12)
        self.assertEqual(tmp.replStatus, 12)
        self.assertEqual(tmp.rescTypeInx, 12)
        self.assertEqual(tmp.replNum, 12)
        return tmp

    def test_portalOprOut_t(self):
        portList = portList_t()
        tmp = create_portalOprOut_t(12, 12, 12, "chksum", portList)
        self.assertEqual(tmp.status, 12)
        self.assertEqual(tmp.l1descInx, 12)
        self.assertEqual(tmp.numThreads, 12)
        self.assertEqual(tmp.chksum, "chksum")
        #self.assertEqual(tmp.portList, portList)
        return tmp

    def test_portList_t_unicode(self):
        tmp = create_portList_t(12, 12, 12, u"hostAddr")
        self.assertEqual(tmp.portNum, 12)
        self.assertEqual(tmp.cookie, 12)
        self.assertEqual(tmp.windowSize, 12)
        self.assertEqual(tmp.hostAddr, u"hostAddr")
        return tmp

    def test_collInp_t_unicode(self):
        condInput = keyValPair_t()
        tmp = create_collInp_t(u"collName", 12, 12, condInput)
        self.assertEqual(tmp.collName, u"collName")
        self.assertEqual(tmp.flags, 12)
        self.assertEqual(tmp.oprType, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_dataObjInp_t_unicode(self):
        specColl = specColl_t()
        condInput = keyValPair_t()
        tmp = create_dataObjInp_t(u"objPath", 12, 12, 12, 12, 12, 12, specColl,
                                  condInput)
        self.assertEqual(tmp.objPath, u"objPath")
        self.assertEqual(tmp.createMode, 12)
        self.assertEqual(tmp.openFlags, 12)
        self.assertEqual(tmp.offset, 12)
        self.assertEqual(tmp.dataSize, 12)
        self.assertEqual(tmp.numThreads, 12)
        self.assertEqual(tmp.oprType, 12)
        #self.assertEqual(tmp.specColl, specColl)
        #self.assertEqual(tmp.condInput, condInput)

    def test_openStat_t_unicode(self):
        tmp = create_openStat_t(12, u"dataType", u"dataMode", 12, 12, 12, 12)
        self.assertEqual(tmp.dataSize, 12)
        self.assertEqual(tmp.dataType, u"dataType")
        self.assertEqual(tmp.dataMode, u"dataMode")
        self.assertEqual(tmp.l3descInx, 12)
        self.assertEqual(tmp.replStatus, 12)
        self.assertEqual(tmp.rescTypeInx, 12)
        self.assertEqual(tmp.replNum, 12)
        return tmp

    def test_portalOprOut_t_unicode(self):
        portList = portList_t()
        tmp = create_portalOprOut_t(12, 12, 12, u"chksum", portList)
        self.assertEqual(tmp.status, 12)
        self.assertEqual(tmp.l1descInx, 12)
        self.assertEqual(tmp.numThreads, 12)
        self.assertEqual(tmp.chksum, u"chksum")
        #self.assertEqual(tmp.portList, portList)
        return tmp

    def test_portList_t_unicode(self):
        tmp = create_portList_t(12, 12, 12, u"hostAddr")
        self.assertEqual(tmp.portNum, 12)
        self.assertEqual(tmp.cookie, 12)
        self.assertEqual(tmp.windowSize, 12)
        self.assertEqual(tmp.hostAddr, u"hostAddr")
        return tmp



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testDataObj))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())