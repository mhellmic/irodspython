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

class testParseCommandLine(iRODSTestCase):

    def test_rodsArguments_t(self):
        tmp = create_rodsArguments_t(12, 12, 12, 12, 12, 12, 12, 12, 12, 
                                     "attrStr", 12, 12, 12, "conditionString", 
                                     12, "collectionString", 12, 12, 12, 12, 
                                     12, 12, 12, "fileString", 12, 
                                     "rescGroupString", 12, 12, 12, 
                                     "hostAddrString", 12, 12, 12, 12, 12, 
                                     "dataTypeString", 12, 12, 12, 12, 12, 12, 
                                     "mountType", 12, "replNumValue", 12, 12, 
                                     12, 12, "physicalPathString", 12, 
                                     "logicalPathString", 12, 12, 
                                     "optionString", 12, 12, 12, 12, 12, 
                                     "queryStr", 12, 12, 12, 12, 
                                     "resourceString", 12, 12, 12, 12, 
                                     "srcRescString", 12, 12, "subsetStr", 12, 
                                     12, "ticketString", 12, 12, "userString", 
                                     12, 12, 12, 12, "zoneName", 12, 12, 
                                     "varStr", 12, 12, "restartFileString", 12, 
                                     "lfrestartFileString", 12, 12, 12, 12, 12, 
                                     "excludeFileString", 12, 12, 12, 12, 12, 12)
        self.assertEqual(tmp.add, 12)
        self.assertEqual(tmp.age, 12)
        self.assertEqual(tmp.agevalue, 12)
        self.assertEqual(tmp.all, 12)
        self.assertEqual(tmp.accessControl, 12)
        self.assertEqual(tmp.admin, 12)
        self.assertEqual(tmp.ascitime, 12)
        self.assertEqual(tmp.attr, 12)
        self.assertEqual(tmp.noattr, 12)
        self.assertEqual(tmp.attrStr, "attrStr")
        self.assertEqual(tmp.bulk, 12)
        self.assertEqual(tmp.backupMode , 12)
        self.assertEqual(tmp.condition, 12)
        self.assertEqual(tmp.conditionString, "conditionString")
        self.assertEqual(tmp.collection, 12)
        self.assertEqual(tmp.collectionString, "collectionString")
        self.assertEqual(tmp.dataObjects, 12)
        self.assertEqual(tmp.dim, 12)
        self.assertEqual(tmp.dryrun, 12)
        self.assertEqual(tmp.echo, 12)
        self.assertEqual(tmp.empty, 12)
        self.assertEqual(tmp.force, 12)
        self.assertEqual(tmp.file, 12)
        self.assertEqual(tmp.fileString, "fileString")
        self.assertEqual(tmp.rescGroup, 12)
        self.assertEqual(tmp.rescGroupString, "rescGroupString")
        self.assertEqual(tmp.header, 12)
        self.assertEqual(tmp.help, 12)
        self.assertEqual(tmp.hostAddr, 12)
        self.assertEqual(tmp.hostAddrString, "hostAddrString")
        self.assertEqual(tmp.input, 12)
        self.assertEqual(tmp.redirectConn, 12)
        self.assertEqual(tmp.checksum, 12)
        self.assertEqual(tmp.verifyChecksum, 12)
        self.assertEqual(tmp.dataType, 12)
        self.assertEqual(tmp.dataTypeString , "dataTypeString")
        self.assertEqual(tmp.longOption, 12)
        self.assertEqual(tmp.link, 12)
        self.assertEqual(tmp.rlock, 12)
        self.assertEqual(tmp.wlock, 12)
        self.assertEqual(tmp.veryLongOption, 12)
        self.assertEqual(tmp.mountCollection, 12)
        self.assertEqual(tmp.mountType , "mountType")
        self.assertEqual(tmp.replNum, 12)
        self.assertEqual(tmp.replNumValue, "replNumValue")
        self.assertEqual(tmp.noPage, 12)
        self.assertEqual(tmp.number, 12)
        self.assertEqual(tmp.numberValue, 12)
        self.assertEqual(tmp.physicalPath, 12)
        self.assertEqual(tmp.physicalPathString, "physicalPathString")
        self.assertEqual(tmp.logicalPath, 12)
        self.assertEqual(tmp.logicalPathString, "logicalPathString")
        self.assertEqual(tmp.progressFlag, 12)
        self.assertEqual(tmp.option, 12)
        self.assertEqual(tmp.optionString, "optionString")
        self.assertEqual(tmp.orphan, 12)
        self.assertEqual(tmp.purgeCache, 12)
        self.assertEqual(tmp.bundle, 12)
        self.assertEqual(tmp.prompt, 12)
        self.assertEqual(tmp.query, 12)
        self.assertEqual(tmp.queryStr, "queryStr")
        self.assertEqual(tmp.rbudp, 12)
        self.assertEqual(tmp.reg, 12)
        self.assertEqual(tmp.recursive, 12)
        self.assertEqual(tmp.resource, 12)
        self.assertEqual(tmp.resourceString, "resourceString")
        self.assertEqual(tmp.remove, 12)
        self.assertEqual(tmp.sizeFlag, 12)
        self.assertEqual(tmp.size, 12)
        self.assertEqual(tmp.srcResc, 12)
        self.assertEqual(tmp.srcRescString, "srcRescString")
        self.assertEqual(tmp.subset, 12)
        self.assertEqual(tmp.intsubsetByVal, 12)
        self.assertEqual(tmp.subsetStr, "subsetStr")
        self.assertEqual(tmp.test, 12)
        self.assertEqual(tmp.ticket, 12)
        self.assertEqual(tmp.ticketString, "ticketString")
        self.assertEqual(tmp.reconnect, 12)
        self.assertEqual(tmp.user, 12)
        self.assertEqual(tmp.userString, "userString")
        self.assertEqual(tmp.unmount, 12)
        self.assertEqual(tmp.verbose, 12)
        self.assertEqual(tmp.veryVerbose, 12)
        self.assertEqual(tmp.zone, 12)
        self.assertEqual(tmp.zoneName, "zoneName")
        self.assertEqual(tmp.verify, 12)
        self.assertEqual(tmp.var, 12)
        self.assertEqual(tmp.varStr, "varStr")
        self.assertEqual(tmp.extract , 12)
        self.assertEqual(tmp.restart, 12)
        self.assertEqual(tmp.restartFileString, "restartFileString")
        self.assertEqual(tmp.lfrestart, 12)
        self.assertEqual(tmp.lfrestartFileString, "lfrestartFileString")
        self.assertEqual(tmp.version, 12)
        self.assertEqual(tmp.retries, 12)
        self.assertEqual(tmp.retriesValue, 12)
        self.assertEqual(tmp.regRepl, 12)
        self.assertEqual(tmp.excludeFile, 12)
        self.assertEqual(tmp.excludeFileString, "excludeFileString")
        self.assertEqual(tmp.parallel, 12)
        self.assertEqual(tmp.serial, 12)
        self.assertEqual(tmp.masterIcat, 12)
        self.assertEqual(tmp.silent, 12)
        self.assertEqual(tmp.sql, 12)
        self.assertEqual(tmp.optind, 12)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testParseCommandLine))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())