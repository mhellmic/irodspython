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
import os
from common import *
from irods import *

class testRodsIO(iRODSTestCase):

    def test_regReplica_t(self):
        srcDataObjInfo = dataObjInfo_t()
        destDataObjInfo = dataObjInfo_t()
        condInput = keyValPair_t()
        tmp = create_regReplica_t(srcDataObjInfo, destDataObjInfo, condInput)
        #self.assertEqual(tmp.srcDataObjInfo, srcDataObjInfo)
        #self.assertEqual(tmp.destDataObjInfo, destDataObjInfo)
        #self.assertEqual(tmp.condInput, condInput)

    def test_unregDataObj_t(self):
        dataObjInfo = dataObjInfo_t()
        condInput = keyValPair_t()
        tmp = create_unregDataObj_t(dataObjInfo, condInput)
        #self.assertEqual(tmp.dataObjInfo, dataObjInfo)
        #self.assertEqual(tmp.condInput, condInput)
        
    def testIrodsFileMeta1(self):
        path = self.myEnv.rodsHome + '/testmeta.txt'
        f = irodsOpen(self.conn, path, 'w')
        self.assertEqual(path, f.collName + '/' + f.dataName)
       
        f.addUserMetadata("test1", "value1")
        f.addUserMetadata("test2", "value2", "units")
        
        md = f.getUserMetadata()
        self.assertTrue(("test1", "value1", "") in md)
        self.assertTrue(("test2", "value2", "units") in md)
        
        f.rmUserMetadata("test1", "value1")
        f.rmUserMetadata("test2", "value2", "units")
        f.close()
        f.delete()
        
    def testIrodsFileRWA(self):
        # Read/Write/Append
        path = self.myEnv.rodsHome + '/testsimpleio.txt'
        f = irodsOpen(self.conn, path, 'w')
        f.write("This is a test")
        f.close()
        
        f = irodsOpen(self.conn, path, 'r')
        self.assertEqual(f.read(), "This is a test")
        f.close()
        
        f = irodsOpen(self.conn, path, 'r')
        self.assertEqual(f.read(5), "This is a test"[:5])
        f.close()
        
        f = irodsOpen(self.conn, path, 'a')
        f.write("\nThis is still the test")
        f.close()
    
        f = irodsOpen(self.conn, path, 'r')
        self.assertEqual(f.read(), "This is a test" + "\nThis is still the test")
        f.close()
        
        f.delete()
        
    def testIrodsFileSeek(self):
        path = self.myEnv.rodsHome + '/testseekio.txt'
        
        f = irodsOpen(self.conn, path, 'w')
        f.write("-" * 100)
        f.close()
        
        f = irodsOpen(self.conn, path, 'r')
        self.assertEqual(f.getSize(), 100)
        f.seek(50, os.SEEK_SET) # middle
        self.assertEqual(f.read(), "-" * 50)
        f.read()
            
        f.seek(0) # begining   
        self.assertEqual(f.read(), "-" * 100) 
        f.seek(f.getSize(), os.SEEK_END) # begining (from the end)
        self.assertEqual(f.read(), "-" * 100) 
        f.close()
        
        f = irodsOpen(self.conn, path, 'a')
        f.seek(-60, os.SEEK_CUR) # middle
        self.assertEqual(f.getPosition(), 40)
        f.write("+" * 20)        
        self.assertEqual(f.getPosition(), 60)       
        f.close()   
        
        f = irodsOpen(self.conn, path, 'r')
        self.assertEqual(f.read(), "-" * 40 + "+" * 20 + "-" * 40)
        f.close()
        
        f.delete()
        
    def testIrodsFileInfos(self):
        path = self.myEnv.rodsHome + '/testinfoio.txt'
        
        f = irodsOpen(self.conn, path, 'w')
        f.write("+" * 25)
        
        self.assertEqual(f.collName, self.myEnv.rodsHome)
        self.assertEqual(f.dataName, 'testinfoio.txt')
        ldesc = f.getDescInx()
        self.assertEqual(f.position, 25)
        rpl_num = f.getReplNumber()
        rsc = f.getResourceName()
        sz = f.getSize()  # size = 0 because size is updated when you close the file
        
        f.close()
    
        f.delete()
        
    def testIrodsFileReplication(self):
        
        # Only works if at least 2 resources, demoResc and demoResc2
        
        resc_names = [ resc.name for resc in getResources(self.conn) ]
        
        if "demoResc" in resc_names and "demoResc2" in resc_names:
            resc1 = "demoResc"
            resc2 = "demoResc2"
            path = self.myEnv.rodsHome + '/testreplication.txt'
                        
            # If path exists on resc2, it will modify the version on resc2 and not create
            # a new one on resc1. This is the choice of irods team.
            f = irodsOpen(self.conn, path, 'w', resc1)
            f.write("=="*15)
            f.close()
            
            # First read, both files are equal
            
            f = irodsOpen(self.conn, path, 'r', resc1)
            pth1 = f.collName + '/' + f.dataName
            self.assertEqual(resc1, f.resourceName)
            rpl1 = f.getReplNumber()
            sz1 = f.getSize()
            s1 = f.read()
            f.replicate(resc2)
            f.close()
            
            f = irodsOpen(self.conn, path, 'r', resc2)
            self.assertEqual(pth1, f.collName + '/' + f.dataName)
            self.assertEqual(resc2, f.getResourceName())
            self.assertNotEqual(rpl1, f.getReplNumber())
            self.assertEqual(sz1, f.getSize())
            self.assertEqual(s1, f.read())
            f.close()
            
            
            # Second read, first file is modified
            
            f = irodsOpen(self.conn, path, 'a', resc1)
            f.write("++"*15)
            f.close()
            
            f = irodsOpen(self.conn, path, 'r', resc1)
            s1 = f.read()
            f.close()
            
            f = irodsOpen(self.conn, path, 'r', resc2)
            self.assertNotEqual(s1, f.read())
            f.close()
            
            # Third read, synchronize the versions
            
            f.update()
            
            f = irodsOpen(self.conn, path, 'r', resc1)
            s1 = f.read()
            f.close()
            
            f = irodsOpen(self.conn, path, 'r', resc2)
            self.assertEqual(s1, f.read())
            f.close()
            
           
            # Get the replicas
            f = irodsOpen(self.conn, path, 'r', resc1)
           
            for fi in f.getReplications():
                self.assertEqual(path, f.collName + '/' + f.dataName)
                self.assertTrue(fi.getResourceName() in [resc1, resc2])
                fi.close()
                fi.delete()
                
            f.close()
            
    def testIrodsCollectionMeta(self):
        path = self.myEnv.rodsHome
        
        c = irodsCollection(self.conn, path)
        
        # 1st version
        
        c.addUserMetadata("test1", "value1")
        c.addUserMetadata("test2", "value2", "units")
        
        md = c.getUserMetadata()
        self.assertTrue(("test1", "value1", "") in md)
        self.assertTrue(("test2", "value2", "units") in md)
        
        c.rmUserMetadata("test1", "value1")
        c.rmUserMetadata("test2", "value2", "units")
        
    def testIrodsCollection(self):
        # Only works if at least 2 resources
        
        resc_names = [ resc.getName() for resc in getResources(self.conn) ]
        
        if "demoResc" in resc_names and "demoResc2" in resc_names:
            path = self.myEnv.rodsHome
            
            resc1 = "demoResc"
            resc2 = "demoResc2"
            
            # Open the current working directory
            c = irodsCollection(self.conn, path)
            
            self.assertEqual(self.myEnv.rodsHome, c.getCollName())
             
            nb = c.getLenSubCollections() # useful at the end
        
            c.createCollection("subCollection")
            c.openCollection("subCollection")
            
            self.assertEqual(path + "/subCollection", c.getCollName())
            
            f = c.create("testCollection.txt")
            nb_bytes_written = f.write("This is a test")
            f.close()
            # REPLICATE THE FILE AFTER CLOSING IT (BECAUSE MODE IS 'w')
            f.replicate(resc2)
        
            f = c.create("testCollection2.txt", resc2)
            nb_bytes_written = f.write("This is another test")
            f.close()
            
            self.assertEqual(3, c.getLenObjects()) # 2 files replicated and 1
            
            for dataObj in c.getObjects():
                data_name = dataObj[0]
                resc_name = dataObj[1]
                
                f = c.open(data_name, "r", resc_name)
                c.delete(data_name, resc_name)
                
                
            c.upCollection()
            
            self.assertEqual(self.myEnv.rodsHome, c.getCollName())
            self.assertEqual(nb + 1, c.getLenSubCollections())
            self.assertEqual(nb + 1, len(c.getSubCollections()))
            
            # After deletion
            c.deleteCollection("subCollection")
            self.assertEqual(nb, c.getLenSubCollections())



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(testRodsIO))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())