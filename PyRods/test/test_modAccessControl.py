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

class testModAccessControl(iRODSTestCase):

    def test_modAccessControlInp_t(self):
        tmp = create_modAccessControlInp_t(12, "accessLevel", "userName", 
                                           "zone", "path")
        self.assertEqual(tmp.recursiveFlag, 12)
        self.assertEqual(tmp.accessLevel, "accessLevel")
        self.assertEqual(tmp.userName, "userName")
        self.assertEqual(tmp.zone, "zone")
        self.assertEqual(tmp.path, "path")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testModAccessControl))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())