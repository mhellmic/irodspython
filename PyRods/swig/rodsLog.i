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

#define LOG_SQL 11
#define LOG_DEBUG1  10
#define LOG_DEBUG2  9
#define LOG_DEBUG3  8
#define LOG_DEBUG   7
#define LOG_NOTICE  5
#define LOG_ERROR  3
#define LOG_SYS_WARNING 2
#define LOG_SYS_FATAL 1

/*****************************************************************************/

char *rodsErrorName(int errorValue, char **subName);

/*****************************************************************************/

void rodsLog(int level, char *formatStr, ...);

/*****************************************************************************/

void rodsLogError(int level, int errCode, char *formatStr, ...);

/*****************************************************************************/

void rodsLogLevel(int level);

/*****************************************************************************/
