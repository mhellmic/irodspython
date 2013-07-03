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
    
    path = myEnv.rodsHome
    
    c = irodsCollection(conn, path)
    
    # There are 2 ways to deal with metadata
    
    # 1: If you have an iRodsCollection object
    
    # Add some metadata
    c.addUserMetadata("units", "12", "cm")
    c.addUserMetadata("author", "rods")
    print c.getUserMetadata()    
    c.rmUserMetadata("author", "rods")
    c.rmUserMetadata("units", "12", "cm")
    print c.getUserMetadata()
    
    # 2: If you have the irods path of the collection
    addCollUserMetadata(conn, path, "units", "12", "cm")
    addCollUserMetadata(conn, path, "author", "rods")
    print getCollUserMetadata(conn, path)
    rmCollUserMetadata(conn, path, "author", "rods")
    rmCollUserMetadata(conn, path, "units", "12", "cm")
    print getCollUserMetadata(conn, path)
    
    conn.disconnect()