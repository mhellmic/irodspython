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
    
    path = myEnv.rodsHome + '/testinfoio.txt'
    
    # Open a file for writing
    f = irodsOpen(conn, path, 'w')
    f.write("\/"*25)
    
    print "Collection :", f.getCollName()
    print "Data Name :", f.getName()
    print "Desc Inx :", f.getDescInx()
    print "Position :", f.getPosition()
    print "Repl Number :", f.getReplNumber()
    print "Resource Name :", f.getResourceName()
    print "Size :", f.getSize()  # size = 0 because size is updated when you close the file
    
    f.close()
    
    f.delete()
    
    conn.disconnect()