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

import unittest
from irods import *

class iRODSTestCase(unittest.TestCase):
    
    def setUp(self):
        status, self.myEnv = getRodsEnv()
        
        self.assertEqual(status, 0)
        
        self.conn, self.errMsg = rcConnect(self.myEnv.rodsHost, self.myEnv.rodsPort, 
                                           self.myEnv.rodsUserName, self.myEnv.rodsZone)
        
        self.assert_(self.conn)
        
        status = clientLogin(self.conn)
        self.assertEqual(status, 0)
        
        
    def tearDown(self):
        rcDisconnect(self.conn) 



def create_authCheckInp_t(challenge, response, username):
    tmp = authCheckInp_t()
    tmp.challenge = challenge
    tmp.response = response
    tmp.username = username
    return tmp

def create_authCheckOut_t(privLevel, clientPrivLevel, serverResponse):
    tmp = authCheckOut_t()
    tmp.privLevel = privLevel
    tmp.clientPrivLevel = clientPrivLevel
    tmp.serverResponse = serverResponse
    return tmp

def create_authInfo_t(authScheme , authFlag , flag , ppid , host , authStr):
    tmp = authInfo_t()
    tmp.authScheme = authScheme
    tmp.authFlag = authFlag
    tmp.flag = flag
    tmp.ppid = ppid
    tmp.host = host
    tmp.authStr = authStr
    return tmp

def create_authResponseInp_t(response, username):
    tmp = authResponseInp_t()
    tmp.response = response
    tmp.username = username
    return tmp

def create_authRequestOut_t(challenge):
    tmp = authRequestOut_t()
    tmp.challenge = challenge
    return tmp

def create_bytesBuf_t(buf):
    tmp = bytesBuf_t()
    tmp.setBuf(buf, len(buf))
    return tmp

def create_chkObjPermAndStat_t(objPath, permission, flags, status, condInput):
    tmp = chkObjPermAndStat_t()
    tmp.objPath = objPath
    tmp.permission = permission
    tmp.flags = flags
    tmp.status = status
    tmp.condInput = condInput
    return tmp

def create_collEnt_t(objType, replNum, replStatus, dataMode, dataSize, collName, 
                     dataName, dataId, createTime, modifyTime, chksum, resource, 
                     rescGrp, phyPath, ownerName, specColl):
    tmp = collEnt_t()
    tmp.objType = objType
    tmp.replNum = replNum
    tmp.replStatus = replStatus
    tmp.dataMode = dataMode
    tmp.dataSize = dataSize
    tmp.collName = collName
    tmp.dataName = dataName
    tmp.dataId = dataId
    tmp.createTime = createTime
    tmp.modifyTime = modifyTime
    tmp.chksum = chksum
    tmp.resource = resource
    tmp.rescGrp = rescGrp
    tmp.phyPath = phyPath
    tmp.ownerName = ownerName
    tmp.specColl = specColl
    return tmp

def create_collHandle_t(state, inuseFlag, flags, rowInx, rodsObjStat, 
                        genQueryInp, dataObjInp, dataObjSqlResult, 
                        collSqlResult, linkedObjPath, prevdataId):
    tmp = collHandle_t()
    tmp.state = state
    tmp.inuseFlag = inuseFlag
    tmp.flags = flags
    tmp.rowInx = rowInx
    tmp.rodsObjStat = rodsObjStat
    #tmp.queryHandle = queryHandle
    tmp.genQueryInp = genQueryInp
    tmp.dataObjInp = dataObjInp
    tmp.dataObjSqlResult = dataObjSqlResult
    tmp.collSqlResult = collSqlResult
    tmp.linkedObjPath = linkedObjPath
    tmp.prevdataId = prevdataId
    return tmp

def create_collInp_t(collName , flags, oprType, condInput):
    tmp = collInp_t()
    tmp.collName = collName 
    tmp.flags = flags
    tmp.oprType = oprType
    tmp.condInput = condInput
    return tmp

def create_collSqlResult_t(rowCnt, attriCnt, continueInx, totalRowCount, 
                           collName, collType, collInfo1, collInfo2, 
                           collOwner, collCreateTime, collModifyTime):
    tmp = collSqlResult_t()
    tmp.rowCnt = rowCnt
    tmp.attriCnt = attriCnt
    tmp.continueInx = continueInx
    tmp.totalRowCount = totalRowCount
    tmp.collName = collName
    tmp.collType = collType
    tmp.collInfo1 = collInfo1
    tmp.collInfo2 = collInfo2
    tmp.collOwner = collOwner
    tmp.collCreateTime = collCreateTime
    tmp.collModifyTime = collModifyTime
    return tmp

def create_dataCopyInp_t(dataOprInp, portalOprOut):
    tmp = dataCopyInp_t()
    tmp.dataOprInp = dataOprInp
    tmp.portalOprOut = portalOprOut
    return tmp

def create_dataObjCopyInp_t(srcDataObjInp, destDataObjInp):
    tmp = dataObjCopyInp_t()
    tmp.srcDataObjInp = srcDataObjInp
    tmp.destDataObjInp = destDataObjInp
    return tmp

def create_dataObjInfo_t(objPath, rescName, rescGroupName, dataType, dataSize, 
                         chksum, version, filePath, #rescInfo, 
                         dataOwnerName, 
                         dataOwnerZone, replNum, replStatus, statusString, 
                         dataId, collId, dataMapId, flags, dataComments, 
                         dataMode, dataExpiry, dataCreate, dataModify, 
                         dataAccess, dataAccessInx, writeFlag, destRescName, 
                         backupRescName, subPath, specColl, regUid, otherFlags, 
                         condInput, next):
    tmp = dataObjInfo_t()
    tmp.objPath = objPath
    tmp.rescName = rescName
    tmp.rescGroupName = rescGroupName
    tmp.dataType = dataType
    tmp.dataSize = dataSize
    tmp.chksum = chksum
    tmp.version = version
    tmp.filePath = filePath
    #tmp.rescInfo = rescInfo
    tmp.dataOwnerName = dataOwnerName
    tmp.dataOwnerZone = dataOwnerZone
    tmp.replNum = replNum
    tmp.replStatus = replStatus
    tmp.statusString = statusString
    tmp.dataId = dataId
    tmp.collId = collId
    tmp.dataMapId = dataMapId
    tmp.flags = flags
    tmp.dataComments = dataComments
    tmp.dataMode = dataMode
    tmp.dataExpiry = dataExpiry
    tmp.dataCreate = dataCreate
    tmp.dataModify = dataModify
    tmp.dataAccess = dataAccess
    tmp.dataAccessInx = dataAccessInx
    tmp.writeFlag = writeFlag
    tmp.destRescName = destRescName
    tmp.backupRescName = backupRescName
    tmp.subPath = subPath
    tmp.specColl = specColl
    tmp.regUid = regUid
    tmp.otherFlags = otherFlags
    tmp.condInput = condInput
    tmp.next = next
    return tmp

def create_dataObjInp_t(objPath, createMode, openFlags, offset, dataSize, 
                        numThreads, oprType, specColl, condInput):
    tmp = dataObjInp_t()
    tmp.objPath = objPath
    tmp.createMode = createMode
    tmp.openFlags = openFlags
    tmp.offset = offset
    tmp.dataSize = dataSize
    tmp.numThreads = numThreads
    tmp.oprType = oprType
    tmp.specColl = specColl
    tmp.condInput = condInput
    return tmp

def create_dataObjSqlResult_t(rowCnt, attriCnt, continueInx, totalRowCount, 
                              collName, dataName, dataMode, dataSize, 
                              createTime, modifyTime, chksum, replStatus, 
                              dataId, resource, phyPath, ownerName, replNum, 
                              rescGrp, dataType):
    tmp = dataObjSqlResult_t()
    tmp.rowCnt = rowCnt
    tmp.attriCnt = attriCnt
    tmp.continueInx = continueInx
    tmp.totalRowCount = totalRowCount
    tmp.collName = collName
    tmp.dataName = dataName
    tmp.dataMode = dataMode
    tmp.dataSize = dataSize
    tmp.createTime = createTime
    tmp.modifyTime = modifyTime
    tmp.chksum = chksum
    tmp.replStatus = replStatus
    tmp.dataId = dataId
    tmp.resource = resource
    tmp.phyPath = phyPath
    tmp.ownerName = ownerName
    tmp.replNum = replNum
    tmp.rescGrp = rescGrp
    tmp.dataType = dataType
    return tmp


def create_dataOprInp_t(oprType, numThreads, srcL3descInx, destL3descInx, 
                        srcRescTypeInx, destRescTypeInx, offset, dataSize, 
                        condInput):
    tmp = dataOprInp_t()
    tmp.oprType = oprType
    tmp.numThreads = numThreads
    tmp.srcL3descInx = srcL3descInx
    tmp.destL3descInx = destL3descInx
    tmp.srcRescTypeInx = srcRescTypeInx
    tmp.destRescTypeInx = destRescTypeInx
    tmp.offset = offset
    tmp.dataSize = dataSize
    tmp.condInput = condInput
    return tmp

def create_execCmd_t(cmd, cmdArgv, execAddr, hintPath, addPathToArgv, dummy, 
                     condInput):
    tmp = execCmd_t()
    tmp.cmd = cmd
    tmp.cmdArgv = cmdArgv
    tmp.execAddr = execAddr
    tmp.hintPath = hintPath
    tmp.addPathToArgv = addPathToArgv
    tmp.dummy = dummy
    tmp.condInput = condInput
    return tmp

def create_execCmdOut_t(stdoutBuf, stderrBuf, status):
    tmp = execCmdOut_t()
    tmp.stdoutBuf = create_bytesBuf_t(stdoutBuf)
    tmp.stderrBuf = create_bytesBuf_t(stderrBuf)
    tmp.status = status
    return tmp

def create_execMyRuleInp_t(myRule, addr, condInput, outParamDesc, inpParamArray):
    tmp = execMyRuleInp_t()
    tmp.myRule = myRule
    tmp.addr = addr
    tmp.condInput = condInput
    tmp.outParamDesc = outParamDesc
    tmp.inpParamArray = inpParamArray
    return tmp

def create_fileChmodInp_t(#fileType, 
                          addr, fileName, mode):
    tmp = fileChmodInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.fileName = fileName
    tmp.mode = mode
    return tmp

def create_fileChksumInp_t(#fileType, 
                           addr, fileName, flag):
    tmp = fileChksumInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.fileName = fileName
    tmp.flag = flag
    return tmp

def create_fileCloseInp_t(fileInx):
    tmp = fileCloseInp_t()
    tmp.fileInx = fileInx
    return tmp

def create_fileClosedirInp_t(fileInx):
    tmp = fileClosedirInp_t()
    tmp.fileInx = fileInx
    return tmp

def create_fileFstatInp_t(fileInx):
    tmp = fileFstatInp_t()
    tmp.fileInx = fileInx
    return tmp

def create_fileFsyncInp_t(fileInx):
    tmp = fileFsyncInp_t()
    tmp.fileInx = fileInx
    return tmp

def create_fileGetFsFreeSpaceInp_t(#fileType, 
                                   addr, fileName, flag):
    tmp = fileGetFsFreeSpaceInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.fileName = fileName
    tmp.flag = flag
    return tmp

def create_fileGetFsFreeSpaceOut_t(size):
    tmp = fileGetFsFreeSpaceOut_t()
    tmp.size = size
    return tmp

def create_fileLseekInp_t(fileInx, offset, whence):
    tmp = fileLseekInp_t()
    tmp.fileInx = fileInx
    tmp.offset = offset
    tmp.whence = whence
    return tmp

def create_fileLseekOut_t(offset):
    tmp = fileLseekOut_t()
    tmp.offset = offset
    return tmp

def create_fileMkdirInp_t(#fileType, 
                          addr, dirName, mode, condInput):
    tmp = fileMkdirInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.dirName = dirName
    tmp.mode = mode
    tmp.condInput = condInput
    return tmp

def create_fileOpenInp_t(#fileType, 
                         otherFlags, addr, fileName, flags, mode, dataSize, 
                         condInput):
    tmp = fileOpenInp_t()
    #tmp.fileType = fileType
    tmp.otherFlags = otherFlags
    tmp.addr = addr
    tmp.fileName = fileName
    tmp.flags = flags
    tmp.mode = mode
    tmp.dataSize = dataSize
    tmp.condInput = condInput
    return tmp

def create_fileOpendirInp_t(#fileType, 
                            addr, dirName):
    tmp = fileOpendirInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.dirName = dirName
    return tmp

def create_fileReadInp_t(fileInx, len):
    tmp = fileReadInp_t()
    tmp.fileInx = fileInx
    tmp.len = len
    return tmp

def create_fileRenameInp_t(#fileType, 
                           addr, oldFileName, newFileName):
    tmp = fileRenameInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.oldFileName = oldFileName
    tmp.newFileName = newFileName
    return tmp

def create_fileRmdirInp_t(#fileType, 
                          flags, addr, dirName):
    tmp = fileRmdirInp_t()
    #tmp.fileType = fileType
    tmp.flags = flags
    tmp.addr = addr
    tmp.dirName = dirName
    return tmp

def create_fileStageInp_t(#fileType, 
                          addr, fileName, flag):
    tmp = fileStageInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.fileName = fileName
    tmp.flag = flag
    return tmp

def create_fileStatInp_t(#fileType, 
                         addr, fileName):
    tmp = fileStatInp_t()
    tmp = fileGetFsFreeSpaceInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.fileName = fileName
    return tmp

def create_fileUnlinkInp_t(#fileType, 
                           addr, fileName):
    tmp = fileUnlinkInp_t()
    tmp = fileGetFsFreeSpaceInp_t()
    #tmp.fileType = fileType
    tmp.addr = addr
    tmp.fileName = fileName
    return tmp

def create_fileWriteInp_t(fileInx, len):
    tmp = fileWriteInp_t()
    tmp.fileInx = fileInx
    tmp.len = len
    return tmp

def create_generalAdminInp_t(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, 
                             arg8, arg9):
    tmp = generalAdminInp_t()
    tmp.arg0 = arg0
    tmp.arg1 = arg1
    tmp.arg2 = arg2
    tmp.arg3 = arg3
    tmp.arg4 = arg4
    tmp.arg5 = arg5
    tmp.arg6 = arg6
    tmp.arg7 = arg7
    tmp.arg8 = arg8
    tmp.arg9 = arg9
    return tmp

def create_generalUpdateInp_t(type, values):
    tmp = generalUpdateInp_t()
    tmp.type = type
    tmp.values = values
    return tmp

def create_genQueryInp_t(maxRows, continueInx, rowOffset, options, condInput, 
                         selectInp, sqlCondInp):
    tmp = genQueryInp_t()
    tmp.maxRows = maxRows
    tmp.continueInx = continueInx
    tmp.rowOffset = rowOffset
    tmp.options = options
    tmp.condInput = condInput
    tmp.selectInp = selectInp
    tmp.sqlCondInp = sqlCondInp
    return tmp

def create_genQueryOut_t(rowCnt, attriCnt, continueInx, totalRowCount, 
                         sqlResult):
    tmp = genQueryOut_t()
    tmp.rowCnt = rowCnt
    tmp.attriCnt = attriCnt
    tmp.continueInx = continueInx
    tmp.totalRowCount = totalRowCount
    tmp.sqlResult = sqlResult
    return tmp

def create_getTempPasswordOut_t(stringToHashWith):
    tmp = getTempPasswordOut_t()
    tmp.stringToHashWith = stringToHashWith
    return tmp

def create_getXmsgTicketInp_t(expireTime, flag):
    tmp = getXmsgTicketInp_t()
    tmp.expireTime = expireTime
    tmp.flag = flag
    return tmp

def create_gsiAuthRequestOut_t(serverDN):
    tmp = gsiAuthRequestOut_t()
    tmp.serverDN = serverDN
    return tmp

def create_inxIvalPair_t(l1, l2, n):
    tmp = inxIvalPair_t()
    tmp.init(l1, l2, n)
    return tmp

def create_inxValPair_t(l1, l2, n):
    tmp = inxValPair_t()
    tmp.init(l1, l2, n)
    return tmp

def create_keyValPair_t(l1, l2, n):
    tmp = keyValPair_t()
    tmp.init(l1, l2, n)
    return tmp

def create_MD5_CTX():
    tmp = MD5_CTX()
    return tmp

def create_miscSvrInfo_t(serverType, serverBootTime,relVersion, apiVersion, 
                         rodsZone):
    tmp = miscSvrInfo_t()
    tmp.serverType = serverType
    tmp.serverBootTime = serverBootTime
    tmp.relVersion = relVersion
    tmp.apiVersion = apiVersion
    tmp.rodsZone = rodsZone
    return tmp

def create_modAccessControlInp_t(recursiveFlag, accessLevel, userName, zone, 
                                 path):
    tmp = modAccessControlInp_t()
    tmp.recursiveFlag = recursiveFlag
    tmp.accessLevel = accessLevel
    tmp.userName = userName
    tmp.zone = zone
    tmp.path = path
    return tmp

def create_modAVUMetadataInp_t(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, 
                               arg8, arg9):
    tmp = modAVUMetadataInp_t()
    tmp.arg0 = arg0
    tmp.arg1 = arg1
    tmp.arg2 = arg2
    tmp.arg3 = arg3
    tmp.arg4 = arg4
    tmp.arg5 = arg5
    tmp.arg6 = arg6
    tmp.arg7 = arg7
    tmp.arg8 = arg8
    tmp.arg9 = arg9
    return tmp

def create_modDataObjMeta_t(dataObjInfo, regParam):
    tmp = modDataObjMeta_t()
    tmp.dataObjInfo = dataObjInfo
    tmp.regParam = regParam
    return tmp

def create_msParam_t(label, type, #inOutStruct, 
                     inpOutBuf):
    tmp = msParam_t()
    tmp.label = label
    tmp.type = type
    #tmp.inOutStruct = inOutStruct
    tmp.inpOutBuf = inpOutBuf
    return tmp

def create_msParamArray_t(len, oprType):#, msParam):
    tmp = msParamArray_t()
    tmp.len = len
    tmp.oprType = oprType
    #tmp.msParam = msParam
    return tmp

def create_openedDataObjInp_t(l1descInx, len, whence, oprType, offset, 
                              bytesWritten, condInput):
    tmp = openedDataObjInp_t()
    tmp.l1descInx = l1descInx
    tmp.len = len
    tmp.whence = whence
    tmp.oprType = oprType
    tmp.offset = offset
    tmp.bytesWritten = bytesWritten
    tmp.condInput = condInput
    return tmp

def create_openStat_t(dataSize, dataType, dataMode, l3descInx, replStatus, 
                      rescTypeInx, replNum):
    tmp = openStat_t()
    tmp.dataSize = dataSize
    tmp.dataType = dataType
    tmp.dataMode = dataMode
    tmp.l3descInx = l3descInx
    tmp.replStatus = replStatus
    tmp.rescTypeInx = rescTypeInx
    tmp.replNum = replNum
    return tmp

def create_portalOprOut_t(status, l1descInx, numThreads, chksum, portList):
    tmp = portalOprOut_t()
    tmp.status = status
    tmp.l1descInx = l1descInx
    tmp.numThreads = numThreads
    tmp.chksum = chksum
    tmp.portList = portList
    return tmp

def create_portList_t(portNum, cookie, windowSize, hostAddr):
    tmp = portList_t()
    tmp.portNum = portNum
    tmp.cookie = cookie
    tmp.windowSize = windowSize
    tmp.hostAddr = hostAddr
    return tmp


def create_rcComm_t(host, sock, portNum, loggedIn, proxyUser, clientUser, 
                    svrVersion, flag, apiInx, status, windowSize, 
                    reconnectedSock):
    tmp = rcComm_t()
    tmp.host = host
    tmp.sock = sock
    tmp.portNum = portNum
    tmp.loggedIn = loggedIn
    tmp.proxyUser = proxyUser
    tmp.clientUser = clientUser
    tmp.svrVersion = svrVersion
    tmp.flag = flag
    tmp.apiInx = apiInx
    tmp.status = status
    tmp.windowSize = windowSize
    tmp.reconnectedSock = reconnectedSock
    return tmp

def create_rcvXmsgInp_t(rcvTicket, msgNumber, seqNumber, msgCondition):
    tmp = rcvXmsgInp_t()
    tmp.rcvTicket = rcvTicket
    tmp.msgNumber = msgNumber
    tmp.seqNumber = seqNumber
    tmp.msgCondition = msgCondition
    return tmp

def create_rcvXmsgOut_t(msgType, sendUserName, sendAddr, msgNumber, seqNumber, 
                        msg):
    tmp = rcvXmsgOut_t()
    tmp.msgType = msgType
    tmp.sendUserName = sendUserName
    tmp.sendAddr = sendAddr
    tmp.msgNumber = msgNumber
    tmp.seqNumber = seqNumber
    tmp.msg = msg
    return tmp

def create_regReplica_t(srcDataObjInfo, destDataObjInfo, condInput):
    tmp = regReplica_t()
    tmp.srcDataObjInfo = srcDataObjInfo
    tmp.destDataObjInfo = destDataObjInfo
    tmp.condInput = condInput
    return tmp

def create_rErrMsg_t(status, msg):
    tmp = rErrMsg_t()
    tmp.status = status
    tmp.msg = msg
    return tmp

def create_rodsArguments_t(add, age, agevalue, all, accessControl, admin, 
                           ascitime, attr, noattr, attrStr, bulk, backupMode, 
                           condition, conditionString, collection, 
                           collectionString, dataObjects, dim, dryrun, echo, 
                           empty, force, file, fileString, rescGroup, 
                           rescGroupString, header, help, hostAddr, 
                           hostAddrString, input, redirectConn, checksum, 
                           verifyChecksum, dataType, dataTypeString, longOption, 
                           link, rlock, wlock, veryLongOption, mountCollection, 
                           mountType, replNum, replNumValue, noPage, number, 
                           numberValue, physicalPath, physicalPathString, 
                           logicalPath, logicalPathString, progressFlag, option, 
                           optionString, orphan, purgeCache, bundle, prompt, 
                           query, queryStr, rbudp, reg, recursive, resource, 
                           resourceString, remove, sizeFlag, size, srcResc, 
                           srcRescString, subset, intsubsetByVal, subsetStr, 
                           test, ticket, ticketString, reconnect, user, 
                           userString, unmount, verbose, veryVerbose, zone, 
                           zoneName, verify, var, varStr, extract, restart, 
                           restartFileString, lfrestart, lfrestartFileString, 
                           version, retries, retriesValue, regRepl, excludeFile, 
                           excludeFileString, parallel, serial, masterIcat, 
                           silent, sql, optind):
    tmp = rodsArguments_t()
    tmp.add = add
    tmp.age = age
    tmp.agevalue = agevalue
    tmp.all = all
    tmp.accessControl = accessControl
    tmp.admin = admin
    tmp.ascitime = ascitime
    tmp.attr = attr
    tmp.noattr = noattr
    tmp.attrStr = attrStr
    tmp.bulk = bulk
    tmp.backupMode  = backupMode
    tmp.condition = condition
    tmp.conditionString = conditionString
    tmp.collection = collection
    tmp.collectionString = collectionString
    tmp.dataObjects = dataObjects
    tmp.dim = dim
    tmp.dryrun = dryrun
    tmp.echo = echo
    tmp.empty = empty
    tmp.force = force
    tmp.file = file
    tmp.fileString = fileString
    tmp.rescGroup = rescGroup
    tmp.rescGroupString = rescGroupString
    tmp.header = header
    tmp.help = help
    tmp.hostAddr = hostAddr
    tmp.hostAddrString = hostAddrString
    tmp.input = input
    tmp.redirectConn = redirectConn
    tmp.checksum = checksum
    tmp.verifyChecksum = verifyChecksum
    tmp.dataType = dataType
    tmp.dataTypeString  = dataTypeString
    tmp.longOption = longOption
    tmp.link = link
    tmp.rlock = rlock
    tmp.wlock = wlock
    tmp.veryLongOption = veryLongOption
    tmp.mountCollection = mountCollection
    tmp.mountType  = mountType
    tmp.replNum = replNum
    tmp.replNumValue = replNumValue
    tmp.noPage = noPage
    tmp.number = number
    tmp.numberValue = numberValue
    tmp.physicalPath = physicalPath
    tmp.physicalPathString = physicalPathString
    tmp.logicalPath = logicalPath
    tmp.logicalPathString = logicalPathString
    tmp.progressFlag = progressFlag
    tmp.option = option
    tmp.optionString = optionString
    tmp.orphan = orphan
    tmp.purgeCache = purgeCache
    tmp.bundle = bundle
    tmp.prompt = prompt
    tmp.query = query
    tmp.queryStr = queryStr
    tmp.rbudp = rbudp
    tmp.reg = reg
    tmp.recursive = recursive
    tmp.resource = resource
    tmp.resourceString = resourceString
    tmp.remove = remove
    tmp.sizeFlag = sizeFlag
    tmp.size = size
    tmp.srcResc = srcResc
    tmp.srcRescString = srcRescString
    tmp.subset = subset
    tmp.intsubsetByVal = intsubsetByVal
    tmp.subsetStr = subsetStr
    tmp.test = test
    tmp.ticket = ticket
    tmp.ticketString = ticketString
    tmp.reconnect = reconnect
    tmp.user = user
    tmp.userString = userString
    tmp.unmount = unmount
    tmp.verbose = verbose
    tmp.veryVerbose = veryVerbose
    tmp.zone = zone
    tmp.zoneName = zoneName
    tmp.verify = verify
    tmp.var = var
    tmp.varStr = varStr
    tmp.extract  = extract
    tmp.restart = restart
    tmp.restartFileString = restartFileString
    tmp.lfrestart = lfrestart
    tmp.lfrestartFileString = lfrestartFileString
    tmp.version = version
    tmp.retries = retries
    tmp.retriesValue = retriesValue
    tmp.regRepl = regRepl
    tmp.excludeFile = excludeFile
    tmp.excludeFileString = excludeFileString
    tmp.parallel = parallel
    tmp.serial = serial
    tmp.masterIcat = masterIcat
    tmp.silent = silent
    tmp.sql = sql
    tmp.optind = optind
    return tmp

def create_rodsDirent_t(d_offset, d_ino, d_reclen, d_namlen, d_name):
    tmp = rodsDirent_t()
    tmp.d_offset = d_offset
    tmp.d_ino = d_ino
    tmp.d_reclen = d_reclen
    tmp.d_namlen = d_namlen
    tmp.d_name = d_name
    return tmp

def create_rodsEnv(rodsUserName, rodsHost, rodsPort, xmsgHost, xmsgPort, 
                   rodsHome, rodsCwd, rodsAuthScheme, rodsDefResource, rodsZone, 
                   rodsServerDn, rodsLogLevel, rodsAuthFileName, rodsDebug):
    tmp = rodsEnv()
    tmp.rodsUserName = rodsUserName
    tmp.rodsHost = rodsHost
    tmp.rodsPort = rodsPort
    tmp.xmsgHost = xmsgHost
    tmp.xmsgPort = xmsgPort
    tmp.rodsHome = rodsHome
    tmp.rodsCwd = rodsCwd
    tmp.rodsAuthScheme = rodsAuthScheme
    tmp.rodsDefResource = rodsDefResource
    tmp.rodsZone = rodsZone
    tmp.rodsServerDn = rodsServerDn
    tmp.rodsLogLevel = rodsLogLevel
    tmp.rodsAuthFileName = rodsAuthFileName
    tmp.rodsDebug = rodsDebug
    return tmp

def create_rodsHostAddr_t(hostAddr, zoneName, portNum, dummyInt):
    tmp = rodsHostAddr_t()
    tmp.hostAddr = hostAddr
    tmp.zoneName = zoneName
    tmp.portNum = portNum
    tmp.dummyInt = dummyInt
    return tmp

def create_rodsObjStat_t(objSize, objType, dataMode, dataId, chksum, ownerName, 
                         ownerZone, createTime, modifyTime, specColl):
    tmp = rodsObjStat_t()
    tmp.objSize = objSize
    tmp.objType = objType
    tmp.dataMode = dataMode
    tmp.dataId = dataId
    tmp.chksum = chksum
    tmp.ownerName = ownerName
    tmp.ownerZone = ownerZone
    tmp.createTime = createTime
    tmp.modifyTime = modifyTime
    tmp.specColl = specColl
    return tmp

def create_rodsPath_t(objType, #objState, 
                      size, objMode, inPath, outPath, dataId, 
                      chksum, rodsObjStat):
    tmp = rodsPath_t()
    tmp.objType = objType
    #tmp.objState = objState
    tmp.size = size
    tmp.objMode = objMode
    tmp.inPath = inPath
    tmp.outPath = outPath
    tmp.dataId = dataId
    tmp.chksum = chksum
    tmp.rodsObjStat = rodsObjStat
    return tmp

def create_rodsPathInp_t(numSrc, srcPath, destPath, targPath, resolved):
    tmp = rodsPathInp_t()
    tmp.numSrc = numSrc
    tmp.srcPath = srcPath
    tmp.destPath = destPath
    tmp.targPath = targPath
    tmp.resolved = resolved
    return tmp

def create_rodsRestart_t(restartFile, fd, doneCnt, collection, lastDonePath, 
                         oprType, curCnt, restartState):
    tmp = rodsRestart_t()
    tmp.restartFile = restartFile
    tmp.fd = fd
    tmp.doneCnt = doneCnt
    tmp.collection = collection
    tmp.lastDonePath = lastDonePath
    tmp.oprType = oprType
    tmp.curCnt = curCnt
    tmp.restartState = restartState
    return tmp

def create_rodsStat_t(st_size, st_dev, st_ino, st_mode, 
                      st_nlink, st_uid, st_gid, st_rdev, 
                      st_atim, st_mtim, st_ctim, st_blksize, 
                      st_blocks):
    tmp = rodsStat_t()
    tmp.st_size = st_size
    tmp.st_dev = st_dev
    tmp.st_ino = st_ino
    tmp.st_mode = st_mode
    tmp.st_nlink = st_nlink
    tmp.st_uid = st_uid
    tmp.st_gid = st_gid
    tmp.st_rdev = st_rdev
    tmp.st_atim = st_atim
    tmp.st_mtim = st_mtim
    tmp.st_ctim = st_ctim
    tmp.st_blksize = st_blksize
    tmp.st_blocks = st_blocks
    return tmp

def create_ruleExecDelInp_t(ruleExecId):
    tmp = ruleExecDelInp_t()
    tmp.ruleExecId = ruleExecId
    return tmp

def create_ruleExecModInp_t(ruleId, condInput):
    tmp = ruleExecModInp_t()
    tmp.ruleId = ruleId
    tmp.condInput = condInput
    return tmp

def create_ruleExecSubmitInp_t(ruleName, reiFilePath, userName, exeAddress, 
                               exeTime, exeFrequency, priority, lastExecTime, 
                               exeStatus, estimateExeTime, notificationAddr, 
                               condInput, packedReiAndArgBBuf, ruleExecId):
    tmp = ruleExecSubmitInp_t()
    tmp.ruleName = ruleName
    tmp.reiFilePath = reiFilePath
    tmp.userName = userName
    tmp.exeAddress = exeAddress
    tmp.exeTime = exeTime
    tmp.exeFrequency = exeFrequency
    tmp.priority = priority
    tmp.lastExecTime = lastExecTime
    tmp.exeStatus = exeStatus
    tmp.estimateExeTime = estimateExeTime
    tmp.notificationAddr = notificationAddr
    tmp.condInput = condInput
    tmp.packedReiAndArgBBuf = packedReiAndArgBBuf
    tmp.ruleExecId = ruleExecId
    return tmp

def create_sendXmsgInp_t(ticket, sendAddr, #sendXmsgInfo
                         ):
    tmp = sendXmsgInp_t()
    tmp.ticket = ticket
    tmp.sendAddr = sendAddr
    #tmp.sendXmsgInfo = sendXmsgInfo
    return tmp

def create_simpleQueryInp_t(sql, arg1, arg2, arg3, arg4, control, form, 
                            maxBufSize):
    tmp = simpleQueryInp_t()
    tmp.sql = sql
    tmp.arg1 = arg1
    tmp.arg2 = arg2
    tmp.arg3 = arg3
    tmp.arg4 = arg4
    tmp.control = control
    tmp.form = form
    tmp.maxBufSize = maxBufSize
    return tmp

def create_simpleQueryOut_t(control, outBuf):
    tmp = simpleQueryOut_t()
    tmp.control = control
    tmp.outBuf = outBuf
    return tmp


def create_specColl_t(#collClass, 
                      #type, 
                      collection, objPath, resource, phyPath, 
                      cacheDir, cacheDirty, replNum):
    tmp = specColl_t()
    #tmp.collClass = collClass
    #tmp.type = type
    tmp.collection = collection
    tmp.objPath = objPath
    tmp.resource = resource
    tmp.phyPath = phyPath
    tmp.cacheDir = cacheDir
    tmp.cacheDirty = cacheDirty
    tmp.replNum = replNum
    return tmp

def create_sqlResult_t(attriInx, len, value):
    tmp = sqlResult_t()
    tmp.attriInx = attriInx
    tmp.len = len
    tmp.value = value
    return tmp

def create_structFileExtAndRegInp_t(objPath, collection, oprType, flags, 
                                    condInput):
    tmp = structFileExtAndRegInp_t()
    tmp.objPath = objPath
    tmp.collection = collection
    tmp.oprType = oprType
    tmp.flags = flags
    tmp.condInput = condInput
    return tmp

def create_structFileOprInp_t(addr, oprType, flags, specColl, condInput):
    tmp = structFileOprInp_t()
    tmp.addr = addr
    tmp.oprType = oprType
    tmp.flags = flags
    tmp.specColl = specColl
    tmp.condInput = condInput
    return tmp

def create_subFile_t(addr, subFilePath, mode, flags, offset, specColl):
    tmp = subFile_t()
    tmp.addr = addr
    tmp.subFilePath = subFilePath
    tmp.mode = mode
    tmp.flags = flags
    tmp.offset = offset
    tmp.specColl = specColl
    return tmp

def create_subStructFileFdOprInp_t(addr, #type, 
                                   fd, len):
    tmp = subStructFileFdOprInp_t()
    tmp.addr = addr
    #tmp.type = type
    tmp.fd = fd
    tmp.len = len
    return tmp

def create_subStructFileLseekInp_t(addr, #type, 
                                   fd, offset, whence):
    tmp = subStructFileLseekInp_t()
    tmp.addr = addr
    #tmp.type = type
    tmp.fd = fd
    tmp.offset = offset
    tmp.whence = whence
    return tmp

def create_subStructFileRenameInp_t(subFile, newSubFilePath):
    tmp = subStructFileRenameInp_t()
    tmp.subFile = subFile
    tmp.newSubFilePath = newSubFilePath
    return tmp

def create_unregDataObj_t(dataObjInfo, condInput):
    tmp = unregDataObj_t()
    tmp.dataObjInfo = dataObjInfo
    tmp.condInput = condInput
    return tmp

def create_userAdminInp_t(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, 
                          arg8, arg9):
    tmp = userAdminInp_t()
    tmp.arg0 = arg0
    tmp.arg1 = arg1
    tmp.arg2 = arg2
    tmp.arg3 = arg3
    tmp.arg4 = arg4
    tmp.arg5 = arg5
    tmp.arg6 = arg6
    tmp.arg7 = arg7
    tmp.arg8 = arg8
    tmp.arg9 = arg9
    return tmp

def create_userInfo_t(userName, rodsZone, userType, sysUid, authInfo, 
                      userOtherInfo):
    tmp = userInfo_t()
    tmp.userName = userName
    tmp.rodsZone = rodsZone
    tmp.userType = userType
    tmp.sysUid = sysUid
    tmp.authInfo = authInfo
    tmp.userOtherInfo = userOtherInfo
    return tmp

def create_userOtherInfo_t(userInfo, userComments, userCreate, userModify):
    tmp = userOtherInfo_t()
    tmp.userInfo = userInfo
    tmp.userComments = userComments
    tmp.userCreate = userCreate
    tmp.userModify = userModify
    return tmp

def create_version_t(status, relVersion, apiVersion, reconnPort, reconnAddr, 
                     cookie):
    tmp = version_t()
    tmp.status = status
    tmp.relVersion = relVersion
    tmp.apiVersion = apiVersion
    tmp.reconnPort = reconnPort
    tmp.reconnAddr = reconnAddr
    tmp.cookie = cookie
    return tmp

def create_xmsgTicketInfo_t(sendTicket, rcvTicket, expireTime, flag):
    tmp = xmsgTicketInfo_t()
    tmp.sendTicket = sendTicket
    tmp.rcvTicket = rcvTicket
    tmp.expireTime = expireTime
    tmp.flag = flag
    return tmp
