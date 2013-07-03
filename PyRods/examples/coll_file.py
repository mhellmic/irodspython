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

from irods import *

if __name__ == "__main__":
    status, myEnv = getRodsEnv()
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
    status = clientLogin(conn)
    
    # These 2 resources have to exist
    collName = "testCollection"
    resc1 = "demoResc"
    resc2 = "demoResc2"
    
    # Open the current working directory
    c = irodsCollection(conn)
    
    print c.getCollName()
    
    c.createCollection("subCollection")
    c.openCollection("subCollection")
    
    print c.getCollName()
    
    f = c.create("testCollection.txt")
    nb_bytes_written = f.write("This is a test")
    f.close()
    # REPLICATE THE FILE AFTER CLOSING IT (BECAUSE MODE IS 'w')
    f.replicate(resc2)    
    
    f = c.create("testCollection2.txt", resc2)
    nb_bytes_written = f.write("This is another test")
    f.close()
    
    print "Number of data objects :", c.getLenObjects()
    
    print c.getObjects()
    
    for dataObj in c.getObjects():
        data_name = dataObj[0]
        resc_name = dataObj[1]
        
        print data_name, resc_name
        
        f = c.open(data_name, "r", resc_name)
        
        print "  Path:", f.getCollName(), f.getName()
        print "  Resource Name :", f.getResourceName()
        print "  Repl Number :", f.getReplNumber()
        print "  Size :", f.getSize()
        print "  Content :", f.read()
        print 
        
        c.delete(data_name, resc_name)
        
        
    c.upCollection()
    
    print c.getCollName()
    print "Number of subcollections :", c.getLenSubCollections()
    print "  ", c.getSubCollections()
    
    
    print "After deletion"
    c.deleteCollection("subCollection")
    print "Number of subcollections :", c.getLenSubCollections()
    print "  ", c.getSubCollections()
    
    c.upCollection()
    c.deleteCollection(collName)
    
    conn.disconnect()