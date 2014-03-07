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
import zipfile

if __name__ == "__main__":
    status, myEnv = getRodsEnv()
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
    
    path = myEnv.rodsHome + '/test_zipfile.zip'
    print path
    
    # Write a zip file using zipfile
    status = clientLogin(conn)
    f = irodsOpen(conn, path, 'w')
    myzip = zipfile.ZipFile(f, 'w')
    myzip.writestr("test.info", "Test Zipfile API")
    myzip.close()
    f.close()
    
    # Read the zip file directly from iRODS
    f = irodsOpen(conn, path, 'r')
    myzip = zipfile.ZipFile(f, 'r')
    myzip.printdir()
    for obj in myzip.infolist():
        print "- ", obj.filename, ": "
        fi = myzip.open(obj.filename, "r")
        print fi.read()
        fi.close()
    myzip.close()
    f.close()
    
    conn.disconnect()