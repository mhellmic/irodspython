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
    
    rescName = "demoResc"
    
    resc = getResource(conn, rescName)
    
    # Get some information
    print "Id:", resc.getId()
    print "Name:", resc.getName()
    print "Zone:", resc.getZone()
    print "Type:", resc.getTypeName()
    print "Class:", resc.getClassName()
    print "Host:", resc.getHost()
    print "Path:", resc.getPath()
    print "Free Space:", resc.getFreeSpace()
    print "Free Space TS:", resc.getFreeSpaceTs()
    print "Info:", resc.getInfo()
    print "Comment:", resc.getComment()
    print "Create TS:", resc.getCreateTs()
    print "Modify TS:", resc.getModifyTs()
        
    # Modify some fields
    #resc.setTypeName("unix file system")
    #resc.setClassName("archive")
    #resc.setHost("localhost.localdomain")
    #resc.setPath("/home/rods/build/iRODS/Vault")
    resc.setComment("Useful comment")
    resc.setInfo("Useful info")
    resc.setFreeSpace("free comment")  
    
    conn.disconnect()