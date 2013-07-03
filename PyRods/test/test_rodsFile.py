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

class testRodsFile(iRODSTestCase):

    def test_fileChmodInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileChmodInp_t(#fileType, 
                                    addr, "fileName", 12)
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.fileName, "fileName")
        self.assertEqual(tmp.mode, 12)

    def test_fileChksumInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileChksumInp_t(#fileType, 
                                    addr, "fileName", 12)
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.fileName, "fileName")
        self.assertEqual(tmp.flag, 12)

    def test_fileCloseInp_t(self):
        tmp = create_fileCloseInp_t(12)
        self.assertEqual(tmp.fileInx, 12)

    def test_fileClosedirInp_t(self):
        tmp = create_fileClosedirInp_t(12)
        self.assertEqual(tmp.fileInx, 12)

    def test_fileFstatInp_t(self):
        tmp = create_fileFstatInp_t(12)
        self.assertEqual(tmp.fileInx, 12)

    def test_fileFsyncInp_t(self):
        tmp = create_fileFsyncInp_t(12)
        self.assertEqual(tmp.fileInx, 12)

    def test_fileGetFsFreeSpaceInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileGetFsFreeSpaceInp_t(#fileType, 
                                             addr, "fileName", 12)
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.fileName, "fileName")
        self.assertEqual(tmp.flag, 12)

    def test_fileGetFsFreeSpaceOut_t(self):
        tmp = create_fileGetFsFreeSpaceOut_t(12)
        self.assertEqual(tmp.size, 12)

    def test_fileLseekInp_t(self):
        tmp = create_fileLseekInp_t(12, 12, 12)
        self.assertEqual(tmp.fileInx, 12)
        self.assertEqual(tmp.offset, 12)
        self.assertEqual(tmp.whence, 12)

    def test_fileLseekOut_t(self):
        tmp = create_fileLseekOut_t(12)
        self.assertEqual(tmp.offset, 12)

    def test_fileMkdirInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        condInput = keyValPair_t()
        tmp = create_fileMkdirInp_t(#fileType, 
                                    addr, "dirName", 12, condInput)
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.dirName, "dirName")
        self.assertEqual(tmp.mode, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_fileOpenInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        condInput = keyValPair_t()
        tmp = create_fileOpenInp_t(#fileType, 
                                  12, addr, "fileName", 12, 12, 12, condInput)
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.fileName, "fileName")
        self.assertEqual(tmp.flags, 12)
        self.assertEqual(tmp.mode, 12)
        self.assertEqual(tmp.dataSize, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_fileOpendirInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileOpendirInp_t(#fileType, 
                                      addr, "dirName")
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.dirName, "dirName")

    def test_fileReadInp_t(self):
        tmp = create_fileReadInp_t(12, 12)
        self.assertEqual(tmp.fileInx, 12)
        self.assertEqual(tmp.len, 12)

    def test_fileRenameInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileRenameInp_t(#fileType, 
                                      addr, "oldFileName", "newFileName")
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.oldFileName, "oldFileName")
        self.assertEqual(tmp.newFileName, "newFileName")

    def test_fileRmdirInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileRmdirInp_t(#fileType, 
                                    12, addr, "dirName")
        #self.assertEqual(tmp.fileType, fileType)
        self.assertEqual(tmp.flags, 12)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.dirName, "dirName")

    def test_fileStageInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileStageInp_t(#fileType, 
                                    addr,  "fileName", 12)
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.fileName, "fileName")
        self.assertEqual(tmp.flag, 12)

    def test_fileStatInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileStatInp_t(#fileType, 
                                   addr, "fileName")
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.fileName, "fileName")

    def test_fileUnlinkInp_t(self):
        #fileType = fileDriverType_t()
        addr = rodsHostAddr_t()
        tmp = create_fileUnlinkInp_t(#fileType, 
                                     addr, "fileName")
        #self.assertEqual(tmp.fileType, fileType)
        #self.assertEqual(tmp.addr, addr)
        self.assertEqual(tmp.fileName, "fileName")

    def test_fileWriteInp_t(self):
        tmp = create_fileWriteInp_t(12, 12)
        self.assertEqual(tmp.fileInx, 12)
        self.assertEqual(tmp.len, 12)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsFile))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())