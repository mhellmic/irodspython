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
#include "modAVUMetadata.h"
#include "modDataObjMeta.h"
%}

/*****************************************************************************/

typedef struct {
    dataObjInfo_t *dataObjInfo;
    keyValPair_t *regParam;
} modDataObjMeta_t;

typedef struct {
   char *arg0;
   char *arg1;
   char *arg2;
   char *arg3;
   char *arg4;
   char *arg5;
   char *arg6;
   char *arg7;
   char *arg8;
   char *arg9;
} modAVUMetadataInp_t;

/*****************************************************************************/

int clearModAVUMetadataInp (modAVUMetadataInp_t *modAVUMetadataInp);

/*****************************************************************************/

int clearModDataObjMetaInp (modDataObjMeta_t *modDataObjMetaInp);

/*****************************************************************************/

int rcModAVUMetadata (rcComm_t *conn, modAVUMetadataInp_t *modAVUMetadataInp);

/*****************************************************************************/

int rcModDataObjMeta (rcComm_t *conn, modDataObjMeta_t *modDataObjMetaInp);

/*****************************************************************************/
