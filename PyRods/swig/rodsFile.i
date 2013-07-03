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
#include "fileChmod.h"
#include "fileChksum.h"
#include "fileClose.h"
#include "fileClosedir.h"
#include "fileCreate.h"
#include "fileFstat.h"
#include "fileFsync.h"
#include "fileGet.h"
#include "fileGetFsFreeSpace.h"
#include "fileLseek.h"
#include "fileMkdir.h"
#include "fileOpen.h"
#include "fileOpendir.h"
#include "filePut.h"
#include "fileRead.h"
#include "fileReaddir.h"
#include "fileRename.h"
#include "fileRmdir.h"
#include "fileOpen.h"
#include "fileStage.h"
#include "fileStat.h"
#include "fileTruncate.h"
#include "fileUnlink.h"
#include "fileWrite.h"
#include "l3FileGetSingleBuf.h"
#include "l3FilePutSingleBuf.h"
%}

/*****************************************************************************/

#define NO_CHK_PERM_FLAG    0x1
#define UNIQUE_REM_COMM_FLAG    0x2
#define FORCE_FLAG      0x4
#define RMDIR_RECUR 0x1

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char fileName[MAX_NAME_LEN];
    int mode;
} fileChmodInp_t;

typedef struct FileChksumInp {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char fileName[MAX_NAME_LEN];
    int flag;
} fileChksumInp_t;

typedef struct FileCloseInp {
    int fileInx;
} fileCloseInp_t;

typedef struct {
    int fileInx;
} fileClosedirInp_t;

typedef fileOpenInp_t fileCreateInp_t;

typedef struct {
    int fileInx;
} fileFstatInp_t;

typedef struct {
    int fileInx;
} fileFsyncInp_t;

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char fileName[MAX_NAME_LEN];
    int flag;
} fileGetFsFreeSpaceInp_t;
    
typedef struct {
    rodsLong_t size;
} fileGetFsFreeSpaceOut_t;

typedef struct FileLseekInp {
    int fileInx;
    rodsLong_t offset; 
    int whence;
} fileLseekInp_t;

typedef struct FileLseekOut {
    rodsLong_t offset; 
} fileLseekOut_t;

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char dirName[MAX_NAME_LEN];
    int mode;
    keyValPair_t condInput;
} fileMkdirInp_t;

typedef struct {
    fileDriverType_t fileType;
    int otherFlags;
    rodsHostAddr_t addr;
    char fileName[MAX_NAME_LEN];
    int flags;
    int mode;
    rodsLong_t dataSize;
    keyValPair_t condInput;
} fileOpenInp_t;

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char dirName[MAX_NAME_LEN];
} fileOpendirInp_t;

typedef struct FileReadInp {
    int fileInx;
    int len;
} fileReadInp_t;

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char oldFileName[MAX_NAME_LEN];
    char newFileName[MAX_NAME_LEN];
} fileRenameInp_t;

typedef struct {
    fileDriverType_t fileType;
    int flags;
    rodsHostAddr_t addr;
    char dirName[MAX_NAME_LEN];
} fileRmdirInp_t;

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char fileName[MAX_NAME_LEN];
    int flag;
} fileStageInp_t;

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char fileName[MAX_NAME_LEN];
} fileStatInp_t;

typedef struct {
    fileDriverType_t fileType;
    rodsHostAddr_t addr;
    char fileName[MAX_NAME_LEN];
} fileUnlinkInp_t;

typedef struct {
    int fileInx;
    int len;
} fileWriteInp_t;

/*****************************************************************************/

int rcFileChmod (rcComm_t *conn, fileChmodInp_t *fileChmodInp);

/*****************************************************************************/

int rcFileChksum (rcComm_t *conn, fileChksumInp_t *fileChksumInp,
char **chksumStr);

/*****************************************************************************/

int rcFileClose (rcComm_t *conn, fileCloseInp_t *fileCloseInp);

/*****************************************************************************/

int rcFileClosedir (rcComm_t *conn, fileClosedirInp_t *fileClosedirInp);

/*****************************************************************************/

int rcFileCreate (rcComm_t *conn, fileCreateInp_t *fileCreateInp);

/*****************************************************************************/

%inline %{
rodsStat_t * rcFileFstat(rcComm_t *conn, fileFstatInp_t *fileFstatInp) {
    rodsStat_t * fileFstatOut = NULL;
    rcFileFstat(conn, fileFstatInp, &fileFstatOut);
    return fileFstatOut;
}
%}

/*****************************************************************************/

int rcFileFsync (rcComm_t *conn, fileFsyncInp_t *fileFsyncInp);

/*****************************************************************************/

int
rcFileGet (rcComm_t *conn, fileOpenInp_t *fileGetInp, 
bytesBuf_t *fileGetOutBBuf);

/*****************************************************************************/

%inline %{
fileGetFsFreeSpaceOut_t * rcFileGetFsFreeSpace(rcComm_t *conn, fileGetFsFreeSpaceInp_t *fileGetFsFreeSpaceInp) {
    fileGetFsFreeSpaceOut_t * fileGetFsFreeSpaceOut = NULL;
    rcFileGetFsFreeSpace(conn, fileGetFsFreeSpaceInp, &fileGetFsFreeSpaceOut);
    return fileGetFsFreeSpaceOut;
}
%}

/*****************************************************************************/

%inline %{
fileLseekOut_t * rcFileLseek(rcComm_t *conn, fileLseekInp_t *fileLseekInp) {
    fileLseekOut_t * fileLseekOut = NULL;
    rcFileLseek(conn, fileLseekInp, &fileLseekOut);
    return fileLseekOut;
}
%}

/*****************************************************************************/

int rcFileMkdir (rcComm_t *conn, fileMkdirInp_t *fileMkdirInp);

/*****************************************************************************/

int rcFileOpen (rcComm_t *conn, fileOpenInp_t *fileOpenInp);

/*****************************************************************************/

int rcFileOpendir (rcComm_t *conn, fileOpendirInp_t *fileOpendirInp);

/*****************************************************************************/

int rcFilePut (rcComm_t *conn, fileOpenInp_t *filePutInp, 
bytesBuf_t *filePutInpBBuf);

/*****************************************************************************/

int rcFileRead (rcComm_t *conn, fileReadInp_t *fileReadInp,
bytesBuf_t *fileReadOutBBuf);

/*****************************************************************************/

%inline %{
rodsDirent_t * rcFileReaddir(rcComm_t *conn, fileReaddirInp_t *fileReaddirInp) {
    rodsDirent_t * fileReaddirOut = NULL;
    rcFileReaddir(conn, fileReaddirInp, &fileReaddirOut);
    return fileReaddirOut;
}
%}

/*****************************************************************************/

int rcFileRename (rcComm_t *conn, fileRenameInp_t *fileRenameInp);

/*****************************************************************************/

int rcFileRmdir (rcComm_t *conn, fileRmdirInp_t *fileRmdirInp);

/*****************************************************************************/

int rcFileStage (rcComm_t *conn, fileStageInp_t *fileStageInp);

/*****************************************************************************/

%inline %{
rodsStat_t * rcFileStat(rcComm_t *conn, fileStatInp_t *fileStatInp) {
    rodsStat_t * fileStatOut = NULL;
    rcFileStat(conn, fileStatInp, &fileStatOut);
    return fileStatOut;
}
%}

/*****************************************************************************/

int rcFileTruncate (rcComm_t *conn, fileOpenInp_t *fileTruncateInp);

/*****************************************************************************/

int
rcFileUnlink (rcComm_t *conn, fileUnlinkInp_t *fileUnlinkInp);

/*****************************************************************************/

int rcFileWrite (rcComm_t *conn, fileWriteInp_t *fileWriteInp,
bytesBuf_t *fileWriteInpBBuf);

/*****************************************************************************/

int rcL3FileGetSingleBuf (rcComm_t *conn, int l1descInx,
bytesBuf_t *dataObjOutBBuf);

/*****************************************************************************/

int rcL3FilePutSingleBuf (rcComm_t *conn, int l1descInx,
bytesBuf_t *dataObjInBBuf);

/*****************************************************************************/
