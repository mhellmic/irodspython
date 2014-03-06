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
#include "rodsDef.h"
%}


/*****************************************************************************/

typedef struct BytesBuf {
    int len;
    void *buf;
} bytesBuf_t;

%extend bytesBuf_t {
    
    void malloc(int size) {
        $self->buf = malloc(size);
    }
    
    ~BytesBuf() {
        if ($self->buf)	free($self->buf);
    }
    
    void setBuf(char * buf, int len) {
        $self->buf = malloc(len+1);
        memcpy($self->buf, buf, len);
        ((char*)$self->buf)[len] = 0;
        $self->len = len;
    }
    
    PyObject * getBuf() {
        PyObject * outString = PyString_FromStringAndSize((char *)$self->buf, 
                                                          $self->len);
        return outString;
    }
    
    char * getBufAsChar() {
        return (char *) $self->buf;
    }

}

typedef struct {
   char stringToHashWith[MAX_PASSWORD_LEN];
} getTempPasswordOut_t; 

typedef enum {
    UNKNOWN_ST,
    NOT_EXIST_ST,
    EXIST_ST
} objStat_t;

typedef enum {
    UNKNOWN_OBJ_T,
    DATA_OBJ_T,
    COLL_OBJ_T,
    UNKNOWN_FILE_T,
    LOCAL_FILE_T,
    LOCAL_DIR_T,
    NO_INPUT_T
} objType_t;

typedef struct rodsDirent {
        unsigned int    d_offset;
        unsigned int    d_ino;
        unsigned int    d_reclen;
        unsigned int    d_namlen;
        char            d_name[DIR_LEN];
} rodsDirent_t;

typedef struct {
    char hostAddr[LONG_NAME_LEN];
    char zoneName[NAME_LEN];
    int portNum;
    int dummyInt;
} rodsHostAddr_t;

typedef long long rodsLong_t;

typedef struct {
    char restartFile[MAX_NAME_LEN];
    int fd;
    int doneCnt;
    char collection[MAX_NAME_LEN];
    char lastDonePath[MAX_NAME_LEN];
    char oprType[NAME_LEN];
    int curCnt;
    int restartState;
} rodsRestart_t; 

typedef struct rodsStat {
    rodsLong_t          st_size;
    unsigned int        st_dev;
    unsigned int        st_ino;
    unsigned int        st_mode;
    unsigned int        st_nlink;
    unsigned int        st_uid;
    unsigned int        st_gid;
    unsigned int        st_rdev;
    unsigned int        st_atim;
    unsigned int        st_mtim;
    unsigned int        st_ctim;
    unsigned int        st_blksize;
    unsigned int        st_blocks;
} rodsStat_t;

typedef struct {
    int status; 
    char relVersion[NAME_LEN];
    char apiVersion[NAME_LEN];
    int reconnPort;
    char reconnAddr[LONG_NAME_LEN];
    int cookie;
} version_t;

/*****************************************************************************/
