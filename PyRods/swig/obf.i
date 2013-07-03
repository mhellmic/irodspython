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

#define MAX_PASSWORD_LEN 50

/*****************************************************************************/

%inline %{
char * obfDecodeByKey(char *in, char *key) {
    char * out = (char*) malloc(sizeof(MAX_PASSWORD_LEN+100));
    obfDecodeByKey(in, key, out);
    return out;
}
%}

/*****************************************************************************/

%inline %{
char * obfDecodeByKeyV2(char *in, char *key1, char *key2) {
    char * out = (char*) malloc(sizeof(MAX_PASSWORD_LEN+10));
    obfDecodeByKeyV2(in, key1, key2, out);
    return out;
}
%}

/*****************************************************************************/

%inline %{
char * obfEncodeByKey(char *in, char *key) {
    char * out = (char*) malloc(sizeof(MAX_PASSWORD_LEN+100));
    obfEncodeByKey(in, key, out);
    return out;
}
%}

/*****************************************************************************/

%inline %{
char * obfEncodeByKeyV2(char *in, char *key, char *key2) {
    char * out = (char*) malloc(sizeof(MAX_PASSWORD_LEN+100));
    obfEncodeByKeyV2(in, key, key2, out);
    return out;
}
%}

/*****************************************************************************/

%cstring_bounded_output(char *obf_out1, MAX_PASSWORD_LEN+CHALLENGE_LEN+2);
int obfGetPw(char *obf_out1);

/*****************************************************************************/

%cstring_bounded_output(char *obf_out2, MAX_PASSWORD_LEN+10);
int obfiDecode(char *in, char *obf_out2, int extra);

/*****************************************************************************/

%inline %{
char * obfiEncode(char *in, int extra) {
    char * out = (char*) malloc(sizeof(MAX_PASSWORD_LEN+10));
    obfiEncode(in, out, extra);
    return out;
}
%}

/*****************************************************************************/

int obfiGetEnvKey();

/*****************************************************************************/

%cstring_bounded_output(char *obf_out3, MAX_PASSWORD_LEN+10);
int obfiGetPw(char *fileName, char *obf_out3);

/*****************************************************************************/

int obfiGetTv(char *fileName);

/*****************************************************************************/

int obfiOpenOutFile(char *fileName, int fileOpt);

/*****************************************************************************/

int obfiWritePw(int fd, char *pw);

/*****************************************************************************/

int obfRmPw(int opt);

/*****************************************************************************/

int obfSavePw(int promptOpt, int fileOpt, int printOpt, char *pwArg);

/*****************************************************************************/

int obfTempOps(int tmpOpt);

/*****************************************************************************/