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

class testRodsDef(iRODSTestCase):

    def test_bytesBuf_t(self):
        tmp = create_bytesBuf_t("bytesBuf_t")
        self.assertEqual(tmp.getBuf(), "bytesBuf_t")

    def test_getTempPasswordOut_t(self):
        tmp = create_getTempPasswordOut_t("stringToHashWith")
        self.assertEqual(tmp.stringToHashWith, "stringToHashWith")

    def test_rodsDirent_t(self):
        tmp = create_rodsDirent_t(12, 12, 12, 12, "d_name")
        self.assertEqual(tmp.d_offset, 12)
        self.assertEqual(tmp.d_ino, 12)
        self.assertEqual(tmp.d_reclen, 12)
        self.assertEqual(tmp.d_namlen, 12)
        self.assertEqual(tmp.d_name, "d_name")

    def test_rodsHostAddr_t(self):
        tmp = create_rodsHostAddr_t("hostAddr", "zoneName", 12, 12)
        self.assertEqual(tmp.hostAddr, "hostAddr")
        self.assertEqual(tmp.zoneName, "zoneName")
        self.assertEqual(tmp.portNum, 12)
        self.assertEqual(tmp.dummyInt, 12)

    def test_rodsRestart_t(self):
        tmp = create_rodsRestart_t("restartFile", 12, 12, "collection", 
                                   "lastDonePath", "oprType", 12, 12)
        self.assertEqual(tmp.restartFile, "restartFile")
        self.assertEqual(tmp.fd, 12)
        self.assertEqual(tmp.doneCnt, 12)
        self.assertEqual(tmp.collection, "collection")
        self.assertEqual(tmp.lastDonePath, "lastDonePath")
        self.assertEqual(tmp.oprType, "oprType")
        self.assertEqual(tmp.curCnt, 12)
        self.assertEqual(tmp.restartState, 12)

    def test_rodsStat_t(self):
        tmp = create_rodsStat_t(12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 
                                12)
        self.assertEqual(tmp.st_size, 12)
        self.assertEqual(tmp.st_dev, 12)
        self.assertEqual(tmp.st_ino, 12)
        self.assertEqual(tmp.st_mode, 12)
        self.assertEqual(tmp.st_nlink, 12)
        self.assertEqual(tmp.st_uid, 12)
        self.assertEqual(tmp.st_gid, 12)
        self.assertEqual(tmp.st_rdev, 12)
        self.assertEqual(tmp.st_atim, 12)
        self.assertEqual(tmp.st_mtim, 12)
        self.assertEqual(tmp.st_ctim, 12)
        self.assertEqual(tmp.st_blksize, 12)
        self.assertEqual(tmp.st_blocks, 12)

    def test_version_t(self):
        tmp = create_version_t(12, "relVersion", "apiVersion", 12, "reconnAddr", 
                               12)
        self.assertEqual(tmp.status, 12)
        self.assertEqual(tmp.relVersion, "relVersion")
        self.assertEqual(tmp.apiVersion, "apiVersion")
        self.assertEqual(tmp.reconnPort, 12)
        self.assertEqual(tmp.reconnAddr, "reconnAddr")
        self.assertEqual(tmp.cookie, 12)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsDef))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())