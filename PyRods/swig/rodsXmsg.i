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
#include "getXmsgTicket.h"
#include "rcvXmsg.h"
#include "sendXmsg.h"
%}

/*****************************************************************************/

#define SINGLE_MSG_TICKET  0
#define MULTI_MSG_TICKET   1

typedef struct {
    unsigned int expireTime;
    unsigned int flag;
} getXmsgTicketInp_t;

typedef struct RcvXmsgInp {
    unsigned int rcvTicket;
    unsigned int msgNumber;
    unsigned int seqNumber;
    char msgCondition[MAX_NAME_LEN];
} rcvXmsgInp_t;

typedef struct RcvXmsgOut {
    char msgType[HEADER_TYPE_LEN];
    char sendUserName[NAME_LEN];
    char sendAddr[NAME_LEN];
    unsigned int msgNumber;
    unsigned int seqNumber;
    char *msg;
} rcvXmsgOut_t;

typedef struct XmsgTicketInfo {
    unsigned int sendTicket;
    unsigned int rcvTicket;
    unsigned int expireTime;
    unsigned int flag;
} xmsgTicketInfo_t;

typedef struct {
    xmsgTicketInfo_t ticket;
    char sendAddr[NAME_LEN];
    sendXmsgInfo_t sendXmsgInfo;
} sendXmsgInp_t;

/*****************************************************************************/

%inline %{
xmsgTicketInfo_t * rcGetXmsgTicket (rcComm_t *conn, getXmsgTicketInp_t *getXmsgTicketInp) {
    xmsgTicketInfo_t * outXmsgTicketInfo = NULL;
    int status = rcGetXmsgTicket(conn, getXmsgTicketInp, &outXmsgTicketInfo);
    if (status == 0)
        return outXmsgTicketInfo;
    else
        return NULL;
}
%}

/*****************************************************************************/

%inline %{
rcvXmsgOut_t * rcRcvXmsg (rcComm_t *conn, rcvXmsgInp_t *rcvXmsgInp) {
    rcvXmsgOut_t * rcvXmsgOut = NULL;
    int status = rcRcvXmsg(conn, rcvXmsgInp, &rcvXmsgOut);
    if (status == 0)
        return rcvXmsgOut;
    else
        return NULL;
}
%}

/*****************************************************************************/

int rcSendXmsg (rcComm_t *conn, sendXmsgInp_t *sendXmsgInp);

/*****************************************************************************/