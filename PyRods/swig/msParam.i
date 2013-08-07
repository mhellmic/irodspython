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


/* some commonly used MS (micro service) type */
#define STR_MS_T                "STR_PI"
#define INT_MS_T                "INT_PI"
#define INT16_MS_T              "INT16_PI"
#define CHAR_MS_T               "CHAR_PI"
#define BUF_LEN_MS_T            "BUF_LEN_PI"
#define STREAM_MS_T     "INT_PI"
#define DOUBLE_MS_T             "DOUBLE_PI"
#define FLOAT_MS_T              "FLOAT_PI"
#define BOOL_MS_T               "BOOL_PI"
#define DataObjInp_MS_T         "DataObjInp_PI"
#define DataObjCloseInp_MS_T    "DataObjCloseInp_PI"
#define DataObjCopyInp_MS_T     "DataObjCopyInp_PI"
#define DataObjReadInp_MS_T     "dataObjReadInp_PI"
#define DataObjWriteInp_MS_T    "dataObjWriteInp_PI"
#define DataObjLseekInp_MS_T    "fileLseekInp_PI"
#define DataObjLseekOut_MS_T    "fileLseekOut_PI"
#define KeyValPair_MS_T         "KeyValPair_PI"
#define TagStruct_MS_T          "TagStruct_PI"
#define CollInp_MS_T            "CollInpNew_PI"
#define ExecCmd_MS_T            "ExecCmd_PI"
#define ExecCmdOut_MS_T         "ExecCmdOut_PI"
#define RodsObjStat_MS_T        "RodsObjStat_PI"
#define VaultPathPolicy_MS_T    "VaultPathPolicy_PI"
#define StrArray_MS_T       "StrArray_PI"
#define IntArray_MS_T       "IntArray_PI"
#define GenQueryInp_MS_T    "GenQueryInp_PI"
#define GenQueryOut_MS_T    "GenQueryOut_PI"
#define XmsgTicketInfo_MS_T     "XmsgTicketInfo_PI"
#define SendXmsgInfo_MS_T       "SendXmsgInfo_PI"
#define GetXmsgTicketInp_MS_T   "GetXmsgTicketInp_PI"
#define SendXmsgInp_MS_T        "SendXmsgInp_PI"
#define RcvXmsgInp_MS_T         "RcvXmsgInp_PI"
#define RcvXmsgOut_MS_T         "RcvXmsgOut_PI"
#define StructFileExtAndRegInp_MS_T         "StructFileExtAndRegInp_PI"
#define RuleSet_MS_T "RuleSet_PI"
#define RuleStruct_MS_T         "RuleStruct_PI"
#define DVMapStruct_MS_T        "DVMapStruct_PI"
#define FNMapStruct_MS_T        "FNMapStruct_PI"
#define MsrvcStruct_MS_T         "MsrvcStruct_PI"
#define NcOpenInp_MS_T      "NcOpenInp_PI"
#define NcInqIdInp_MS_T     "NcInqIdInp_PI"
#define NcInqWithIdOut_MS_T "NcInqWithIdOut_PI"
#define NcInqInp_MS_T       "NcInqInp_PI"
#define NcInqOut_MS_T       "NcInqOut_PI"
#define NcCloseInp_MS_T     "NcCloseInp_PI"
#define NcGetVarInp_MS_T    "NcGetVarInp_PI"
#define NcGetVarOut_MS_T    "NcGetVarOut_PI"
#define NccfGetVarInp_MS_T  "NccfGetVarInp_PI"
#define NccfGetVarOut_MS_T  "NccfGetVarOut_PI"
#define NcInqOut_MS_T       "NcInqOut_PI"
#define NcInqGrpsOut_MS_T   "NcInqGrpsOut_PI"
#define Dictionary_MS_T     "Dictionary_PI"
#define DictArray_MS_T      "DictArray_PI"
#define GenArray_MS_T       "GenArray_PI"

#define RESC_NAME_FLAG      0x1
#define DEST_RESC_NAME_FLAG     0x2
#define BACKUP_RESC_NAME_FLAG   0x4
#define FORCE_FLAG_FLAG     0x8
#define ALL_FLAG        0x10
#define LOCAL_PATH_FLAG     0x20
#define VERIFY_CHKSUM_FLAG  0x40
#define IRODS_ADMIN_FLAG    0x80
#define UPDATE_REPL_FLAG    0x100
#define REPL_NUM_FLAG       0x200
#define DATA_TYPE_FLAG      0x400
#define CHKSUM_ALL_FLAG     0x800
#define FORCE_CHKSUM_FLAG   0x1000
#define FILE_PATH_FLAG      0x2000
#define CREATE_MODE_FLAG    0x4000
#define OPEN_FLAGS_FLAG     0x8000
#define COLL_FLAGS_FLAG     0x8000
#define DATA_SIZE_FLAGS     0x10000
#define NUM_THREADS_FLAG    0x20000
#define OPR_TYPE_FLAG       0x40000
#define OBJ_PATH_FLAG       0x80000
#define COLL_NAME_FLAG      0x80000
#define IRODS_RMTRASH_FLAG  0x100000
#define IRODS_ADMIN_RMTRASH_FLAG 0x200000
#define DEF_RESC_NAME_FLAG  0x400000
#define RBUDP_TRANSFER_FLAG     0x800000
#define RBUDP_SEND_RATE_FLAG    0x1000000
#define RBUDP_PACK_SIZE_FLAG    0x2000000
#define BULK_OPR_FLAG       0x4000000
#define UNREG_FLAG      0x8000000


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
