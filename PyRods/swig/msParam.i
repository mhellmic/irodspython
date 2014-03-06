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

%extend msParam_t {

    execCmdOut_t * getInOutAsExecCmdOut() {
        return (execCmdOut_t *) $self->inOutStruct;
    }

    char * getInOutAsChar() {
        return (char *) $self->inOutStruct;
    }

    int getInOutAsInt() {
        return *(int *) $self->inOutStruct;
    }

    double getInOutAsDouble() {
        return *(double *) $self->inOutStruct;
    }

    keyValPair_t * getInOutAsKeyValPair() {
        return (keyValPair_t *) $self->inOutStruct;
    }

    tagStruct_t * getInOutAsTagStruct() {
        return (tagStruct_t *) $self->inOutStruct;
    }

}

typedef struct MsParamArray {
    int len;
    int oprType;
    msParam_t **msParam;
} msParamArray_t;


%extend msParamArray_t {

    msParam_t * getMsParam(int n) {
        if ( (n >=0) && (n < $self->len) )
            return $self->msParam[n];
        else
            return NULL;
    }

}

/*****************************************************************************/

int addMsParamToArray (msParamArray_t *msParamArray, char *label,
char *type, void *inOutStruct, bytesBuf_t *inpOutBuf, int replFlag);

%inline %{

int addCharParamToArray(msParamArray_t *msParamArray, char *label,
                          char *inOutStruct) {
    return addMsParamToArray(msParamArray, label, (char *) STR_MS_T, 
                     (void *) strdup ((char *)inOutStruct), NULL, 0);
}

int addDoubleParamToArray(msParamArray_t *msParamArray, char *label,
                          double inpDouble) {
    double *myDouble;
    int status;

    myDouble = (double *)malloc (sizeof (double));
    *myDouble = inpDouble;
    status = addMsParamToArray(msParamArray, label, (char *) DOUBLE_MS_T, 
                              myDouble, NULL, 0);
    return status;
}

int addKeyValParamToArray(msParamArray_t *msParamArray, char *label,
                          keyValPair_t * keyVal) {
    return addMsParamToArray(msParamArray, label, (char *) KeyValPair_MS_T, 
                              keyVal, NULL, 0);
}

int addTagStructParamToArray(msParamArray_t *msParamArray, char *label,
                             tagStruct_t * tagStruct) {
    return addMsParamToArray(msParamArray, label, (char *) TagStruct_MS_T, 
                              tagStruct, NULL, 0);
}

%}

/*****************************************************************************/

int
addIntParamToArray (msParamArray_t *msParamArray, char *label, int inpInt);

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

msParam_t * getMsParamByLabel(msParamArray_t *msParamArray, char *label);

/*****************************************************************************/

msParam_t * getMsParamByType(msParamArray_t *msParamArray, char *type);

/*****************************************************************************/

int parseMspForFloat (msParam_t *inpParam, float *floatout);

/*****************************************************************************/

int parseMspForPosInt (msParam_t *inpParam);

/*****************************************************************************/

char * parseMspForStr (msParam_t *inpParam);

/*****************************************************************************/
