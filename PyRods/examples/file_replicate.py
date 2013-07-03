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
    resc1 = "demoResc"
    resc2 = "demoResc2"
    
    path = myEnv.rodsHome + '/testreplication.txt'
    
    # If path exists on resc2, it will modify the version on resc2 and not create
    # a new one on resc1. This is the choice of irods team.
    f = irodsOpen(conn, path, 'w', resc1)
    f.write("=="*15)
    f.close()
    
    print "First read, both files are equal"
    
    f = irodsOpen(conn, path, 'r', resc1)
    print "  Path:", f.getCollName(), f.getName()
    print "  Resource Name :", f.getResourceName()
    print "  Repl Number :", f.getReplNumber()
    print "  Size :", f.getSize()
    print "  Content :", f.read()
    print
    f.replicate(resc2)
    f.close()
    
    f = irodsOpen(conn, path, 'r', resc2)
    print "  Path:", f.getCollName(), f.getName()
    print "  Resource Name :", f.getResourceName()
    print "  Repl Number :", f.getReplNumber()
    print "  Size :", f.getSize()
    print "  Content :", f.read()
    print
    f.close()
    
    print "Second read, first file is modified"
    
    f = irodsOpen(conn, path, 'a', resc1)
    f.write("++"*15)
    f.close()
    
    f = irodsOpen(conn, path, 'r', resc1)
    print "  Path:", f.getCollName(), f.getName()
    print "  Resource Name :", f.getResourceName()
    print "  Repl Number :", f.getReplNumber()
    print "  Size :", f.getSize()
    print "  Content :", f.read()
    print
    f.close()
    
    f = irodsOpen(conn, path, 'r', resc2)
    print "  Path:", f.getCollName(), f.getName()
    print "  Resource Name :", f.getResourceName()
    print "  Repl Number :", f.getReplNumber()
    print "  Size :", f.getSize()
    print "  Content :", f.read()
    print
    f.close()
    
    print "Third read, synchronize the versions"
    
    f.update()
    
    f = irodsOpen(conn, path, 'r', resc1)
    print "  Path:", f.getCollName(), f.getName()
    print "  Resource Name :", f.getResourceName()
    print "  Repl Number :", f.getReplNumber()
    print "  Size :", f.getSize()
    print "  Content :", f.read()
    print
    f.close()
    
    f = irodsOpen(conn, path, 'r', resc2)
    print "  Path:", f.getCollName(), f.getName()
    print "  Resource Name :", f.getResourceName()
    print "  Repl Number :", f.getReplNumber()
    print "  Size :", f.getSize()
    print "  Content :", f.read()
    print
    f.close()
    
    print "Get the replicas"
    f = irodsOpen(conn, path, 'r', resc1)
    
    for fi in f.getReplications():
        print "  Path:", fi.getCollName(), fi.getName()
        print "  Resource Name :", fi.getResourceName()
        print "  Repl Number :", fi.getReplNumber()
        print "  Size :", fi.getSize()
        print "  Content :", fi.read()
        print
        
        fi.close()
        fi.delete()
        
    f.close()
    
    conn.disconnect()