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


class testAuth(iRODSTestCase):

    def test_authCheckInp_t(self):
        tmp = create_authCheckInp_t("challenge", "response", "username")
        self.assertEqual(tmp.challenge, "challenge")
        self.assertEqual(tmp.response, "response")
        self.assertEqual(tmp.username, "username")

    def test_authCheckOut_t(self):
        tmp = create_authCheckOut_t(12, 12, "serverResponse")
        self.assertEqual(tmp.clientPrivLevel, 12)
        self.assertEqual(tmp.privLevel, 12)
        self.assertEqual(tmp.serverResponse, "serverResponse")

    def test_authResponseInp_t(self):
        tmp = create_authResponseInp_t("response", "username")
        self.assertEqual(tmp.response, "response")
        self.assertEqual(tmp.username, "username")
        
    def test_authRequestOut_t(self):
        tmp = create_authRequestOut_t("challenge")
        self.assertEqual(tmp.challenge, "challenge")

    def test_gsiAuthRequestOut_t(self):
        tmp = create_gsiAuthRequestOut_t("serverDN")
        self.assertEqual(tmp.serverDN, "serverDN")
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testAuth))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())