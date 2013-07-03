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
        
    # Get the information present in the iCAT
    print getUserInfo(conn, myEnv.rodsUserName)
    #print getUserInfo(conn, myEnv.rodsUserName, myEnv.rodsZone)
    
    # Get an irodsUser object, the zone is optional
    user = getUser(conn, myEnv.rodsUserName)
    #user = getUser(conn, myEnv.rodsUserName, myEnv.rodsZone)
         
    print "Id:", user.getId()
    print "Name:", user.getName()
    print "Type:", user.getTypeName()
    print "Zone:", user.getZone()
    print "Info:", user.getInfo()
    print "Comment:", user.getComment()
    print "Create TS:", user.getCreateTs()
    print "Modify TS:", user.getModifyTs()
    
    # You can modify some of the fields if you are admin
    #user.setComment("Useful Comment")
    #user.setInfo("Useful info")
    
    # Be careful if you remove your user from rodsadmin you will have trouble to put it back
    #user.setTypeName("rodsuser")
    # Be careful with this one as changing the zone will change the authentication
    #user.setZone("newZone")
    
    # You can get the groups the user belongs to. You obtain irodsGroup instances
    print "Member of :"
    for g in user.getGroups():
        print "  -", g.getName()
      
    conn.disconnect()