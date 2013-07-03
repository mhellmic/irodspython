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
    
    path = myEnv.rodsHome + '/testmeta.txt'
 
    f = irodsOpen(conn, path, 'w')
    
    # There's 2 way to deal with metadata
    
    # 1: If you have an iRodsFile object
    
    f.addUserMetadata("units", "12", "cm")
    f.addUserMetadata("author", "rods")
    print f.getUserMetadata()
    f.rmUserMetadata("author", "rods")
    f.rmUserMetadata("units", "12", "cm")
    print f.getUserMetadata()        
        
    # 2: If you have the irods path of the file
    addFileUserMetadata(conn, path, "units", "12", "cm")
    addFileUserMetadata(conn, path, "author", "rods")
    print getFileUserMetadata(conn, path)
    rmFileUserMetadata(conn, path, "author", "rods") 
    rmFileUserMetadata(conn, path, "units", "12", "cm")
    print getFileUserMetadata(conn, path)     
       
    f.close()
    f.delete()
    
    conn.disconnect()