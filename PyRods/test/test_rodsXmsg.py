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

class testRodsXmsg(iRODSTestCase):

    def test_getXmsgTicketInp_t(self):
        tmp = create_getXmsgTicketInp_t(12, 12)
        self.assertEqual(tmp.expireTime, 12)
        self.assertEqual(tmp.flag, 12)

    def test_rcvXmsgInp_t(self):
        tmp = create_rcvXmsgInp_t(12, 12, 12, "msgCondition")
        self.assertEqual(tmp.rcvTicket, 12)
        self.assertEqual(tmp.msgNumber, 12)
        self.assertEqual(tmp.seqNumber, 12)
        self.assertEqual(tmp.msgCondition, "msgCondition")

    def test_rcvXmsgOut_t(self):
        tmp = create_rcvXmsgOut_t("msgType", "sendUserName", "sendAddr", 12, 12,
                                  "msg")
        self.assertEqual(tmp.msgType, "msgType")
        self.assertEqual(tmp.sendUserName, "sendUserName")
        self.assertEqual(tmp.sendAddr, "sendAddr")
        self.assertEqual(tmp.msgNumber, 12)
        self.assertEqual(tmp.seqNumber, 12)
        self.assertEqual(tmp.msg, "msg")

    def test_xmsgTicketInfo_t(self):
        tmp = create_xmsgTicketInfo_t(12, 12, 12, 12)
        self.assertEqual(tmp.sendTicket, 12)
        self.assertEqual(tmp.rcvTicket, 12)
        self.assertEqual(tmp.expireTime, 12)
        self.assertEqual(tmp.flag, 12)

    def test_sendXmsgInp_t(self):
        ticket = xmsgTicketInfo_t()
        #sendXmsgInfo = sendXmsgInfo_t
        tmp = create_sendXmsgInp_t(ticket, "sendAddr", #sendXmsgInfo
                                   )
        #self.assertEqual(tmp.ticket, ticket)
        self.assertEqual(tmp.sendAddr, "sendAddr")
        #self.assertEqual(tmp.sendXmsgInfo, sendXmsgInfo)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsXmsg))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())