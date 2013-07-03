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
#include "authCheck.h"
#include "authRequest.h"
#include "authResponse.h"
#include "gsiAuthRequest.h"
%}

/*****************************************************************************/

#define CHALLENGE_LEN 64 /* 64 bytes of data and terminating null */
#define RESPONSE_LEN 16  /* 16 bytes of data and terminating null */

/*****************************************************************************/

typedef struct {
   char *challenge;
   char *response;
   char *username;
} authCheckInp_t;

typedef struct {
   int  privLevel;
   int  clientPrivLevel;
   char *serverResponse;
} authCheckOut_t;

typedef struct {
   char *response;
   char *username;
} authResponseInp_t;

typedef struct {
   char *challenge;
} authRequestOut_t;

typedef struct {
   char *serverDN;
} gsiAuthRequestOut_t;

/*****************************************************************************/

//int
//rcAuthCheck(rcComm_t *conn, authCheckInp_t *authCheckInp, 
//         authCheckOut_t **authCheckOut );
%inline %{
PyObject * rcAuthCheck(rcComm_t *conn, authCheckInp_t *authCheckInp) {
    authCheckOut_t *authCheckOut = NULL;
    int status = rcAuthCheck(conn, authCheckInp, &authCheckOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(authCheckOut), 
                                            SWIGTYPE_p_authCheckOut_t, 0 |  0 ));
}
%}

/*****************************************************************************/

//int
//rcAuthRequest(rcComm_t *conn, authRequestOut_t **authRequestOut );
%inline %{
PyObject * rcAuthRequest(rcComm_t *conn) {
    authRequestOut_t *authReqOut = NULL;
    int status = rcAuthRequest(conn, &authReqOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(authReqOut), 
                                            SWIGTYPE_p_authRequestOut_t, 0 |  0 ));
}
%}

/*****************************************************************************/

int rcAuthResponse(rcComm_t *conn, authResponseInp_t *authResponseInp );

/*****************************************************************************/

//int
//rcGsiAuthRequest (rcComm_t *conn, gsiAuthRequestOut_t **gsiAuthRequestOut );
%inline %{
PyObject * rcGsiAuthRequest(rcComm_t *conn) {
    gsiAuthRequestOut_t *gsiAuthRequestOut = NULL;
    int status = rcGsiAuthRequest(conn, &gsiAuthRequestOut);
    return Py_BuildValue("(iO)", 
                         status, 
                         SWIG_NewPointerObj(SWIG_as_voidptr(gsiAuthRequestOut), 
                                            SWIGTYPE_p_gsiAuthRequestOut_t, 0 |  0 ));
}
%}

/*****************************************************************************/
