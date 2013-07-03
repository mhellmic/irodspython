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

## icommands to set quotas: 
##   - iadmin suq rods 'total' 200000
##   - iadmin suq rods 'demoResc' 20000
##
##   - iadmin sgq public 'total' 200000
##   - iadmin sgq public 'demoResc' 20000

## Examples of usage:
## python iquota.py
## python iquota.py -a
## python iquota.py --usage
## python iqouta.py -a --usage
## python iquota.py -u josh
## python iquota.py -h


from irods import *
import argparse

quotaTime = ""
QUOTA_APPROACH_WARNING_SIZE = -10000000000


def printNice(inArg, units):
    niceString = '{:,}'.format(inArg)
    
    
    commaCount = niceString.count(",")
    
    if commaCount == 1:
        numberName = "thousand"
        firstPart = int(inArg / 1e3)
        
    if commaCount == 2:
        numberName = "million"
        firstPart = int(inArg / 1e6)
        
    if commaCount == 3:
        numberName = "billion"
        firstPart = int(inArg / 1e9)
        
    if commaCount == 4:
        numberName = "trillion"
        firstPart = int(inArg / 1e12)
        
    if commaCount == 0:
        print "%s %s" % (niceString, units),
    elif commaCount > 4:
        print "%s (very many) %s" % (niceString, units),
    else:
        print "%s (%s %s) %s" % (niceString, firstPart, numberName, units),

def showUserGroupMembership(userNameIn, usersZone):
    showUserZone = True
    
    status, userName, zoneName = parseUserName(userNameIn)
    
    if not zoneName:
        zoneName = usersZone
        showUserZone = False 
    
    l = getUserGroupMembership(conn, userName, zoneName)
    
    if showUserZone:
        print "User %s#%s is a member of groups: " % (userName, zoneName),
    else:
        print "User %s is a member of groups: " % (userName),
        
    print "%s" % ", ".join(l)

def showQuotas(conn, userName, userQ, globalQ):
    res = getQuota(conn, userName, userQ, globalQ)
    
    if not res:
        print "  None"
        print
    
    for el in res:
        print "  Resource: ", el.get('resource', "")
        if userQ:
            print "  User: ", el.get('user', "")
        else:
            print "  Group: ", el.get('group', "")
        print "  Zone: ", el.get('zone', "")
        print "  Quota: ", 
        printNice(el.get('quota', 0), "bytes")
        print
        print "  Over: ", 
        printNice(el.get('over', 0), "bytes")
        if el.get('over', 0) > 0:
            print " OVER QUOTA"
        elif el.get('over', 0) > QUOTA_APPROACH_WARNING_SIZE:
            print " (Nearing quota)"
        else:
            print " (under quota)"
            
        global quotaTime
        quotaTime = el.get("time", "")
        
        print
    
def showUserUsage(userName, usersZone):
    res = getUserUsage(userName, usersZone)
    
    if not res:
        print "No records found, run 'iadmin cu' to calculate usage"
        return
    
    print "Resource        User            Data-stored (bytes)"
    
    for d in res:
        resc = d.get('resource', '')
        print resc,
        k = len(resc)
        if k < 14:
            print " " * (14-k),
            
        user = d.get('user', '')
        print user,
        k = len(user)
        if k < 14:
            print " " * (14-k),
            
        printNice(d.get("usage", 0), "")
        print
        
        
        global quotaTime
        quotaTime = d.get("time", "")
        
    print

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="""Show information on iRODS quotas (if any).
By default, information is displayed for the current iRODS user.

The 'over' values indicate whether the user or group is over quota
or not and by how much; positive values are over-quota.
The 'usage' information shows how much data is stored on each resource,
when last determined.""")
    parser.add_argument("-a", "--all", action='store_true', help='All users')
    parser.add_argument("-u", "--user", action='store', metavar="UserName[#ZoneName]",
                        help="For the specified user")
    parser.add_argument("--usage", action='store_true', help='Show usage information')
    
    args = parser.parse_args()
        
    # Parse the .irodsEnv file
    status, myEnv = getRodsEnv()
    
    # Connection to a server with the default values
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
    
    status = clientLogin(conn)
    
    userName =  myEnv.rodsUserName
    
    if args.user:
        userName = args.user
        
    if args.all:
        userName = ""
        
    if args.usage: 
        showUserUsage(userName, myEnv.rodsZone)
    else:
        if userName:
            print "Resource quotas for user %s:" % userName
        else:
            print "Resource quotas for users:"
        showQuotas(conn, userName, True, False)
        
        if userName:
            print "Global quotas for user %s:" % userName
        else:
            print "Global quotas for users:"
        showQuotas(conn, userName, True, True)
        
        print "Group quotas on resources:"
        showQuotas(conn, "", False, False)
        
        print "Group global (total) quotas:"
        showQuotas(conn, "", False, True)
        
        if userName:
            showUserGroupMembership(userName, myEnv.rodsZone)
    
    if quotaTime:
      print "Information was set at " + quotaTime
    
    # Disconnect
    status = conn.disconnect()
    