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

OBF_PWD_PATH = os.environ['HOME'] + "/.irods/.irodsA"

if __name__ == "__main__":
    # Get the plain text password
    status, password = obfGetPw()
    print password
    # Get the encrypted password
    status, obf_password = obfiGetPw(OBF_PWD_PATH)
    print obf_password
    
    # you can use obfiDecode(obf_password) or obfiEncode(password)
    # to encode or decode a password
    
    envVal = obfiGetEnvKey()
    status, decoded_password = obfiDecode(obf_password, envVal)
    print decoded_password
    
    encoded_password = obfiEncode(password, envVal)
    print encoded_password
    
    status, decoded_password = obfiDecode(encoded_password, envVal)
    print decoded_password
    
    
    # Parse the .irodsEnv file
    status, myEnv = getRodsEnv()
    
    # Connection to a server with the default values
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
    
    # 3 different ways to log on the server
    status = clientLogin(conn)
    #status = clientLoginWithPassword(conn, password)
    #status = clientLoginWithObfPassword(conn, obf_password)
    
    print status
    
    # Do what you have to do
    
    # Disconnect
    status = conn.disconnect()
    #status = rcDisconnect(conn)
    