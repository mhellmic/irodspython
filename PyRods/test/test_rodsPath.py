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

class testRodsPath(iRODSTestCase):

    def test_rodsPath_t(self):
        objType = UNKNOWN_OBJ_T
        #objState = UNKNOWN_ST
        rodsObjStat = rodsObjStat_t()
        tmp = create_rodsPath_t(objType, #objState, 
                                12, 12, "inPath", "outPath", 
                                "dataId", "chksum", rodsObjStat)
        self.assertEqual(tmp.objType, objType)
        #self.assertEqual(tmp.objState, objState)
        self.assertEqual(tmp.size, 12)
        self.assertEqual(tmp.objMode, 12)
        self.assertEqual(tmp.inPath, "inPath")
        self.assertEqual(tmp.outPath, "outPath")
        self.assertEqual(tmp.dataId, "dataId")
        self.assertEqual(tmp.chksum, "chksum")
        #self.assertEqual(tmp.rodsObjStat, rodsObjStat)

    def test_rodsPathInp_t(self):
        srcPath = rodsPath_t()
        destPath = rodsPath_t()
        targPath = rodsPath_t()
        tmp = create_rodsPathInp_t(12, srcPath, destPath, targPath, 12)
        self.assertEqual(tmp.numSrc, 12)
        #self.assertEqual(tmp.srcPath, srcPath)
        #self.assertEqual(tmp.destPath, destPath)
        #self.assertEqual(tmp.targPath, targPath)
        self.assertEqual(tmp.resolved, 12)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsPath))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())