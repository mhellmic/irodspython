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

class testRodsQuery(iRODSTestCase):

    def test_generalUpdateInp_t(self):
        values = inxValPair_t()
        tmp = create_generalUpdateInp_t(12, values)
        self.assertEqual(tmp.type, 12)
        #self.assertEqual(tmp.values, values)

    def test_genQueryInp_t(self):
        condInput = keyValPair_t()
        selectInp = inxIvalPair_t()
        sqlCondInp = inxValPair_t()
        tmp = create_genQueryInp_t(12, 12, 12, 12, condInput, selectInp, 
                                   sqlCondInp)
        self.assertEqual(tmp.maxRows, 12)
        self.assertEqual(tmp.continueInx, 12)
        self.assertEqual(tmp.rowOffset, 12)
        self.assertEqual(tmp.options, 12)
        #self.assertEqual(tmp.condInput, condInput)
        #self.assertEqual(tmp.selectInp, selectInp)
        #self.assertEqual(tmp.sqlCondInp, sqlCondInp)

    def test_genQueryOut_t(self):
        sqlResult = sqlResult_t()
        tmp = create_genQueryOut_t(12, 12, 12, 12, sqlResult)
        self.assertEqual(tmp.rowCnt, 12)
        self.assertEqual(tmp.attriCnt, 12)
        self.assertEqual(tmp.continueInx, 12)
        self.assertEqual(tmp.totalRowCount, 12)
        #self.assertEqual(tmp.sqlResult, sqlResult)

    def test_simpleQueryInp_t(self):
        tmp = create_simpleQueryInp_t("sql", "arg1", "arg2", "arg3", "arg4", 
                                      12, 12, 12)
        self.assertEqual(tmp.sql, "sql")
        self.assertEqual(tmp.arg1, "arg1")
        self.assertEqual(tmp.arg2, "arg2")
        self.assertEqual(tmp.arg3, "arg3")
        self.assertEqual(tmp.arg4, "arg4")
        self.assertEqual(tmp.control, 12)
        self.assertEqual(tmp.form, 12)
        self.assertEqual(tmp.maxBufSize, 12)

    def test_simpleQueryOut_t(self):
        tmp = create_simpleQueryOut_t(12, "outBuf")
        self.assertEqual(tmp.control, 12)
        self.assertEqual(tmp.outBuf, "outBuf")

    def test_sqlResult_t(self):
        tmp = create_sqlResult_t(12, 12, "value")
        self.assertEqual(tmp.attriInx, 12)
        self.assertEqual(tmp.len, 12)
        self.assertEqual(tmp.value, "value")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsQuery))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())