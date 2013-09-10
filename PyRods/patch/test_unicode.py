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
import irods

if __name__ == "__main__":
    conn, errMsg = irods.rcConnect(u"localhost", 1247, u"rods", u"tempZone", 0)
    print conn, errMsg
    status = clientLogin(conn)
    
    print status
    print getUserInfo(conn, u"rods//??")
    
    conn.disconnect()