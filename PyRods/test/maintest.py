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
from irods import *
from test_auth import *
from test_chkObjPermAndStat import *
from test_dataObj import *
from test_getRodsEnv import *
from test_MD5 import *
from test_miscUtil import *
from test_modAccessControl import *
from test_msParam import *
from test_obf import *
from test_parseCommandLine import *
from test_rcConnect import *
from test_rcMisc import *
from test_rodsAdmin import *
from test_rodsDef import *
from test_rodsError import *
from test_rodsExec import *
from test_rodsFile import *
from test_rodsInfo import *
from test_rodsIO import *
from test_rodsLog import *
from test_rodsMeta import *
from test_rodsPath import *
from test_rodsQuery import *
from test_rodsStructFile import *
from test_rodsUser import *
from test_rodsXmsg import *
from test_SqlMisc import *
from test_StringOpr import *


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testAuth))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testChkObjPermAndStat))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testDataObj))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testGetRodsEnv))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testMd5))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testMiscUtil))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testModAccessControl))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testMsParam))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testParseCommandLine))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRcConnect))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRcMisc))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsAdmin))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsDef))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsError))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsExec))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsFile))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsInfo))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsIO))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsLog))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsMeta))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsPath))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsQuery))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsStructFile))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsUser))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsXmsg))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testStringOpr))
    
    
    return suite



if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())