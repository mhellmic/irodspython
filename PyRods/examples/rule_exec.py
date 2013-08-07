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

def printMsParamNew(outParamArray, output):
    if not outParamArray:
        return
    
    for i in xrange(outParamArray.len):
        msParam = outParamArray.getMsParam(i)

        if msParam.label == "ruleExecOut":
            continue

        if msParam.label and msParam.type and msParam.inOutStruct:
            if msParam.type == STR_MS_T:
                print "%s = %s" % (msParam.label, msParam.getInOutAsChar())
            elif msParam.type == INT_MS_T:
                print "%s = %i" % (msParam.label, msParam.getInOutAsInt())
            elif msParam.type == DOUBLE_MS_T:
                print "%s = %f" % (msParam.label, msParam.getInOutAsDouble())
            elif msParam.type == KeyValPair_MS_T:
                kVPairs = msParam.getInOutAsKeyValPair()
                print "KVpairs %s: %i" % (msParam.label, kVPairs.len)
                for j in xrange(kVPairs.len):
                    print "       %s = %s" % (kVPairs.getKeyWord(j),
                                              kVPairs.getValue(j))
            elif msParam.type == TagStruct_MS_T:
                tagValues = msParam.getInOutAsTagStruct()
                print "Tags %s: %i" % (msParam.label, tagValues.len)
                for j in xrange(tagValues.len):
                    print "       AttName = %s" % (tagValues.getKeyWord(j))
                    print "       PreTag  = %s" % (tagValues.getPreTag(j))
                    print "       PostTag = %s" % (tagValues.getPostTag(j))
            elif msParam.type == ExecCmdOut_MS_T:
                execCmdOut = msParam.getInOutAsExecCmdOut()
                if execCmdOut.stdoutBuf.buf != None:
                    print "STDOUT = %s" % (execCmdOut.stdoutBuf.getBufAsChar())
                if execCmdOut.stderrBuf.buf != None:
                    print "STRERR = %s" % (execCmdOut.stderrBuf.getBufAsChar())
            else:
                print "%s: %s" % (msParam.label, msParam.type)
                
        if msParam.inpOutBuf:
            print "    outBuf: buf length = %d" % (msParam.inpOutBuf.len)

if __name__ == "__main__":
    # Parse the .irodsEnv file
    status, myEnv = getRodsEnv()
    
    # Connection to a server with the default values
    conn, errMsg = rcConnect(myEnv.rodsHost, myEnv.rodsPort, 
                             myEnv.rodsUserName, myEnv.rodsZone)
    
    # log on the server
    status = clientLogin(conn)
    
    execMyRuleInp = execMyRuleInp_t()
    msParamArray = msParamArray_t()
    execMyRuleInp.myRule = 'myTestRule { writeLine("stdout","Sample rule *Double *Int *Path " ); }'
    execMyRuleInp.inpParamArray = msParamArray
    addCharParamToArray(msParamArray, "*Path", "/myZone/home/john/coll1")
    addIntParamToArray(msParamArray, "*Int", 12)
    addDoubleParamToArray(msParamArray, "*Double", 12.0)
    
    keyVal = keyValPair_t()
    addKeyVal(keyVal, "test1", "value1")
    addKeyVal(keyVal, "test2", "value2")
    addKeyValParamToArray(msParamArray, "*keyVal", keyVal)
    
    tagStruct = tagStruct_t()
    addTagStruct(tagStruct, "pre", "post", "keyWord")
    addTagStructParamToArray(msParamArray, "*tag", tagStruct)
    
    printMsParamNew(execMyRuleInp.inpParamArray, 0)
    
    execMyRuleInp.outParamDesc = "ruleExecOut"
    status, outParamArray = rcExecMyRule(conn, execMyRuleInp)
    
    msParam = outParamArray.getMsParam(0)
    
    printMsParamNew(outParamArray, 0)
    
    mP = getMsParamByType(outParamArray, ExecCmdOut_MS_T)
    if mP != None:
        execCmdOut = mP.getInOutAsExecCmdOut()
        if execCmdOut.stdoutBuf.buf != None:
            print execCmdOut.stdoutBuf.getBufAsChar()
        if execCmdOut.stderrBuf.buf != None:
            print execCmdOut.stderrBuf.getBufAsChar()

    # Disconnect
    status = conn.disconnect()
    