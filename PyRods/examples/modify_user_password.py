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

USER = "testModify"
PW = "1Password"

if __name__ == "__main__":
    status, myEnv = getRodsEnv()
    # This have to be a user in the rodsadmin group
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
    status = clientLogin(conn)
        
    # Create a user with the name and the group
    user = createUser(conn, USER, "rodsuser")
    delete_user_after = True
    if not user:
        delete_user_after = False # If the user exists we won't delete it
        user = getUser(conn, USER)
    
    #print setPassword(conn, user.getName(), PW)
    print "status for modification: ", user.setPassword(PW)
    
    conn.disconnect()
    
    # Test connection for our modified user
    conn, errMsg = rcConnect("localhost", 1247, USER, "tempZone")
    status = clientLoginWithPassword(conn, PW)
    print "Status for the connection with our modified user %s: %d" % (USER, status)
    conn.disconnect()
    
    if delete_user_after:
        conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
        status = clientLogin(conn)
        deleteUser(conn, USER)
        conn.disconnect()
        