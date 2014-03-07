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
 
#define CHALLENGE_LEN 64
#define RESPONSE_LEN 16

#define DONE_OPR             9999
#define PUT_OPR              1
#define GET_OPR              2
#define SAME_HOST_COPY_OPR   3
#define COPY_TO_LOCAL_OPR    4
#define COPY_TO_REM_OPR      5
#define REPLICATE_OPR        6
#define REPLICATE_DEST       7
#define REPLICATE_SRC        8
#define COPY_DEST            9
#define COPY_SRC             10
#define RENAME_DATA_OBJ      11
#define RENAME_COLL          12
#define MOVE_OPR             13
#define RSYNC_OPR            14
#define PHYMV_OPR            15
#define PHYMV_SRC            16
#define PHYMV_DEST           17
#define QUERY_DATA_OBJ       18
#define QUERY_DATA_OBJ_RECUR 19
#define QUERY_COLL_OBJ       20
#define QUERY_COLL_OBJ_RECUR 21
#define RENAME_UNKNOWN_TYPE  22
#define REMOTE_ZONE_OPR      24
#define UNREG_OPR            26

#define NC_OPR            1000
#define NC_OPEN_FOR_WRITE 1000
#define NC_OPEN_FOR_READ  1001
#define NC_CREATE         1002
#define NC_OPEN_GROUP     1003

#define CREATE_TYPE         1
#define OPEN_FOR_READ_TYPE  2
#define OPEN_FOR_WRITE_TYPE 3

#define STREAMING_FLAG       0x1
#define NO_CHK_COPY_LEN_FLAG 0x2

#define READ_LOCK_TYPE  "readLockType"
#define WRITE_LOCK_TYPE "writeLockType"
#define UNLOCK_TYPE     "unlockType"

#define SET_LOCK_CMD      "setLockCmd"
#define SET_LOCK_WAIT_CMD "setLockWaitCmd"
#define GET_LOCK_CMD      "getLockCmd"

#define LONG_METADATA_FG           0x1
#define VERY_LONG_METADATA_FG      0x2
#define RECUR_QUERY_FG             0x4
#define DATA_QUERY_FIRST_FG        0x8
#define NO_TRIM_REPL_FG            0x10
#define INCLUDE_CONDINPUT_IN_QUERY 0x20

#define STR_MS_T                "STR_PI"
#define INT_MS_T                "INT_PI"
#define INT16_MS_T              "INT16_PI"
#define CHAR_MS_T               "CHAR_PI"
#define BUF_LEN_MS_T            "BUF_LEN_PI"
#define STREAM_MS_T             "INT_PI"
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
#define StrArray_MS_T           "StrArray_PI"
#define IntArray_MS_T           "IntArray_PI"
#define GenQueryInp_MS_T        "GenQueryInp_PI"
#define GenQueryOut_MS_T        "GenQueryOut_PI"
#define XmsgTicketInfo_MS_T     "XmsgTicketInfo_PI"
#define SendXmsgInfo_MS_T       "SendXmsgInfo_PI"
#define GetXmsgTicketInp_MS_T   "GetXmsgTicketInp_PI"
#define SendXmsgInp_MS_T        "SendXmsgInp_PI"
#define RcvXmsgInp_MS_T         "RcvXmsgInp_PI"
#define RcvXmsgOut_MS_T         "RcvXmsgOut_PI"
#define StructFileExtAndRegInp_MS_T "StructFileExtAndRegInp_PI"
#define RuleSet_MS_T            "RuleSet_PI"
#define RuleStruct_MS_T         "RuleStruct_PI"
#define DVMapStruct_MS_T        "DVMapStruct_PI"
#define FNMapStruct_MS_T        "FNMapStruct_PI"
#define MsrvcStruct_MS_T        "MsrvcStruct_PI"
#define NcOpenInp_MS_T          "NcOpenInp_PI"
#define NcInqIdInp_MS_T         "NcInqIdInp_PI"
#define NcInqWithIdOut_MS_T     "NcInqWithIdOut_PI"
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

#define MAX_PASSWORD_LEN 50

#define MAX_PATH_ALLOWED 1024
#define MAX_NAME_LEN   (MAX_PATH_ALLOWED+64)
#define TRANS_BUF_SZ    (4*1024*1024)

#define PUBLIC_USER_NAME    "public"

#define NO_CHK_PERM_FLAG    0x1
#define UNIQUE_REM_COMM_FLAG    0x2
#define FORCE_FLAG      0x4
#define RMDIR_RECUR 0x1

#define PURGE_STRUCT_FILE_CACHE 0x1 
#define DELETE_STRUCT_FILE  0x2 
#define NO_REG_COLL_INFO    0x4 
#define LOGICAL_BUNDLE      0x8
#define CREATE_TAR_OPR      0x0
#define ADD_TO_TAR_OPR          0x10
#define PRESERVE_COLL_PATH      0x20
#define PRESERVE_DIR_CONT   0x40

// We can also use the os module in Python
#define O_RDONLY 0
#define O_WRONLY 1
#define O_RDWR 2
#define O_CREAT 64
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#define LOG_SQL 11
#define LOG_DEBUG1  10
#define LOG_DEBUG2  9
#define LOG_DEBUG3  8
#define LOG_DEBUG   7
#define LOG_NOTICE  5
#define LOG_ERROR  3
#define LOG_SYS_WARNING 2
#define LOG_SYS_FATAL 1

#define ALLOW_NO_SRC_FLAG   0x1


#define MAX_SQL_ATTR    50
#define MAX_SQL_ROWS   256

#define ORDER_BY 0x400
#define ORDER_BY_DESC 0x800

#define RETURN_TOTAL_ROW_COUNT 0x20
#define NO_DISTINCT 0x40
#define QUOTA_QUERY 0x80
#define AUTO_CLOSE  0x100
#define UPPER_CASE_WHERE  0x200

#define SELECT_MIN 2
#define SELECT_MAX 3
#define SELECT_SUM 4
#define SELECT_AVG 5
#define SELECT_COUNT 6

#define MAX_CORE_TABLE_VALUE 10000

#define COL_ZONE_ID 101
#define COL_ZONE_NAME 102
#define COL_ZONE_TYPE 103
#define COL_ZONE_CONNECTION 104
#define COL_ZONE_COMMENT 105
#define COL_ZONE_CREATE_TIME 106
#define COL_ZONE_MODIFY_TIME 107

#define COL_USER_ID 201
#define COL_USER_NAME 202
#define COL_USER_TYPE 203
#define COL_USER_ZONE 204
#define COL_USER_INFO 206
#define COL_USER_COMMENT 207
#define COL_USER_CREATE_TIME 208
#define COL_USER_MODIFY_TIME 209

#define COL_USER_DN_INVALID 205 /* For backward compatibility, irods 2.1 DN */

#define COL_R_RESC_ID 301
#define COL_R_RESC_NAME 302
#define COL_R_ZONE_NAME 303
#define COL_R_TYPE_NAME 304
#define COL_R_CLASS_NAME 305
#define COL_R_LOC 306
#define COL_R_VAULT_PATH 307
#define COL_R_FREE_SPACE 308
#define COL_R_RESC_INFO  309
#define COL_R_RESC_COMMENT 310
#define COL_R_CREATE_TIME 311
#define COL_R_MODIFY_TIME 312
#define COL_R_RESC_STATUS 313
#define COL_R_FREE_SPACE_TIME 314

#define COL_D_DATA_ID 401
#define COL_D_COLL_ID 402
#define COL_DATA_NAME 403
#define COL_DATA_REPL_NUM 404
#define COL_DATA_VERSION 405
#define COL_DATA_TYPE_NAME 406
#define COL_DATA_SIZE 407
#define COL_D_RESC_GROUP_NAME 408
#define COL_D_RESC_NAME 409
#define COL_D_DATA_PATH 410
#define COL_D_OWNER_NAME 411
#define COL_D_OWNER_ZONE 412
#define COL_D_REPL_STATUS 413 /* isDirty */
#define COL_D_DATA_STATUS 414
#define COL_D_DATA_CHECKSUM 415
#define COL_D_EXPIRY 416
#define COL_D_MAP_ID 417
#define COL_D_COMMENTS 418
#define COL_D_CREATE_TIME 419
#define COL_D_MODIFY_TIME 420
#define COL_DATA_MODE 421

#define COL_COLL_ID 500
#define COL_COLL_NAME 501
#define COL_COLL_PARENT_NAME 502
#define COL_COLL_OWNER_NAME 503
#define COL_COLL_OWNER_ZONE 504
#define COL_COLL_MAP_ID 505
#define COL_COLL_INHERITANCE 506
#define COL_COLL_COMMENTS 507
#define COL_COLL_CREATE_TIME 508
#define COL_COLL_MODIFY_TIME 509
#define COL_COLL_TYPE 510
#define COL_COLL_INFO1 511
#define COL_COLL_INFO2 512

#define COL_META_DATA_ATTR_NAME 600
#define COL_META_DATA_ATTR_VALUE 601
#define COL_META_DATA_ATTR_UNITS 602
#define COL_META_DATA_ATTR_ID 603
#define COL_META_DATA_CREATE_TIME 604
#define COL_META_DATA_MODIFY_TIME 605

#define COL_META_COLL_ATTR_NAME 610
#define COL_META_COLL_ATTR_VALUE 611
#define COL_META_COLL_ATTR_UNITS 612
#define COL_META_COLL_ATTR_ID 613
#define COL_META_COLL_CREATE_TIME 614
#define COL_META_COLL_MODIFY_TIME 615

#define COL_META_NAMESPACE_COLL 620
#define COL_META_NAMESPACE_DATA 621
#define COL_META_NAMESPACE_RESC 622
#define COL_META_NAMESPACE_USER 623
#define COL_META_NAMESPACE_RESC_GROUP 624
#define COL_META_NAMESPACE_RULE 625
#define COL_META_NAMESPACE_MSRVC 626
#define COL_META_NAMESPACE_MET2 627

#define COL_META_RESC_ATTR_NAME 630
#define COL_META_RESC_ATTR_VALUE 631
#define COL_META_RESC_ATTR_UNITS 632
#define COL_META_RESC_ATTR_ID 633
#define COL_META_RESC_CREATE_TIME 634
#define COL_META_RESC_MODIFY_TIME 635

#define COL_META_USER_ATTR_NAME 640
#define COL_META_USER_ATTR_VALUE 641
#define COL_META_USER_ATTR_UNITS 642
#define COL_META_USER_ATTR_ID 643
#define COL_META_USER_CREATE_TIME 644
#define COL_META_USER_MODIFY_TIME 645

#define COL_META_RESC_GROUP_ATTR_NAME 650
#define COL_META_RESC_GROUP_ATTR_VALUE 651
#define COL_META_RESC_GROUP_ATTR_UNITS 652
#define COL_META_RESC_GROUP_ATTR_ID 653
#define COL_META_RESC_GROUP_CREATE_TIME 654
#define COL_META_RESC_GROUP_MODIFY_TIME 655

#define COL_META_RULE_ATTR_NAME 660
#define COL_META_RULE_ATTR_VALUE 661
#define COL_META_RULE_ATTR_UNITS 662
#define COL_META_RULE_ATTR_ID 663
#define COL_META_RULE_CREATE_TIME 664
#define COL_META_RULE_MODIFY_TIME 665

#define COL_META_MSRVC_ATTR_NAME 670
#define COL_META_MSRVC_ATTR_VALUE 671
#define COL_META_MSRVC_ATTR_UNITS 672
#define COL_META_MSRVC_ATTR_ID 673
#define COL_META_MSRVC_CREATE_TIME 674
#define COL_META_MSRVC_MODIFY_TIME 675

#define COL_META_MET2_ATTR_NAME 680
#define COL_META_MET2_ATTR_VALUE 681
#define COL_META_MET2_ATTR_UNITS 682
#define COL_META_MET2_ATTR_ID 683
#define COL_META_MET2_CREATE_TIME 684
#define COL_META_MET2_MODIFY_TIME 685

#define COL_DATA_ACCESS_TYPE 700
#define COL_DATA_ACCESS_NAME 701
#define COL_DATA_TOKEN_NAMESPACE 702
#define COL_DATA_ACCESS_USER_ID 703
#define COL_DATA_ACCESS_DATA_ID 704

#define COL_COLL_ACCESS_TYPE 710
#define COL_COLL_ACCESS_NAME 711
#define COL_COLL_TOKEN_NAMESPACE 712
#define COL_COLL_ACCESS_USER_ID 713
#define COL_COLL_ACCESS_COLL_ID 714

#define COL_RESC_ACCESS_TYPE 720
#define COL_RESC_ACCESS_NAME 721
#define COL_RESC_TOKEN_NAMESPACE 722
#define COL_RESC_ACCESS_USER_ID 723
#define COL_RESC_ACCESS_RESC_ID 724

#define COL_META_ACCESS_TYPE 730
#define COL_META_ACCESS_NAME 731
#define COL_META_TOKEN_NAMESPACE 732
#define COL_META_ACCESS_USER_ID 733
#define COL_META_ACCESS_META_ID 734

#define COL_RULE_ACCESS_TYPE 740
#define COL_RULE_ACCESS_NAME 741
#define COL_RULE_TOKEN_NAMESPACE 742
#define COL_RULE_ACCESS_USER_ID 743
#define COL_RULE_ACCESS_RULE_ID 744

#define COL_MSRVC_ACCESS_TYPE 750
#define COL_MSRVC_ACCESS_NAME 751
#define COL_MSRVC_TOKEN_NAMESPACE 752
#define COL_MSRVC_ACCESS_USER_ID 753
#define COL_MSRVC_ACCESS_MSRVC_ID 754

#define COL_RESC_GROUP_RESC_ID 800
#define COL_RESC_GROUP_NAME 801
#define COL_RESC_GROUP_ID 802

#define COL_USER_GROUP_ID 900
#define COL_USER_GROUP_NAME 901

#define COL_RULE_EXEC_ID 1000
#define COL_RULE_EXEC_NAME 1001
#define COL_RULE_EXEC_REI_FILE_PATH 1002
#define COL_RULE_EXEC_USER_NAME   1003
#define COL_RULE_EXEC_ADDRESS 1004
#define COL_RULE_EXEC_TIME    1005
#define COL_RULE_EXEC_FREQUENCY 1006
#define COL_RULE_EXEC_PRIORITY 1007
#define COL_RULE_EXEC_ESTIMATED_EXE_TIME 1008
#define COL_RULE_EXEC_NOTIFICATION_ADDR 1009
#define COL_RULE_EXEC_LAST_EXE_TIME 1010
#define COL_RULE_EXEC_STATUS 1011

#define COL_TOKEN_NAMESPACE 1100
#define COL_TOKEN_ID 1101
#define COL_TOKEN_NAME 1102
#define COL_TOKEN_VALUE 1103
#define COL_TOKEN_VALUE2 1104
#define COL_TOKEN_VALUE3 1105
#define COL_TOKEN_COMMENT 1106

#define COL_AUDIT_OBJ_ID      1200
#define COL_AUDIT_USER_ID     1201
#define COL_AUDIT_ACTION_ID   1202
#define COL_AUDIT_COMMENT     1203
#define COL_AUDIT_CREATE_TIME 1204
#define COL_AUDIT_MODIFY_TIME 1205

#define COL_AUDIT_RANGE_START 1200
#define COL_AUDIT_RANGE_END   1299

#define COL_COLL_USER_NAME    1300
#define COL_COLL_USER_ZONE    1301

#define COL_DATA_USER_NAME    1310
#define COL_DATA_USER_ZONE    1311

#define COL_RESC_USER_NAME    1320
#define COL_RESC_USER_ZONE    1321

#define COL_SL_HOST_NAME      1400
#define COL_SL_RESC_NAME      1401
#define COL_SL_CPU_USED       1402
#define COL_SL_MEM_USED       1403
#define COL_SL_SWAP_USED      1404
#define COL_SL_RUNQ_LOAD      1405
#define COL_SL_DISK_SPACE     1406
#define COL_SL_NET_INPUT      1407
#define COL_SL_NET_OUTPUT     1408
#define COL_SL_NET_OUTPUT     1408
#define COL_SL_CREATE_TIME    1409

#define COL_SLD_RESC_NAME     1500
#define COL_SLD_LOAD_FACTOR   1501
#define COL_SLD_CREATE_TIME   1502

#define COL_USER_AUTH_ID 1600
#define COL_USER_DN      1601

#define COL_RULE_ID           1700
#define COL_RULE_VERSION      1701
#define COL_RULE_BASE_NAME    1702
#define COL_RULE_NAME         1703
#define COL_RULE_EVENT        1704
#define COL_RULE_CONDITION    1705
#define COL_RULE_BODY         1706
#define COL_RULE_RECOVERY     1707
#define COL_RULE_STATUS       1708
#define COL_RULE_OWNER_NAME   1709
#define COL_RULE_OWNER_ZONE   1710
#define COL_RULE_DESCR_1      1711
#define COL_RULE_DESCR_2      1712
#define COL_RULE_INPUT_PARAMS      1713
#define COL_RULE_OUTPUT_PARAMS     1714
#define COL_RULE_DOLLAR_VARS       1715
#define COL_RULE_ICAT_ELEMENTS     1716
#define COL_RULE_SIDEEFFECTS       1717
#define COL_RULE_COMMENT      1718
#define COL_RULE_CREATE_TIME  1719
#define COL_RULE_MODIFY_TIME  1720

#define COL_RULE_BASE_MAP_VERSION      1721
#define COL_RULE_BASE_MAP_BASE_NAME    1722
#define COL_RULE_BASE_MAP_OWNER_NAME   1723
#define COL_RULE_BASE_MAP_OWNER_ZONE   1724
#define COL_RULE_BASE_MAP_COMMENT      1725
#define COL_RULE_BASE_MAP_CREATE_TIME  1726
#define COL_RULE_BASE_MAP_MODIFY_TIME  1727
#define COL_RULE_BASE_MAP_PRIORITY     1728 

#define COL_DVM_ID            1800
#define COL_DVM_VERSION       1801
#define COL_DVM_BASE_NAME     1802
#define COL_DVM_EXT_VAR_NAME  1803
#define COL_DVM_CONDITION     1804
#define COL_DVM_INT_MAP_PATH  1805
#define COL_DVM_STATUS        1806
#define COL_DVM_OWNER_NAME    1807
#define COL_DVM_OWNER_ZONE    1808
#define COL_DVM_COMMENT       1809
#define COL_DVM_CREATE_TIME   1810
#define COL_DVM_MODIFY_TIME   1811

#define COL_DVM_BASE_MAP_VERSION      1812
#define COL_DVM_BASE_MAP_BASE_NAME    1813
#define COL_DVM_BASE_MAP_OWNER_NAME   1814
#define COL_DVM_BASE_MAP_OWNER_ZONE   1815
#define COL_DVM_BASE_MAP_COMMENT      1816
#define COL_DVM_BASE_MAP_CREATE_TIME  1817
#define COL_DVM_BASE_MAP_MODIFY_TIME  1818

#define COL_FNM_ID            1900
#define COL_FNM_VERSION       1901
#define COL_FNM_BASE_NAME     1902
#define COL_FNM_EXT_FUNC_NAME 1903
#define COL_FNM_INT_FUNC_NAME 1904
#define COL_FNM_STATUS        1905
#define COL_FNM_OWNER_NAME    1906
#define COL_FNM_OWNER_ZONE    1907
#define COL_FNM_COMMENT       1908
#define COL_FNM_CREATE_TIME   1909
#define COL_FNM_MODIFY_TIME   1910

#define COL_FNM_BASE_MAP_VERSION      1911
#define COL_FNM_BASE_MAP_BASE_NAME    1912
#define COL_FNM_BASE_MAP_OWNER_NAME   1913
#define COL_FNM_BASE_MAP_OWNER_ZONE   1914
#define COL_FNM_BASE_MAP_COMMENT      1915
#define COL_FNM_BASE_MAP_CREATE_TIME  1916
#define COL_FNM_BASE_MAP_MODIFY_TIME  1917

#define COL_QUOTA_USER_ID     2000
#define COL_QUOTA_RESC_ID     2001
#define COL_QUOTA_LIMIT       2002
#define COL_QUOTA_OVER        2003
#define COL_QUOTA_MODIFY_TIME 2004

#define COL_QUOTA_USAGE_USER_ID     2010
#define COL_QUOTA_USAGE_RESC_ID     2011
#define COL_QUOTA_USAGE             2012
#define COL_QUOTA_USAGE_MODIFY_TIME 2013

#define COL_QUOTA_RESC_NAME  2020
#define COL_QUOTA_USER_NAME  2021
#define COL_QUOTA_USER_ZONE  2022
#define COL_QUOTA_USER_TYPE  2023

#define COL_MSRVC_ID 2100
#define COL_MSRVC_NAME 2101
#define COL_MSRVC_SIGNATURE 2102
#define COL_MSRVC_DOXYGEN 2103
#define COL_MSRVC_VARIATIONS 2104
#define COL_MSRVC_STATUS 2105
#define COL_MSRVC_OWNER_NAME 2106
#define COL_MSRVC_OWNER_ZONE 2107
#define COL_MSRVC_COMMENT 2108
#define COL_MSRVC_CREATE_TIME 2109
#define COL_MSRVC_MODIFY_TIME 2110
#define COL_MSRVC_VERSION 2111
#define COL_MSRVC_HOST 2112
#define COL_MSRVC_LOCATION 2113
#define COL_MSRVC_LANGUAGE 2114
#define COL_MSRVC_TYPE_NAME 2115
#define COL_MSRVC_MODULE_NAME 2116

#define COL_MSRVC_VER_OWNER_NAME 2150
#define COL_MSRVC_VER_OWNER_ZONE 2151
#define COL_MSRVC_VER_COMMENT 2152
#define COL_MSRVC_VER_CREATE_TIME 2153
#define COL_MSRVC_VER_MODIFY_TIME 2154

#define COL_TICKET_ID 2200
#define COL_TICKET_STRING 2201
#define COL_TICKET_TYPE 2202
#define COL_TICKET_USER_ID 2203
#define COL_TICKET_OBJECT_ID 2204
#define COL_TICKET_OBJECT_TYPE 2205
#define COL_TICKET_USES_LIMIT 2206
#define COL_TICKET_USES_COUNT 2207
#define COL_TICKET_EXPIRY_TS 2208
#define COL_TICKET_CREATE_TIME 2209
#define COL_TICKET_MODIFY_TIME 2210
#define COL_TICKET_WRITE_FILE_COUNT 2211
#define COL_TICKET_WRITE_FILE_LIMIT 2212
#define COL_TICKET_WRITE_BYTE_COUNT 2213
#define COL_TICKET_WRITE_BYTE_LIMIT 2214

#define COL_TICKET_ALLOWED_HOST_TICKET_ID 2220
#define COL_TICKET_ALLOWED_HOST 2221
#define COL_TICKET_ALLOWED_USER_TICKET_ID 2222
#define COL_TICKET_ALLOWED_USER_NAME 2223
#define COL_TICKET_ALLOWED_GROUP_TICKET_ID 2224
#define COL_TICKET_ALLOWED_GROUP_NAME 2225

#define COL_TICKET_DATA_NAME 2226
#define COL_TICKET_DATA_COLL_NAME 2227
#define COL_TICKET_COLL_NAME 2228

#define COL_TICKET_OWNER_NAME 2229
#define COL_TICKET_OWNER_ZONE 2230

#define COL_COLL_FILEMETA_OBJ_ID 2300
#define COL_COLL_FILEMETA_UID 2301
#define COL_COLL_FILEMETA_GID 2302
#define COL_COLL_FILEMETA_OWNER 2303
#define COL_COLL_FILEMETA_GROUP 2304
#define COL_COLL_FILEMETA_MODE 2305
#define COL_COLL_FILEMETA_CTIME 2306
#define COL_COLL_FILEMETA_MTIME 2307
#define COL_COLL_FILEMETA_SOURCE_PATH 2308
#define COL_COLL_FILEMETA_CREATE_TIME 2309
#define COL_COLL_FILEMETA_MODIFY_TIME 2310

#define COL_DATA_FILEMETA_OBJ_ID 2320
#define COL_DATA_FILEMETA_UID 2321
#define COL_DATA_FILEMETA_GID 2322
#define COL_DATA_FILEMETA_OWNER 2323
#define COL_DATA_FILEMETA_GROUP 2324
#define COL_DATA_FILEMETA_MODE 2325
#define COL_DATA_FILEMETA_CTIME 2326
#define COL_DATA_FILEMETA_MTIME 2327
#define COL_DATA_FILEMETA_SOURCE_PATH 2328
#define COL_DATA_FILEMETA_CREATE_TIME 2329
#define COL_DATA_FILEMETA_MODIFY_TIME 2330

#define SINGLE_MSG_TICKET  0
#define MULTI_MSG_TICKET   1

#define ACCESS_NULL                 "null"
#define ACCESS_EXECUTE              "execute"
#define ACCESS_READ_ANNOTATION      "read annotation"
#define ACCESS_READ_SYSTEM_METADATA "read system metadata"
#define ACCESS_READ_METADATA        "read metadata"
#define ACCESS_READ_OBJECT          "read object"
#define ACCESS_WRITE_ANNOTATION     "write annotation"
#define ACCESS_CREATE_METADATA      "create metadata"
#define ACCESS_MODIFY_METADATA      "modify metadata"
#define ACCESS_DELETE_METADATA      "delete metadata"
#define ACCESS_ADMINISTER_OBJECT    "administer object"
#define ACCESS_CREATE_OBJECT        "create object"
#define ACCESS_MODIFY_OBJECT        "modify object"
#define ACCESS_DELETE_OBJECT        "delete object"
#define ACCESS_CREATE_TOKEN         "create token"
#define ACCESS_DELETE_TOKEN         "delete token"
#define ACCESS_CURATE               "curate"
#define ACCESS_OWN                  "own"

#define ACCESS_INHERIT              "inherit"
#define ACCESS_NO_INHERIT           "noinherit"

#define AU_ACCESS_GRANTED                      1000

#define AU_REGISTER_DATA_OBJ                   2010
#define AU_REGISTER_DATA_REPLICA               2011
#define AU_UNREGISTER_DATA_OBJ                 2012

#define AU_REGISTER_DELAYED_RULE               2020
#define AU_MODIFY_DELAYED_RULE                 2021
#define AU_DELETE_DELAYED_RULE                 2022

#define AU_REGISTER_RESOURCE                   2030
#define AU_DELETE_RESOURCE                     2031

#define AU_DELETE_USER_RE                      2040

#define AU_REGISTER_COLL_BY_ADMIN              2050
#define AU_REGISTER_COLL                       2051

#define AU_DELETE_COLL_BY_ADMIN                2060
#define AU_DELETE_COLL                         2061
#define AU_DELETE_ZONE                         2062

#define AU_REGISTER_ZONE                       2064

#define AU_MOD_USER_NAME                       2070
#define AU_MOD_USER_TYPE                       2071
#define AU_MOD_USER_ZONE                       2072
#define AU_MOD_USER_DN                         2073  /* no longer used */
#define AU_MOD_USER_INFO                       2074
#define AU_MOD_USER_COMMENT                    2075
#define AU_MOD_USER_PASSWORD                   2076

#define AU_ADD_USER_AUTH_NAME                  2077
#define AU_DELETE_USER_AUTH_NAME               2078

#define AU_MOD_GROUP                           2080
#define AU_MOD_RESC                            2090
#define AU_MOD_RESC_FREE_SPACE                 2091
#define AU_MOD_RESC_GROUP                      2092
#define AU_MOD_ZONE                            2093

#define AU_REGISTER_USER_RE                    2100
#define AU_ADD_AVU_METADATA                    2110
#define AU_DELETE_AVU_METADATA                 2111
#define AU_COPY_AVU_METADATA                   2112
#define AU_ADD_AVU_WILD_METADATA               2113

#define AU_MOD_ACCESS_CONTROL_OBJ              2120
#define AU_MOD_ACCESS_CONTROL_COLL             2121
#define AU_MOD_ACCESS_CONTROL_COLL_RECURSIVE   2122
#define AU_MOD_ACCESS_CONTROL_RESOURCE         2123

#define AU_RENAME_DATA_OBJ                     2130
#define AU_RENAME_COLLECTION                   2131

#define AU_MOVE_DATA_OBJ                       2140
#define AU_MOVE_COLL                           2141

#define AU_REG_TOKEN                           2150
#define AU_DEL_TOKEN                           2151

#define AU_CREATE_TICKET                       2160
#define AU_MOD_TICKET                          2161
#define AU_DELETE_TICKET                       2162
#define AU_USE_TICKET                          2163


