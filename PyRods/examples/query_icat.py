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
import os


if __name__ == "__main__":
    # Parse the .irodsEnv file
    status, myEnv = getRodsEnv()
    
    # Connection to a server with the default values
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
    
    status = clientLogin(conn)
    
    resc_name = "demoResc"
    columnNames = ["mem_used", "create_ts"]
    
    sqlCondInp = inxValPair_t()
    selectInp = inxIvalPair_t()
    selectInp.init([COL_SL_MEM_USED,
                    COL_SL_CREATE_TIME,
                    ], 
                   [0, 0], 2)
    sqlCondInp.init([COL_SL_RESC_NAME],["='%s'" % resc_name], 1)
    
    l = queryToFormatDictList(conn, selectInp, sqlCondInp, columnNames)
    
    for i in l[:5]:
        print i
    
    # Disconnect
    status = conn.disconnect()
    