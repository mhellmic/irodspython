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
  UINT4 state[4];
  UINT4 count[2];
  unsigned char buffer[64];
} MD5_CTX;

/*****************************************************************************/

int chksumLocFile (char *fileName, char *chksumStr);

/*****************************************************************************/

%inline %{
char * MD5Digest(char * md5Buf) {
    MD5_CTX context;
    unsigned char * digest = (unsigned char *) malloc(sizeof(unsigned char) * (RESPONSE_LEN+2));
    
    MD5Init(&context);
    MD5Update(&context, (unsigned char*) md5Buf, CHALLENGE_LEN+MAX_PASSWORD_LEN);
    MD5Final(digest, &context);
    
    return (char *) digest;
}
%}

/*****************************************************************************/

int md5ToStr (unsigned char *digest, char *chksumStr);

/*****************************************************************************/

int rcChksumLocFile (char *fileName, char *chksumFlag, keyValPair_t *condInput);

/*****************************************************************************/
