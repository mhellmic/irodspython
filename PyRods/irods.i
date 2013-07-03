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
 
%module irods
 
 
%pythoncode %{# Copyright (c) 2013, University of Liverpool
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
%}


%include cstring.i
%include templates.i

%include auth.i
%include chkObjPermAndStat.i
%include dataObj.i
%include getRodsEnv.i
%include md5.i
%include miscUtil.i
%include modAccessControl.i
%include msParam.i
%include obf.i
%include parseCommandLine.i
%include rcConnect.i
%include rcMisc.i
%include rodsAdmin.i
%include rodsDef.i
%include rodsError.i
%include rodsErrorTable.i
%include rodsExec.i
%include rodsFile.i
%include rodsInfo.i
%include rodsIO.i
%include rodsKeyWdDef.i
%include rodsLog.i
%include rodsMeta.i
%include rodsPath.i
%include rodsQuery.i
%include rodsStructFile.i
%include rodsUser.i
%include rodsXmsg.i
%include sqlMisc.i
%include stringOpr.i

