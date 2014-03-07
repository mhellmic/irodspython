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
import pickle

def readline(f, size=None):
    res = ""
    end = False
    
    c = f.read(1)
    readsize = 1
    end = c == ''

    print end

    while not end:
        res += c
        c = f.read(1)
        readsize += 1
        if not c or c in ['\r', '\n']:
            res += c
            end = True
        if size:
            if readsize >= size:
                res += c
                end = True

    return res

class TestPickle(object):
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return str(self.a) + " - " + str(self.b) + " - (" + str(self.c) + ")"


if __name__ == "__main__":
    status, myEnv = getRodsEnv()
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
     
    path = myEnv.rodsHome + '/test_pickle.dmp'
    print path
     
    obj1 = TestPickle(12, "Test", None)
    obj2 = TestPickle(121, "Test 2", obj1)
     
    print obj2
     
    # Dump an object in a file in iRODS
    status = clientLogin(conn)
    f = irodsOpen(conn, path, 'w')
    pickle.dump(obj2, f)
    f.close()
     
    # Read a dumped object directly from iRODS
    f = irodsOpen(conn, path, 'r')
    obj = pickle.load(f)
    f.close()
    print obj
     
    conn.disconnect()