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

class testRodsMeta(iRODSTestCase):

    def test_modDataObjMeta_t(self):
        dataObjInfo = dataObjInfo_t()
        regParam = keyValPair_t()
        tmp = create_modDataObjMeta_t(dataObjInfo, regParam)
        #self.assertEqual(tmp.dataObjInfo, dataObjInfo)
        #self.assertEqual(tmp.regParam, regParam)

    def test_modAVUMetadataInp_t(self):
        dataObjInfo = dataObjInfo_t()
        regParam = keyValPair_t()
        tmp = create_modAVUMetadataInp_t("arg0", "arg1", "arg2", "arg3", "arg4", 
                                         "arg5", "arg6", "arg7", "arg8", "arg9")
        self.assertEqual(tmp.arg0, "arg0")
        self.assertEqual(tmp.arg1, "arg1")
        self.assertEqual(tmp.arg2, "arg2")
        self.assertEqual(tmp.arg3, "arg3")
        self.assertEqual(tmp.arg4, "arg4")
        self.assertEqual(tmp.arg5, "arg5")
        self.assertEqual(tmp.arg6, "arg6")
        self.assertEqual(tmp.arg7, "arg7")
        self.assertEqual(tmp.arg8, "arg8")
        self.assertEqual(tmp.arg9, "arg9")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsMeta))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())