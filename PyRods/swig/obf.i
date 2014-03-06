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

%cstring_bounded_output(char *obf_out10, MAX_PASSWORD_LEN+10);
%cstring_bounded_output(char *obf_out100, MAX_PASSWORD_LEN+100);

/*****************************************************************************/

void obfDecodeByKey(char *in, char *key, char *obf_out100);
void obfDecodeByKeyV2(char *in, char *key, char *key2, char *obf_out100);
void obfEncodeByKey(char *in, char *key, char *obf_out100);
void obfEncodeByKeyV2(char *in, char *key, char *key2, char *obf_out100);
int obfGetPw(char *obf_out10);
int obfiDecode(char *in, char *obf_out10, int extra);
void obfiEncode(char *in, char *obf_out10, int extra);
int obfiGetEnvKey();
int obfiGetPw(char *fileName, char *obf_out10);
int obfiGetTv(char *fileName);
int obfiOpenOutFile(char *fileName, int fileOpt);
int obfiWritePw(int fd, char *pw);
int obfRmPw(int opt);
int obfSavePw(int promptOpt, int fileOpt, int printOpt, char *pwArg);
int obfTempOps(int tmpOpt);

/*****************************************************************************/