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

class testChkObjPermAndStat(iRODSTestCase):

    def test_chkObjPermAndStat_t(self):
        condInput = keyValPair_t()
        tmp = create_chkObjPermAndStat_t("objPath", "permission", 12, 12, 
                                         condInput)
        self.assertEqual(tmp.objPath, "objPath")
        self.assertEqual(tmp.permission, "permission")
        self.assertEqual(tmp.flags, 12)
        self.assertEqual(tmp.status, 12)
        #self.assertEqual(tmp.condInput, condInput)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testChkObjPermAndStat))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())