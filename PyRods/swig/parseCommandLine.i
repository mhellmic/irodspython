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
   int add;
   int age;
   int agevalue;
   int all;
   int accessControl;
   int admin;
   int ascitime;
   int attr;
   int noattr;
   char *attrStr;
   int bulk;
   int backupMode; 
   int condition;
   char *conditionString;
   int collection;
   char *collectionString;
   int dataObjects;
   int dim;
   int dryrun;
   int echo;
   int empty;
   int force;
   int file;
   char *fileString;
   //int global;
   int rescGroup;
   char *rescGroupString;
   int header;
   int help;
   int hostAddr;
   char *hostAddrString;
   int input;
   int redirectConn;
   int checksum;
   int verifyChecksum;
   int dataType;
   char *dataTypeString; 
   int longOption;
   int link;
   int rlock;
   int wlock;
   int veryLongOption;
   int mountCollection;
   char *mountType; 
   int replNum;
   char *replNumValue;
   int noPage;
   int number;
   int numberValue;
   int physicalPath;
   char *physicalPathString;
   int logicalPath;
   char *logicalPathString;
   int progressFlag;
   int option;
   char *optionString;
   int orphan;
   int purgeCache;
   int bundle;
   int prompt;
   int query;
   char *queryStr;
   int rbudp;
   int reg;
   int recursive;
   int resource;
   char *resourceString;
   int remove;
   int sizeFlag;
   rodsLong_t size;
   int srcResc;
   char *srcRescString;
   int subset;
   int subsetByVal;
   char *subsetStr;
   int test;
   int ticket;
   char *ticketString;
   int reconnect;
   int user;
   char *userString;
   int unmount;
   int verbose;
   int veryVerbose;
   int zone;
   char *zoneName;
   int verify;
   int var;
   char *varStr;
   int extract; 
   int restart;
   char *restartFileString;
   int lfrestart;
   char *lfrestartFileString;
   int version;
   int retries;
   int retriesValue;
   int regRepl;
   int excludeFile;
   char *excludeFileString;

   int parallel;
   int serial;
   int masterIcat;
   int silent;
   int sql;
   int optind;
} rodsArguments_t;

/*****************************************************************************/

int parseCmdLineOpt(int argc, char **argv, char *optString, int includeLong,
         rodsArguments_t *rodsArgs);

/*****************************************************************************/