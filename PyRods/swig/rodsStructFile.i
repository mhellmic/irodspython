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
#include "structFileBundle.h"
#include "structFileExtract.h"
#include "subStructFileClose.h"
#include "subStructFileClosedir.h"
#include "subStructFileCreate.h"
#include "subStructFileFstat.h"
#include "subStructFileGet.h"
#include "subStructFileLseek.h"
#include "subStructFileMkdir.h"
#include "subStructFileOpen.h"
#include "subStructFileOpendir.h"
#include "subStructFilePut.h"
#include "subStructFileReaddir.h"
#include "subStructFileRename.h"
#include "subStructFileRmdir.h"
#include "subStructFileTruncate.h"
#include "subStructFileUnlink.h"
#include "subStructFileWrite.h"
%}

/*****************************************************************************/

typedef struct StructFileExtAndRegInp {
    char objPath[MAX_NAME_LEN];
    char collection[MAX_NAME_LEN]; 
    int oprType;
    int flags;
    keyValPair_t condInput;
} structFileExtAndRegInp_t;

typedef struct StructFileOprInp {
    rodsHostAddr_t addr;
    int oprType;
    int flags;
    specColl_t *specColl;
    keyValPair_t condInput;
} structFileOprInp_t;

typedef struct SubStructFileFdOpr {
    rodsHostAddr_t addr;
    structFileType_t type;
    int fd;
    int len;
} subStructFileFdOprInp_t;

typedef struct SubStructFileLseekInp {
    rodsHostAddr_t addr;
    structFileType_t type;
    int fd;
    rodsLong_t offset;
    int whence;
} subStructFileLseekInp_t;

typedef struct SubStructFileRenameInp {
    subFile_t subFile;
    char newSubFilePath[MAX_NAME_LEN];
} subStructFileRenameInp_t;

/*****************************************************************************/

int rcStructFileBundle (rcComm_t *conn, 
structFileExtAndRegInp_t *structFileBundleInp);

/*****************************************************************************/

int rcStructFileExtAndReg (rcComm_t *conn, 
structFileExtAndRegInp_t *structFileExtAndRegInp);

/*****************************************************************************/

int rcStructFileExtract (rcComm_t *conn, structFileOprInp_t *structFileOprInp);

/*****************************************************************************/

int rcStructFileSync (rcComm_t *conn, structFileOprInp_t *structFileOprInp);

/*****************************************************************************/

int rcSubStructFileClose (rcComm_t *conn, subStructFileFdOprInp_t *subStructFileCloseInp);

/*****************************************************************************/

int rcSubStructFileClosedir (rcComm_t *conn, subStructFileFdOprInp_t *subStructFileClosedirInp);

/*****************************************************************************/

int rcSubStructFileCreate (rcComm_t *conn, subFile_t *subFile);

/*****************************************************************************/

%inline %{
rodsStat_t *rcSubStructFileFstat (rcComm_t *conn, subStructFileFdOprInp_t *subStructFileFstatInp) {
    rodsStat_t *subStructFileStatOut = NULL;
    int status = rcSubStructFileFstat(conn, subStructFileFstatInp, &subStructFileStatOut);
    if (status == 0)
        return subStructFileStatOut;
    else
        return NULL;
    }
%}

/*****************************************************************************/

int rcSubStructFileGet (rcComm_t *conn, subFile_t *subFile, 
bytesBuf_t *subFileGetOutBBuf);

/*****************************************************************************/

%inline %{
fileLseekOut_t *rcSubStructFileLseek (rcComm_t *conn, subStructFileLseekInp_t *subStructFileLseekInp) {
    fileLseekOut_t *subStructFileLseekOut = NULL;
    int status = rcSubStructFileLseek(conn, subStructFileLseekInp, &subStructFileLseekOut);
    if (status == 0)
        return subStructFileLseekOut;
    else
        return NULL;
    }
%}

/*****************************************************************************/

int rcSubStructFileMkdir (rcComm_t *conn, subFile_t *subFile);

/*****************************************************************************/

int rcSubStructFileOpen (rcComm_t *conn, subFile_t *subFile);

/*****************************************************************************/

int rcSubStructFileOpendir (rcComm_t *conn, subFile_t *subFile);

/*****************************************************************************/

int rcSubStructFilePut (rcComm_t *conn, subFile_t *subFile, 
bytesBuf_t *subFilePutOutBBuf);

/*****************************************************************************/

int rcSubStructFileRead (rcComm_t *conn, subStructFileFdOprInp_t *subStructFileReadInp,
bytesBuf_t *subStructFileReadOutBBuf);

/*****************************************************************************/

int rcSubStructFileReaddir (rcComm_t *conn, subStructFileFdOprInp_t *subStructFileReaddirInp,
rodsDirent_t **rodsDirent);

/*****************************************************************************/

int rcSubStructFileRename (rcComm_t *conn, subStructFileRenameInp_t *subStructFileRenameInp);

/*****************************************************************************/

int rcSubStructFileRmdir (rcComm_t *conn, subFile_t *subFile);

/*****************************************************************************/

int rcSubStructFileTruncate (rcComm_t *conn, subFile_t *subStructFileTruncateInp);

/*****************************************************************************/

int rcSubStructFileUnlink (rcComm_t *conn, subFile_t *subFile);

/*****************************************************************************/

int rcSubStructFileWrite (rcComm_t *conn, subStructFileFdOprInp_t *subStructFileWriteInp,
bytesBuf_t *subStructFileWriteOutBBuf);

/*****************************************************************************/