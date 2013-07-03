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

/*****************************************************************************/

typedef struct {
    irodsProt_t irodsProt;
    char host[NAME_LEN];
    int sock;
    int portNum;
    int loggedIn;
    struct sockaddr_in  localAddr;
    struct sockaddr_in  remoteAddr;
    userInfo_t proxyUser;
    userInfo_t clientUser;
    version_t *svrVersion;
    rError_t *rError;
    int flag;
    transferStat_t transStat;
    int apiInx;
    int status;
    int windowSize;
    int reconnectedSock;
    time_t reconnTime;
#ifdef USE_BOOST
    volatile bool exit_flg;
    boost::thread*              reconnThr;
    boost::mutex*               lock;
    boost::condition_variable*  cond;
#else
#ifndef windows_platform
    pthread_t reconnThr;
    pthread_mutex_t lock;
    pthread_cond_t cond;
#endif
#endif
    procState_t agentState;
    procState_t clientState;
    procState_t reconnThrState;
    operProgress_t operProgress;
    fileRestart_t fileRestart;
#ifdef USE_SSL
    int ssl_on;
    SSL_CTX *ssl_ctx;
    SSL *ssl;
#endif
} rcComm_t;

%extend rcComm_t {

    int disconnect() {
        return rcDisconnect($self);
    }

}

/*****************************************************************************/

int clientLogin(rcComm_t *conn);

/*****************************************************************************/

int clientLoginWithPassword(rcComm_t *conn, char* password);

/*****************************************************************************/

%inline %{
int clientLoginWithObfPassword(rcComm_t *conn, char* obfPassword) {
    char password[MAX_PASSWORD_LEN+10];
    obfiDecode(obfPassword, password, 0);
    return clientLoginWithPassword(conn, password);
}
%}

/*****************************************************************************/

char * getSessionSignitureClientside();

/*****************************************************************************/

rcComm_t *
rcConnect (char *rodsHost, int rodsPort, char *userName, char *rodsZone,
int reconnFlag, rErrMsg_t *out_errMsg);

%pythoncode %{
def rcConnect(rodsHost, rodsPort, userName, rodsZone, reconnFlag=0):
    errMsg = rErrMsg_t()
    status = _irods.rcConnect(rodsHost, rodsPort, userName, rodsZone, reconnFlag, errMsg)
    return (status, errMsg)
%}

/*****************************************************************************/

int rcDisconnect (rcComm_t *conn);

/*****************************************************************************/