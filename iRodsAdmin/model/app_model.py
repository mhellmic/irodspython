# Copyright (c) 2009, University of Liverpool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Author       : Jerome Fuselier
# Creation     : August, 2009

"""The model of the application :
     - Configuration tools
     - Interface to iRODS API
     - Management or iRODS rules"""

try:
    import irods
except ImportError:
    print "You need PyRods package"
    import sys
    sys.exit(-1)

import os.path
import ConfigParser
import wx

from model.parsers import PythonParser


class AppModel(object):
    """Application Model
    This is also an interface to access PyRods"""

    def __init__(self, config):
        # A Config object
        self.cfg = config
        self.conn = None
        if self.cfg.use_irods:
            self.cfg.set_irods_info(self.get_default_username(),
                                       self.get_default_host(),
                                       self.get_default_zone(),
                                       self.get_default_port())

    def add_collection_metadata(self, irods_path, name, value, units=''):
        """Add metadatas to a collection"""
        return irods.addCollUserMetadata(self.conn, irods_path, name, value,
                                         units)

    def add_file_metadata(self, irods_path, name, value, units=''):
        """Add metadatas to a file"""
        return irods.addFileUserMetadata(self.conn, irods_path, name, value,
                                         units)

    def connect(self):
        """Connect to an irods server, return the connection and an error
        message"""
        return self.connect_infos(self.cfg.irods_hostname,
                                  self.cfg.irods_port,
                                  self.cfg.irods_username,
                                  self.cfg.irods_zone)

    def connect_infos(self, host, port, user, zone):
        """Same as connect but with information on the server in parameters
        port is an integer, host, user and zone are strings"""
        conn, err_msg = irods.rcConnect(host, port, user, zone)
        if not conn:
            self.conn = None
            return err_msg.status
        self.conn = conn
        return irods.clientLoginWithObfPassword(conn, self.cfg.password)

    def create_file(self, irods_path, content='', resc=None):
        """Create a new text file in iRODS"""
        if resc:
            f = irods.irodsOpen(self.conn, irods_path, "w", resc)
        else:
            f = irods.irodsOpen(self.conn, irods_path, "w")
        if not f:
            return False
        f.write(content)
        f.close()
        return True

    def delete_collection(self, irods_collection):
        """Delete a collection in iRODS
        irods_collection : path (str)"""
        collInp = irods.collInp_t()
        irods.addKeyVal(collInp.condInput, irods.RECURSIVE_OPR__KW, "")
        collInp.collName = irods_collection
        return irods.rcRmColl(self.conn, collInp, 0)

    def delete_file(self, path, resc=None):
        """Delete a file in iRODS
        path : irods path (str)
        resc : Resource"""
        dataObjInp = irods.dataObjInp_t()
        dataObjInp.openFlags = irods.O_RDONLY
        if resc:
            d = irods.getFileInfo(path, resc)
            irods.addKeyVal(dataObjInp.condInput,
                            irods.REPL_NUM_KW,
                            d['data_repl_num'])
        dataObjInp.objPath = path
        status = irods.rcDataObjUnlink(self.conn, dataObjInp)
        return status

    def delete_files(self, irods_files):
        """Delete a list of files from iRODS
        irods_files : list of tuples (collection, file, resource)"""
        dataObjInp = irods.dataObjInp_t()
        dataObjInp.openFlags = irods.O_RDONLY
        st = []
        for (collection, irods_file, resource) in irods_files:
            d = irods.getFileInfo(self.conn, collection, irods_file, resource)
            irods.addKeyVal(dataObjInp.condInput,
                            irods.REPL_NUM_KW,
                            d['data_repl_num'])
            dataObjInp.objPath = collection + '/' + irods_file
            status = irods.rcDataObjUnlink(self.conn, dataObjInp)
            st.append(status)
        return st

    def disconnect(self):
        """Disconnect from the server"""
        if self.conn:
            self.conn.disconnect()

    def download_collection(self, irods_collection, targ_dir=""):
        """Get the list of files of an irods collection
        if targ_dir is provided it becomes the prefix of the output relative
        target"""
        files_to_download = []
        dir_to_create = []
        _, collHandle = irods.rclOpenCollection(self.conn,
                                                     irods_collection,
                                                     irods.RECUR_QUERY_FG)
        if irods_collection.endswith('/'):
            irods_collection = irods_collection[:-1]
        if targ_dir.endswith(os.sep):
            targ_dir = targ_dir[:-1]
        # If we download the collection /tmpZone/home/rods/temp in /tmp then
        # in fact we want to download it in /tmp/temp to mimic the iget code
        # so the relative target path will have this name as a prefix
        coll_name = os.path.basename(irods_collection)
        collLen = len(irods_collection)

        status, collEnt = irods.rclReadCollection(self.conn, collHandle)
        while status >= 0:
            if collEnt.objType == irods.DATA_OBJ_T:
                src_child_path = "%s/%s" % (collEnt.collName,
                                            collEnt.dataName)
                tgt_relative_path = "%s%s/%s" % (coll_name,
                                                 collEnt.collName[collLen:],
                                                 collEnt.dataName)
                resc = collEnt.resource
                if targ_dir:
                    tgt_relative_path = targ_dir + '/' + tgt_relative_path
                tgt_relative_path = tgt_relative_path.replace("/", os.sep)
                files_to_download.append((src_child_path,
                                          resc,
                                          tgt_relative_path))
            elif collEnt.objType == irods.COLL_OBJ_T:
                tgt_dir = "%s%s" % (coll_name,
                                    collEnt.collName[collLen:])
                tgt_dir = tgt_dir.replace("/", os.sep)
                if targ_dir:
                    tgt_dir = targ_dir + '/' + tgt_dir
                dir_to_create.append(tgt_dir)
            status, collEnt = irods.rclReadCollection(self.conn, collHandle)
        irods.rclCloseCollection(collHandle)

        return files_to_download, dir_to_create

    def download_file(self, irods_path, local_path, resource=None,
                    overwrite=False):
        """Download a file from irods to a local directory
        - irods_files : list of tuples (collection, file, resource)
        - local path
        - resource
        - overwrite the exisiting file if it exists"""
        dataObjOprInp = irods.dataObjInp_t()
        dataObjOprInp.openFlags = irods.O_RDONLY
        if overwrite:
            irods.addKeyVal(dataObjOprInp.condInput, irods.FORCE_FLAG_KW, "")
        if resource:
            irods.addKeyVal(dataObjOprInp.condInput, irods.RESC_NAME_KW,
                            resource)
        dataObjOprInp.objPath = irods_path
        status = irods.rcDataObjGet(self.conn, dataObjOprInp, local_path)
        return status == irods.OVERWRITE_WITHOUT_FORCE_FLAG

    def download_files(self, irods_files, targPath, overwrite=False):
        """Download a list of files from irods to a local directory
        irods_files : list of tuples (collection, file, resource)
        targPath : local path
        If some files already exist in the local directory and if the overwrite
        option is not set then a structure is returned, the caller will then
        have to define a strategy."""
        dataObjOprInp = irods.dataObjInp_t()
        dataObjOprInp.openFlags = irods.O_RDONLY
        if overwrite:
            irods.addKeyVal(dataObjOprInp.condInput, irods.FORCE_FLAG_KW, "")
        already_there = []
        for (collection, irods_file, resource) in irods_files:
            if resource:
                irods.addKeyVal(dataObjOprInp.condInput,
                                irods.RESC_NAME_KW,
                                resource)
            dataObjOprInp.objPath = collection + '/' + irods_file
            status = irods.rcDataObjGet(self.conn,
                                        dataObjOprInp,
                                        targPath + os.sep + irods_file)
            # If the file is already present we catch the error
            if status == irods.OVERWRITE_WITHOUT_FORCE_FLAG:
                already_there.append((collection, irods_file, resource))
        return already_there

    def encode(self, password):
        """Encode a password"""
        envVal = irods.obfiGetEnvKey()
        return irods.obfiEncode(password, envVal)

    def file_exist(self, irods_path):
        """Return True if the file is present in iRODS"""
        f = irods.irodsOpen(self.conn, irods_path)
        return f != None

    def get_collection(self, path):
        """Get an iRodsCollection object from a path in iRODS"""
        return irods.irodsCollection(self.conn, path)

    def get_collection_metadatas(self, irods_path):
        """Get a list of metadatas for a collection
        a metadata is a tuple (name, value, units)"""
        return irods.getCollUserMetadata(self.conn, irods_path)

    def get_collection_nb_objects(self, irods_path):
        """Get the number of files of a collection from an irodsPath"""
        c = irods.irodsCollection(self.conn, irods_path)
        return c.getLenObjects()

    def get_collection_objects(self, irods_path):
        """Get the list of the files of a collection from an irodsPath
        The list is a list of irods.irodsFile"""
        c = irods.irodsCollection(self.conn, irods_path)
        return c.getObjects()

    def get_collection_subCollections(self, irods_path):
        """Get the list of the subcollection of a collection from an irodsPath
        The list is a list of irods.irodsCollection"""
        c = irods.irodsCollection(self.conn, irods_path)
        return c.getSubCollections()

    def get_config(self):
        """Get the configuration object of the application"""
        return self.cfg

    def get_current_dir(self):
        """Get the current collection from .irodsEnv"""
        status, myEnv = irods.getRodsEnv()
        if status < 0:
            return None
        return myEnv.rodsCwd

    def get_default_host(self):
        """Get the default host from .irodsEnv"""
        status, myEnv = irods.getRodsEnv()
        if myEnv and (status == 0):
            return myEnv.rodsHost
        else:
            return ""

    def get_default_port(self):
        """Get the default port from .irodsEnv"""
        status, myEnv = irods.getRodsEnv()
        if myEnv and (status == 0):
            return myEnv.rodsPort
        else:
            return 0

    def get_default_resource(self):
        """Get the default resource from .irodsEnv"""
        status, myEnv = irods.getRodsEnv()
        if myEnv and (status == 0):
            return myEnv.rodsDefResource
        else:
            return ""

    def get_default_username(self):
        """Get the default username from .irodsEnv"""
        status, myEnv = irods.getRodsEnv()
        if myEnv and (status == 0):
            return myEnv.rodsUserName
        else:
            return ""

    def get_default_zone(self):
        """Get the default zone from .irodsEnv"""
        status, myEnv = irods.getRodsEnv()
        if myEnv and (status == 0):
            return myEnv.rodsZone
        else:
            return ""

    def get_file_info(self, irods_path, resource):
        """Get a dictionary of file information"""
        _, coll_name, data_name = irods.splitPathByKey(irods_path, "/")
        return irods.getFileInfo(self.conn, coll_name, data_name, resource)

    def get_file_metadatas(self, irods_path):
        """Get a list of metadatas for a file
        a metadata is a tuple (name, value, units)"""
        return irods.getFileUserMetadata(self.conn, irods_path)

    def get_list_resources(self):
        """Get the list of resource names for the server"""
        irods_resc = irods.getResources(self.conn)
        return [resc.getName() for resc in irods_resc]

    def get_password(self):
        """Get The obfuscated password, obtained from .irodsA.
        Returns a string"""
        _, obf_password = irods.obfGetPw()
        return self.encode(obf_password)

    def get_user_infos(self, name):
        """Returns a dictionary of information on a user"""
        return irods.getUserInfo(self.conn, name)

    def mkdirR(self, targ_dir, targ_child_path):
        """Make a collection in iRODS"""
        irods.mkdirR(targ_dir, targ_child_path, 0750)

    def move_collection(self, path, new_path):
        """Move a collection in irods
        return True if the dest collection is already present"""
        dataObjRenameInp = irods.dataObjCopyInp_t()
        srcDataObj = dataObjRenameInp.srcDataObjInp
        dstDataObj = dataObjRenameInp.destDataObjInp
        srcDataObj.oprType = irods.RENAME_COLL
        dstDataObj.oprType = irods.RENAME_COLL
        srcDataObj.objPath = path
        dstDataObj.objPath = new_path
        status = irods.rcDataObjRename(self.conn, dataObjRenameInp)
        return status

    def move_file(self, path, new_path, overwrite=False):
        """Move a file in irods
        return True if the file is already present"""
        if overwrite:
            self.delete_file(new_path)
        dataObjRenameInp = irods.dataObjCopyInp_t()
        srcDataObj = dataObjRenameInp.srcDataObjInp
        dstDataObj = dataObjRenameInp.destDataObjInp
        srcDataObj.oprType = irods.RENAME_DATA_OBJ
        dstDataObj.oprType = irods.RENAME_DATA_OBJ
        srcDataObj.objPath = path
        dstDataObj.objPath = new_path
        status = irods.rcDataObjRename(self.conn, dataObjRenameInp)
        return status == irods.CAT_NAME_EXISTS_AS_DATAOBJ

    def move_files(self, local_files, targCollection, overwrite=False):
        """Move a list of files from a collection to another irods collection
        local_files : list of paths (str)
        Returns a list of files which was already present"""
        already_there = []
        for local_file in local_files:
            coll_name, file_name, _ = local_file
            irods_path_src = coll_name + '/' + file_name
            irods_path_dst = targCollection + '/' + file_name
            exist = self.move_file(irods_path_src, irods_path_dst, overwrite)
            if exist:
                already_there.append(local_file)
        return already_there

    def new_collection(self, irods_path):
        """Make a new directory in iRods"""
        collCreateInp = irods.collInp_t()
        irods.addKeyVal(collCreateInp.condInput,
                        irods.RECURSIVE_OPR__KW,
                        "")
        collCreateInp.collName = irods_path
        status = irods.rcCollCreate(self.conn, collCreateInp)
        return status

    def open(self, path, resource, mode="r"):
        """Open a file in iRods, return an iRodsFile"""
        return irods.irodsOpen(self.conn, path, resource, mode)

    def read_file(self, irods_path, resc=None):
        """Read textual content from an iRODS file"""
        if resc:
            f = irods.irodsOpen(self.conn, irods_path, "r", resc)
        else:
            f = irods.irodsOpen(self.conn, irods_path, "r")
        if not f:
            return ""
        txt = f.read()
        f.close()
        return txt

    def rename_collection(self, irods_collection, new_name):
        """Rename a collection from irods
        irods_collection : path (str)"""
        dataObjRenameInp = irods.dataObjCopyInp_t()
        srcDataObj = dataObjRenameInp.srcDataObjInp
        dstDataObj = dataObjRenameInp.destDataObjInp
        srcDataObj.oprType = irods.RENAME_COLL
        dstDataObj.oprType = irods.RENAME_COLL
        srcDataObj.objPath = irods_collection
        dstDataObj.objPath = new_name
        return irods.rcDataObjRename(self.conn, dataObjRenameInp)

    def rename_file(self, file_info, new_name):
        """Rename a file from irods
        file_info : (collection, file, resource)
        new_name : str"""
        (collection, irods_file, _) = file_info
        dataObjRenameInp = irods.dataObjCopyInp_t()
        srcDataObj = dataObjRenameInp.srcDataObjInp
        dstDataObj = dataObjRenameInp.destDataObjInp
        srcDataObj.oprType = irods.RENAME_DATA_OBJ
        dstDataObj.oprType = irods.RENAME_DATA_OBJ
        srcDataObj.objPath = collection + '/' + irods_file
        dstDataObj.objPath = collection + '/' + new_name
        return irods.rcDataObjRename(self.conn, dataObjRenameInp)

    def replicate_file(self, file_info, dst_resource):
        """Replicate a file in irods
        file_info : (collection, file, resource)
        dst_resource : str"""
        (collection, irods_file, src_resource) = file_info
        dataObjInp = irods.dataObjInp_t()
        d = irods.getFileInfo(self.conn, collection, irods_file, src_resource)
        cond_inp = dataObjInp.condInput
        irods.addKeyVal(cond_inp, irods.REPL_NUM_KW, d['data_repl_num'])
        irods.addKeyVal(cond_inp, irods.RESC_NAME_KW, src_resource)
        irods.addKeyVal(cond_inp, irods.DEST_RESC_NAME_KW, dst_resource)
        dataObjInp.objPath = collection + '/' + irods_file
        status = irods.rcDataObjRepl(self.conn, dataObjInp)
        return status

    def rm_collection_metadata(self, irods_path, name, value, units=''):
        """Remove metadatas from a collection"""
        return irods.rmCollUserMetadata(self.conn, irods_path, name, value,
                                        units)

    def rm_file_metadata(self, irods_path, name, value, units=''):
        """Remove metadatas from a file"""
        return irods.rmFileUserMetadata(self.conn, irods_path, name, value,
                                        units)

    def rodsErrorName(self, errorCode):
        """Return the name for an IRODS error code"""
        myErrName, mySubErrName = irods.rodsErrorName(errorCode)
        return myErrName, mySubErrName

    def save_file(self, irods_path, txt, resc=None):
        """Save textual content to an iRODS file"""
        if resc:
            f = irods.irodsOpen(self.conn, irods_path, "w", resc)
        else:
            f = irods.irodsOpen(self.conn, irods_path, "w")
        if not f:
            return
        f.write(txt)
        f.close()

    def split_path_by_key(self, path, key):
        """Split an iRODS path to obtain the collection name and the data
        object name"""
        col_path, filename, status = irods.splitPathByKey(path, key)
        if status == 0:
            return (col_path, filename)
        else:
            return (path, '')

    def upload_file(self, local_path, irods_path, resource=None,
                    overwrite=False):
        """Upload a file to irods
        return True if the file is already present"""
        dataObjOprInp = irods.dataObjInp_t()
        dataObjOprInp.oprType = irods.PUT_OPR
        dataObjOprInp.openFlags = irods.O_RDWR
        if overwrite:
            irods.addKeyVal(dataObjOprInp.condInput, irods.FORCE_FLAG_KW, "")
        if resource:
            irods.addKeyVal(dataObjOprInp.condInput,
                            irods.DEST_RESC_NAME_KW,
                            resource)
        dataObjOprInp.objPath = irods_path
        status = irods.rcDataObjPut(self.conn, dataObjOprInp, local_path)
        return status == irods.OVERWRITE_WITHOUT_FORCE_FLAG


class Config(object):
    """Keep the main configuration options of the application
    (global constants)
    Most of the options are parsed from the config.ini file with the
    ConfigParser module"""

    # script_dir: From where the script is launched
    # config_file: path of the configuration file
    def __init__(self, script_dir, config_file, ms_file, session_var_filename,
                 var_sets_filename, rule_filename, use_irods=True):
        self.script_dir = script_dir
        # The different sets of options in the .ini file
        ir_opt = 'iRods Options'
        main_opt = 'Main Options'
        config = ConfigParser.ConfigParser()
        config.read(config_file)

        #################
        # Main options #
        #################

        self.app_version = config.get(main_opt, "version")

        #################
        # iRods options #
        #################

        self.quick_connect = config.getboolean(ir_opt, "quick_connect")
        self.use_irods = use_irods
        self.password = None
        self.irods_username = config.get(ir_opt, "username")
        self.irods_hostname = config.get(ir_opt, "hostname")
        self.irods_zone = config.get(ir_opt, "zone")
        self.irods_port = config.getint(ir_opt, "port")
        self.irods_path = config.get(ir_opt, "path")

        #################
        # Other parsers #
        #################

        self.python_parser = PythonParser()

    def get_bmp(self, bmp_name):
        """Get a png filename, create the full path of the image and return the
        wx.Bitmap object"""
        return wx.Bitmap(os.path.join(self.script_dir, 'interface', 'icons',
                                      bmp_name))

    def get_python_parser(self):
        """Return the python parser"""
        return self.python_parser

    def get_static_bmp(self, parent, bmp_name):
        """Get a png filename, create the full path of the image and return the
        wx.StaticBitmap object"""
        return wx.StaticBitmap(parent, -1, self.get_bmp(bmp_name))

    def set_irods_info(self, user, host, zone, port):
        """Update connection info for irods"""
        self.irods_username = user
        self.irods_hostname = host
        self.irods_zone = zone
        self.irods_port = port

    def set_password(self, obf_pass):
        """Set the obfuscated password we want to use through the interface"""
        self.password = obf_pass
