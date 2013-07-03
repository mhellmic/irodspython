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
    
    # Get a list of metadatas, a metadata is a tuple (name, value, units)
    print resc.getUserMetadata()
    
    # Add some metadatas, the unit field is optional
    resc.addUserMetadata("test1", "value1")
    resc.addUserMetadata("test2", "value2", "units")
    
    print resc.getUserMetadata()
        
    # Remove the metadatas we added
    resc.rmUserMetadata("test1", "value1")
    resc.rmUserMetadata("test2", "value2", "units")
        
    print resc.getUserMetadata()
    
    conn.disconnect()