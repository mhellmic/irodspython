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
#include "generalUpdate.h"
#include "querySpecColl.h"
#include "rodsGenQuery.h"
#include "simpleQuery.h"
%}


/*****************************************************************************/

typedef struct GeneralUpdateInp {
   int type;
   inxValPair_t values;
} generalUpdateInp_t;

typedef struct GenQueryInp {
    int maxRows; 
    int continueInx; 
    int rowOffset;
    int options;
    keyValPair_t condInput;
    inxIvalPair_t selectInp; 
    inxValPair_t sqlCondInp; 
} genQueryInp_t;

typedef struct GenQueryOut {
    int rowCnt;
    int attriCnt;
    int continueInx;
    int totalRowCount; 
    sqlResult_t sqlResult[MAX_SQL_ATTR]; 
} genQueryOut_t; 

%extend genQueryOut_t {

    void release() {
        freeGenQueryOut(&$self);
    }

    PyObject * getSqlResult() {
  		int i;
  		PyObject *l = PyList_New($self->rowCnt);
 		for (i = 0; i < $self->rowCnt; i++) {
      		PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&$self->sqlResult[i]), SWIGTYPE_p_SqlResult, 0 |  0 );
    		PyList_SetItem(l, i, o);
  		}
   		return l;
    }
        
    PyObject * getSqlResultIdx(int idx) {
    	if ($self->attriCnt == 1) {
			char *tResult;
			tResult = $self->sqlResult[0].value;
			tResult += idx * $self->sqlResult[0].len;
			return Py_BuildValue("s", tResult);
		} else {
			int a;
			PyObject *tuple = PyTuple_New($self->attriCnt);
    		for ( a = 0 ; a < $self->attriCnt ; a++ ) {
				char *tResult;
				tResult = $self->sqlResult[a].value;
				tResult += idx * $self->sqlResult[a].len;
				
				PyTuple_SetItem(tuple, a, Py_BuildValue("s", tResult));
			}    	
			return tuple;
		}
    }    
    
    
    PyObject * getSqlResultByInxIdx(int inx, int idx) {
		sqlResult_t *rescName = getSqlResultByInx($self, inx);
		char *tResult;
		tResult = rescName[0].value;
		tResult += idx * rescName[0].len;
		return Py_BuildValue("s", tResult);
    }

}

typedef struct {
   char *sql;
   char *arg1;
   char *arg2;
   char *arg3;
   char *arg4;
   int control;
   int form;   
   int maxBufSize;
} simpleQueryInp_t;

typedef struct {
   int control;
   char *outBuf;
} simpleQueryOut_t;

typedef struct SqlResult {
    int attriInx;
    int len;
    char *value;
} sqlResult_t;

/*****************************************************************************/

int rcGeneralUpdate (rcComm_t *conn, generalUpdateInp_t *generalUpdateInp);

/*****************************************************************************/

%inline %{
genQueryOut_t * rcGenQuery(rcComm_t *conn, genQueryInp_t *genQueryInp) {
    genQueryOut_t *genQueryOut = NULL;
    rcGenQuery(conn, genQueryInp, &genQueryOut);
    return genQueryOut;
}
%}

/*****************************************************************************/

%inline %{
genQueryOut_t * rcQuerySpecColl(rcComm_t *conn, dataObjInp_t *querySpecCollInp) {
    genQueryOut_t *genQueryOut = NULL;
    rcQuerySpecColl(conn, querySpecCollInp, &genQueryOut);
    return genQueryOut;
}
%}

/*****************************************************************************/

%inline %{
simpleQueryOut_t * rcSimpleQuery(rcComm_t *conn, simpleQueryInp_t *simpleQueryInp) {
    simpleQueryOut_t *simpleQueryOut = NULL;
    rcSimpleQuery(conn, simpleQueryInp, &simpleQueryOut);
    return simpleQueryOut;
}
%}

/*****************************************************************************/
