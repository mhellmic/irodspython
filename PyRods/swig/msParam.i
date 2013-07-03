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

typedef struct MsParam {
    char *label;
    char *type;
    void *inOutStruct;
    bytesBuf_t *inpOutBuf;
} msParam_t;

typedef struct MsParamArray {
    int len;
    int oprType;
    msParam_t **msParam;
} msParamArray_t;

/*****************************************************************************/

int addMsParamToArray (msParamArray_t *msParamArray, char *label,
char *type, void *inOutStruct, bytesBuf_t *inpOutBuf, int replFlag);

/*****************************************************************************/

int fillBufLenInMsParam (msParam_t *msParam, int myInt, bytesBuf_t *bytesBuf);

/*****************************************************************************/

int fillCharInMsParam (msParam_t *msParam, char myChar);

/*****************************************************************************/

int fillDoubleInMsParam (msParam_t *msParam, rodsLong_t myDouble);

/*****************************************************************************/

int fillFloatInMsParam (msParam_t *msParam, float myFloat);

/*****************************************************************************/

int  fillIntInMsParam (msParam_t *msParam, int myInt);

/*****************************************************************************/

int fillStrInMsParam (msParam_t *msParam, char *myStr);

/*****************************************************************************/

msParam_t * getMsParamByLabel (msParamArray_t *msParamArray, char *label);

/*****************************************************************************/

int parseMspForFloat (msParam_t *inpParam, float *floatout);

/*****************************************************************************/

int parseMspForPosInt (msParam_t *inpParam);

/*****************************************************************************/

char * parseMspForStr (msParam_t *inpParam);

/*****************************************************************************/
