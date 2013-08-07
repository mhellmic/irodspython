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
#include "getMiscSvrInfo.h"
#include "objStat.h"
%}

/*****************************************************************************/

typedef struct DataObjInfo {
    char objPath[MAX_NAME_LEN];
    char rescName[NAME_LEN];
    char rescGroupName[NAME_LEN];
    char dataType[NAME_LEN];
    rodsLong_t dataSize;
    char chksum[NAME_LEN];
    char version[NAME_LEN];
    char filePath[MAX_NAME_LEN];
    rescInfo_t *rescInfo;
    char dataOwnerName[NAME_LEN];
    char dataOwnerZone[NAME_LEN];
    int  replNum;
    int  replStatus;
    char statusString[NAME_LEN];
    rodsLong_t  dataId;
    rodsLong_t  collId;
    int  dataMapId;
    int flags;
    char dataComments[LONG_NAME_LEN];
    char dataMode[SHORT_STR_LEN];
    char dataExpiry[TIME_LEN];
    char dataCreate[TIME_LEN];
    char dataModify[TIME_LEN];
    char dataAccess[NAME_LEN];
    int  dataAccessInx;
    int  writeFlag;
    char destRescName[NAME_LEN];
    char backupRescName[NAME_LEN];
    char subPath[MAX_NAME_LEN];
    specColl_t *specColl;
    int regUid;
    int otherFlags;
    keyValPair_t condInput;
    struct DataObjInfo *next;
} dataObjInfo_t;

typedef struct MiscSvrInfo {
    int serverType;
    unsigned int serverBootTime;
    char relVersion[NAME_LEN];
    char apiVersion[NAME_LEN];
    char rodsZone[NAME_LEN];
} miscSvrInfo_t;

typedef struct rodsObjStat {
    rodsLong_t          objSize;
    objType_t           objType;
    unsigned int        dataMode;
    char                dataId[NAME_LEN];
    char                chksum[NAME_LEN];
    char                ownerName[NAME_LEN];
    char                ownerZone[NAME_LEN];
    char                createTime[TIME_LEN];
    char                modifyTime[TIME_LEN];
    specColl_t          *specColl;
} rodsObjStat_t;

%ignore TagStruct::preTag;
%ignore TagStruct::postTag;
%ignore TagStruct::keyWord;

typedef struct TagStruct {
    int len;
    char **preTag;
    char **postTag;
    char **keyWord;
} tagStruct_t;


%extend tagStruct_t {
    
    char ** getPreTag(size_t *len) {
        *len = $self->len;
        return $self->preTag;
    }
    
    char * getPreTag(int n) {
        if ( (n >=0) && (n < $self->len) ) {
            char * tag = $self->preTag[n];
            return tag;
        } else
            return NULL;
    }

    char * getPostTag(int n) {
        if ( (n >=0) && (n < $self->len) )
            return $self->postTag[n];
        else
            return NULL;
    }
    
    char ** getPostTag(size_t *len) {
        *len = $self->len;
        return $self->postTag;
    }
    
    char ** getKeyWord(size_t *len) {
        *len = $self->len;
        return $self->keyWord;
    }

    char * getKeyWord(int n) {
        if ( (n >=0) && (n < $self->len) )
            return $self->keyWord[n];
        else
            return NULL;
    }

}

typedef struct SpecColl {
    specCollClass_t collClass;
    structFileType_t type;
    char collection[MAX_NAME_LEN];
    char objPath[MAX_NAME_LEN];
    char resource[NAME_LEN];
    char phyPath[MAX_NAME_LEN];
    char cacheDir[MAX_NAME_LEN];
    int cacheDirty; 
    int replNum;
} specColl_t;

typedef struct Subfile {
    rodsHostAddr_t addr;
    char subFilePath[MAX_NAME_LEN];
    int mode;
    int flags;
    rodsLong_t offset;
    specColl_t *specColl;
} subFile_t;

/*****************************************************************************/

%ignore KeyValPair::keyWord;
%ignore KeyValPair::value;

typedef struct KeyValPair {
    int len;
    char **keyWord;
    char **value;
} keyValPair_t;

%extend keyValPair_t {
  
    void init(char **keyWord, char **value, int len) { 
        int i;
        
        $self->keyWord = (char **) malloc((len+1)*sizeof(char*));
        $self->value = (char **) malloc((len+1)*sizeof(char*));
            
        for (i = 0 ; i < len ; i++) { 
            size_t size = (strlen(keyWord[i])+1)*sizeof(char);
            $self->keyWord[i] = (char *) malloc(size);
            strcpy($self->keyWord[i], keyWord[i]);
            
            size = (strlen(value[i])+1)*sizeof(char);
            $self->value[i] = (char *) malloc(size);
            strcpy($self->value[i], value[i]);
        }
        $self->keyWord[len] = 0;
        $self->value[len] = 0;
        $self->len = len;
    }
    
    int getLen() {
        return $self->len;
    }
    
    char ** getKeyWord(size_t *len) {
        *len = $self->len;
        return $self->keyWord;
    }
    
    char * getKeyWord(int n) {
        if ( (n >=0) && (n < $self->len) )
            return $self->keyWord[n];
        else
            return NULL;
    }
    
    char ** getValue(size_t *len) {
        *len = $self->len;
        return $self->value;
    }
    
    char * getValue(int n) {
        if ( (n >=0) && (n < $self->len) )
            return $self->value[n];
        else
            return NULL;
    }
    
    char * __str__() {
        char * str = (char *)malloc(1024 * sizeof(char));
        strcpy (str,"keyValPair_t:\n");
        for (int i = 0 ; i < $self->len ; i ++) {
            char tmp[1024];
            sprintf(tmp, " %s - %s\n", $self->keyWord[i], $self->value[i]); 
            strcat(str, tmp);
        }
        return str;
    }

}

/*****************************************************************************/

%ignore InxIvalPair::inx;
%ignore InxIvalPair::value;

typedef struct InxIvalPair {
    int len;
    int *inx;
    int *value;
} inxIvalPair_t;

%extend inxIvalPair_t {
   
    void init(int *inx, int *value, int len) { 
        int i;
        
        $self->inx = (int *) malloc((len+1)*sizeof(int));
        $self->value = (int *) malloc((len+1)*sizeof(int));
            
        for (i = 0 ; i < len ; i++) {
            $self->inx[i] = inx[i];
            $self->value[i] = value[i];
                    
        }
        $self->inx[len] = 0;
        $self->value[len] = 0;
        $self->len = len;
   }
    
   int getLen() {
        return $self->len;
   }
    
   int * getInx(size_t *len) {
        *len = $self->len;
        return $self->inx;
   }
    
    int * getValue(size_t *len) {
        *len = $self->len;
        return $self->value;
    }
 
    char * __str__() {
        char * str = (char *)malloc(1024 * sizeof(char));
        strcpy (str,"inxIvalPair_t:\n");
        for (int i = 0 ; i < $self->len ; i ++) {
            char tmp[1024];
            sprintf(tmp, " %d - %d\n", $self->inx[i], $self->value[i]); 
            strcat(str, tmp);
        }
        return str;
    }

}

/*****************************************************************************/

%ignore InxValPair::inx;
%ignore InxValPair::value;

typedef struct InxValPair {
    int len;
    int *inx;
    char **value;
} inxValPair_t;

%extend inxValPair_t {
  
    void init(int *inx, char **value, int len) {
        $self->inx = (int *) malloc((len+1)*sizeof(int));
        $self->value = (char **) malloc((len+1)*sizeof(char*));
            
        for (int i = 0 ; i < len ; i++) { 
            size_t size = (strlen(value[i])+1)*sizeof(char);
            $self->value[i] = (char *) malloc(size);
            strcpy($self->value[i], value[i]);
            
            $self->inx[i] = inx[i];
        }
        $self->inx[len] = 0;
        $self->value[len] = 0;
        $self->len = len;
    }
    
   int getLen() {
        return $self->len;
   }
    
   int * getInx(size_t *len) {
        *len = $self->len;
        return $self->inx;
   }
    
    char ** getValue(size_t *len) {
        *len = $self->len;
        return $self->value;
    }
 
    char * __str__() {
        char * str = (char *)malloc(1024 * sizeof(char));
        strcpy (str,"inxValPair_t:\n");
        for (int i = 0 ; i < $self->len ; i ++) {
            char tmp[1024];
            sprintf(tmp, " %d - %s\n", $self->inx[i], $self->value[i]); 
            strcat(str, tmp);
        }
        return str;
    }

}

/*****************************************************************************/

%inline %{
miscSvrInfo_t * rcGetMiscSvrInfo(rcComm_t *conn) {
    miscSvrInfo_t * outSvrInfo = NULL;
    rcGetMiscSvrInfo(conn, &outSvrInfo);
    return outSvrInfo;
}
%}

/*****************************************************************************/

%inline %{
rodsObjStat_t * rcObjStat(rcComm_t *conn, dataObjInp_t *dataObjInp) {
    rodsObjStat_t * rodsObjStatOut = NULL;
    rcObjStat(conn, dataObjInp, &rodsObjStatOut);
    return rodsObjStatOut;
}
%}

/*****************************************************************************/