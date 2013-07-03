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
        
    # Get an iRodsGroup with its name
    group = getGroup(conn, "public")
    
    # Get the fields
    print "Id:", group.getId()
    print "Name:", group.getName()
    print "Type:", group.getTypeName()
    print "Zone:", group.getZone()
    print "Info:", group.getInfo()
    print "Comment:", group.getComment()
    print "Create TS:", group.getCreateTs()
    print "Modify TS:", group.getModifyTs()
    
    # You can modify some of the fields with an admin account
    #group.setComment("Useful Comment")
    #group.setDN("long description of the group")
    #group.setInfo("Useful info")
    
    # You can get the members of a group. You obtain iRodsUser instances
    print
    print "Members of the group:"
    for user in group.getMembers():
        print "Id:", user.getId()
        print "Name:", user.getName()
        print "Zone:", user.getZone()
        print
      
    conn.disconnect()