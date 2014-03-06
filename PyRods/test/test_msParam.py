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

class testMsParam(iRODSTestCase):

    def test_msParam_t(self):
        inpOutBuf = bytesBuf_t()
        tmp = create_msParam_t("label", "type", #"inOutStruct", 
                               inpOutBuf)
        
        self.assertEqual(tmp.label, "label")
        self.assertEqual(tmp.type, "type")
        #self.assertEqual(tmp.inOutStruct, "inOutStruct")
        #self.assertEqual(tmp.inpOutBuf, inpOutBuf)
        

    def test_msParamArray_t(self):
        tmp = create_msParamArray_t(12, 12)# msParam)
        self.assertEqual(tmp.len, 12)
        self.assertEqual(tmp.oprType, 12)
        #self.assertEqual(tmp.msParam, msParam)

    def test_msParam_t_unicode(self):
        inpOutBuf = bytesBuf_t()
        tmp = create_msParam_t(u"label", u"type", #"inOutStruct", 
                               inpOutBuf)
        
        self.assertEqual(tmp.label, u"label")
        self.assertEqual(tmp.type, u"type")
        #self.assertEqual(tmp.inOutStruct, "inOutStruct")
        #self.assertEqual(tmp.inpOutBuf, inpOutBuf)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testMsParam))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())