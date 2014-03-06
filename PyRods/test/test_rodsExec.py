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

class testRodsExec(iRODSTestCase):

    def test_execCmd_t(self):
        condInput = keyValPair_t()
        tmp = create_execCmd_t("cmd", "cmdArgv", "execAddr", "hintPath", 12, 
                               12, condInput)
        self.assertEqual(tmp.cmd, "cmd")
        self.assertEqual(tmp.cmdArgv, "cmdArgv")
        self.assertEqual(tmp.execAddr, "execAddr")
        self.assertEqual(tmp.hintPath, "hintPath")
        self.assertEqual(tmp.addPathToArgv, 12)
        self.assertEqual(tmp.dummy, 12)
        #self.assertEqual(tmp.condInput, condInput)

    def test_execCmdOut_t(self):
        tmp = create_execCmdOut_t("stdoutBuf", "stderrBuf", 12)
        #self.assertEqual(tmp.stdoutBuf.getBuf(), "stdoutBuf")
        #self.assertEqual(tmp.stderrBuf.getBuf(), "stderrBuf")
        self.assertEqual(tmp.status, 12)

    def test_execMyRuleInp_t(self):
        addr = rodsHostAddr_t()
        condInput = keyValPair_t()
        inpParamArray = msParamArray_t()
        tmp = create_execMyRuleInp_t("myRule", addr, condInput, "outParamDesc", 
                                     inpParamArray)
        self.assertEqual(tmp.myRule, "myRule")
        #self.assertEqual(tmp.addr, addr)
        #self.assertEqual(tmp.condInput, condInput)
        self.assertEqual(tmp.outParamDesc, "outParamDesc")
        #self.assertEqual(tmp.inpParamArray, inpParamArray)

    def test_ruleExecDelInp_t(self):
        tmp = create_ruleExecDelInp_t("ruleExecId")
        self.assertEqual(tmp.ruleExecId, "ruleExecId")

    def test_ruleExecModInp_t(self):
        condInput = keyValPair_t()
        tmp = create_ruleExecModInp_t("ruleId", condInput)
        self.assertEqual(tmp.ruleId, "ruleId")
        #self.assertEqual(tmp.condInput, "condInput")

    def test_ruleExecSubmitInp_t(self):
        condInput = keyValPair_t()
        packedReiAndArgBBuf = bytesBuf_t()
        tmp = create_ruleExecSubmitInp_t("ruleName", "reiFilePath", "userName", 
                                         "exeAddress", "exeTime", "exeFrequency", 
                                         "priority", "lastExecTime", "exeStatus", 
                                         "estimateExeTime", "notificationAddr", 
                                         condInput, packedReiAndArgBBuf, 
                                         "ruleExecId")
        self.assertEqual(tmp.ruleName, "ruleName")
        self.assertEqual(tmp.reiFilePath, "reiFilePath")
        self.assertEqual(tmp.userName, "userName")
        self.assertEqual(tmp.exeAddress, "exeAddress")
        self.assertEqual(tmp.exeTime, "exeTime")
        self.assertEqual(tmp.exeFrequency, "exeFrequency")
        self.assertEqual(tmp.priority, "priority")
        self.assertEqual(tmp.lastExecTime, "lastExecTime")
        self.assertEqual(tmp.exeStatus, "exeStatus")
        self.assertEqual(tmp.estimateExeTime, "estimateExeTime")
        self.assertEqual(tmp.notificationAddr, "notificationAddr")
        #self.assertEqual(tmp.condInput, condInput)
        #self.assertEqual(tmp.packedReiAndArgBBuf, packedReiAndArgBBuf)
        self.assertEqual(tmp.ruleExecId, "ruleExecId")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsExec))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())