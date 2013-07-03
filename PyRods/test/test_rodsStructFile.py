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

class testRodsStructFile(iRODSTestCase):

    def test_structFileExtAndRegInp_t(self):
        condInput = keyValPair_t()
        tmp = create_structFileExtAndRegInp_t("objPath", "collection", 12, 12, 
                                              condInput)
        self.assertEqual(tmp.objPath, "objPath")
        self.assertEqual(tmp.collection, "collection")
        self.assertEqual(tmp.oprType, 12)
        self.assertEqual(tmp.flags, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_structFileOprInp_t(self):
        addr = rodsHostAddr_t()
        specColl = specColl_t()
        condInput = keyValPair_t()
        tmp = create_structFileOprInp_t(addr, 12, 12, specColl, condInput)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.oprType, 12)
        self.assertEqual(tmp.flags, 12)
        #self.assertEqual(tmp.specColl, specColl)
        #self.assertEqual(tmp.condInput, condInput)

    def test_subStructFileFdOprInp_t(self):
        addr = rodsHostAddr_t()
        #type = structFileType_t()
        tmp = create_subStructFileFdOprInp_t(addr, #type, 
                                             12, 12)
        #self.assertEqual(tmp.addr, addr)
        #self.assertEqual(tmp.type, type)
        self.assertEqual(tmp.fd, 12)
        self.assertEqual(tmp.len, 12)

    def test_subStructFileLseekInp_t(self):
        addr = rodsHostAddr_t()
        #type = structFileType_t()
        tmp = create_subStructFileLseekInp_t(addr, #type, 
                                             12, 12, 12)
        #self.assertEqual(tmp.addr, addr)
        #self.assertEqual(tmp.type, type)
        self.assertEqual(tmp.fd, 12)
        self.assertEqual(tmp.offset, 12)
        self.assertEqual(tmp.whence, 12)

    def test_subStructFileRenameInp_t(self):
        subFile = subFile_t()
        tmp = create_subStructFileRenameInp_t(subFile, "newSubFilePath")
        #self.assertEqual(tmp.subFile, subFile)
        self.assertEqual(tmp.newSubFilePath, "newSubFilePath")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsStructFile))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())