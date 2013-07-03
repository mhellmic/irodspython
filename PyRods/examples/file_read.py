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
    
    path = myEnv.rodsHome + '/testsimpleio.txt'
    
    # Write a string in a file
    f = irodsOpen(conn, path, 'w')
    f.write("This is a test")
    f.close()
    
    # Read the file
    f = irodsOpen(conn, path, 'r')
    print f.read()
    f.close()
    
    # Read the file (give the buffer size)
    f = irodsOpen(conn, path, 'r')
    print f.read(5)
    print f.read()
    f.close()
    
    # Append to the file
    f = irodsOpen(conn, path, 'a')
    f.write("\nThis is still the test")
    f.close()
    
    # Read the file again
    f = irodsOpen(conn, path, 'r')
    print f.read()
    f.close()
    
    f.delete()
    
    conn.disconnect()