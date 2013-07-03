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
#include "getRodsEnv.h"
%}

/*****************************************************************************/

typedef struct {
   char rodsUserName[NAME_LEN];
   char rodsHost[NAME_LEN];
   int  rodsPort;
   char xmsgHost[NAME_LEN];
   int  xmsgPort;
   char rodsHome[MAX_NAME_LEN];
   char rodsCwd[MAX_NAME_LEN];
   char rodsAuthScheme[NAME_LEN];
   char rodsDefResource[NAME_LEN];
   char rodsZone[NAME_LEN];
   char *rodsServerDn;
   int rodsLogLevel;
   char rodsAuthFileName[LONG_NAME_LEN];
   char rodsDebug[NAME_LEN];
} rodsEnv;

/*****************************************************************************/

int appendRodsEnv(char *appendText);

/*****************************************************************************/

int getRodsEnv(rodsEnv *rodsEnvArg);

%pythoncode %{
def getRodsEnv():
    rodsEnvArg = rodsEnv()
    status = _irods.getRodsEnv(rodsEnvArg)
    return (status, rodsEnvArg)
%}

/*****************************************************************************/

char *getRodsEnvAuthFileName();

/*****************************************************************************/

char *getRodsEnvFileName();

/*****************************************************************************/
