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

class testRcConnect(iRODSTestCase):

    def test_rcComm_t(self):
        proxyUser = userInfo_t()
        clientUser = userInfo_t()
        svrVersion = version_t()
        tmp = create_rcComm_t("host", 12, 12, 12, proxyUser, clientUser, 
                              svrVersion, 12, 12, 12, 12, 12)
        self.assertEqual(tmp.host, "host")
        self.assertEqual(tmp.sock, 12)
        self.assertEqual(tmp.portNum, 12)
        self.assertEqual(tmp.loggedIn, 12)
        #self.assertEqual(tmp.proxyUser, proxyUser)
        #self.assertEqual(tmp.clientUser, clientUser)
        #self.assertEqual(tmp.svrVersion, svrVersion)
        self.assertEqual(tmp.flag, 12)
        self.assertEqual(tmp.apiInx, 12)
        self.assertEqual(tmp.status, 12)
        self.assertEqual(tmp.windowSize, 12)
        self.assertEqual(tmp.reconnectedSock, 12)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRcConnect))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())