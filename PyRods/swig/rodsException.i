/* Copyright (c) 2013, University of Liverpool
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *
 * Author       : Jerome Fuselier
 */


%pythoncode %{

# Keep the status of the last called API function
lastStatus = 0

def getStatus():
    return lastStatus

def getStatusStr():
    errName, _ = rodsErrorName(lastStatus)
    return errName

class IrodsException(Exception):

    def __init__(self, errCode):
        self.errCode = errCode
        self.errName, self.errSubName = rodsErrorName(errCode)

    def __str__(self):
        if self.errSubName:
            msg = "iRODS failed with error %d %s %s" % (self.errCode,
                                                        self.errName,
                                                        self.errSubName)
            return msg
        else:
            msg = "iRODS failed with error %d %s" % (self.errCode,
                                                     self.errName)
            return msg
%}