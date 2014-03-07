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
    
    path1 = myEnv.rodsHome + '/testcopy.txt'
    tmp_coll = myEnv.rodsHome + "/testCopy"
    status = createCollection(conn, tmp_coll)
    path2 = tmp_coll + "/testcopy2.txt"
    
    f = irodsOpen(conn, path1, 'w')
    f.write("Test Copy")
    f.close()
    
    f = irodsOpen(conn, path1, 'r')
    print "Content before copy:", f.read()
    print
    f.close()
    
    #status = f.copy(path2, force=True)
    status = irodsCopy(conn, path1, path2, force=True, resc="demoResc")
    print status
    
    f = irodsOpen(conn, path2, 'r')
    print "Content after copy:", f.read()
    print
    f.close()
    
    status = deleteCollection(conn, tmp_coll)
    status = deleteFile(conn, path1)
    conn.disconnect()