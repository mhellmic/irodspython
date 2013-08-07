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

%{
#include "execMyRule.h"
#include "ruleExecDel.h"
#include "ruleExecMod.h"
#include "ruleExecSubmit.h"
%}

/*****************************************************************************/

typedef struct ExecCmd {
    char cmd[LONG_NAME_LEN];
    char cmdArgv[HUGE_NAME_LEN];
    char execAddr[LONG_NAME_LEN];
    char hintPath[MAX_NAME_LEN];
    int addPathToArgv;
    int dummy;
    keyValPair_t condInput;
} execCmd_t;

typedef struct ExecCmdOut {
    bytesBuf_t stdoutBuf;
    bytesBuf_t stderrBuf;
    int status;
} execCmdOut_t;

typedef struct ExecMyRuleInp {
    char myRule[META_STR_LEN];
    rodsHostAddr_t addr;
    keyValPair_t condInput;
    char outParamDesc[LONG_NAME_LEN];  
    msParamArray_t *inpParamArray;
} execMyRuleInp_t;

typedef struct {
    char ruleExecId[NAME_LEN];  
} ruleExecDelInp_t;

typedef struct {
   char ruleId[NAME_LEN];
   keyValPair_t condInput;
} ruleExecModInp_t;

typedef struct {
    char ruleName[META_STR_LEN];
    char reiFilePath[MAX_NAME_LEN];
    char userName[NAME_LEN];
    char exeAddress[NAME_LEN];
    char exeTime[TIME_LEN];
    char exeFrequency[NAME_LEN];
    char priority[NAME_LEN];
    char lastExecTime[NAME_LEN];
    char exeStatus[NAME_LEN];
    char estimateExeTime[NAME_LEN];
    char notificationAddr[NAME_LEN];
    keyValPair_t condInput;
    bytesBuf_t *packedReiAndArgBBuf;
    char ruleExecId[NAME_LEN];
} ruleExecSubmitInp_t;

/*****************************************************************************/

%inline %{
PyObject * rcExecCmd(rcComm_t *conn, execCmd_t *execCmdInp) {
    execCmdOut_t *execCmdOut = NULL;
    int status = rcExecCmd(conn, execCmdInp, &execCmdOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(execCmdOut), 
                                            SWIGTYPE_p_ExecCmdOut, 0 |  0 ));
}
%}

/*****************************************************************************/

%inline %{
PyObject * rcExecMyRule(rcComm_t *conn, execMyRuleInp_t *execMyRuleInp) {
    msParamArray_t *outParamArray = NULL;
    int status = rcExecMyRule(conn, execMyRuleInp, &outParamArray);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(outParamArray), 
                                            SWIGTYPE_p_MsParamArray, 0 |  0 ));
}
%}

/*****************************************************************************/

int rcRuleExecDel (rcComm_t *conn, ruleExecDelInp_t *ruleExecDelInp);

/*****************************************************************************/

int rcRuleExecMod (rcComm_t *conn, ruleExecModInp_t *ruleExecModInp);

/*****************************************************************************/

int rcRuleExecSubmit (rcComm_t *conn, ruleExecSubmitInp_t *ruleExecSubmitInp,
char **ruleExecId);

/*****************************************************************************/
