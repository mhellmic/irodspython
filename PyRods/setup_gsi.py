# Copyright (c) 2013, University of Liverpool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Author       : Jerome Fuselier

#!/usr/bin/env python


from distutils.core import setup, Extension

from distutils import sysconfig
save_init_posix = sysconfig._init_posix
def my_init_posix():
    ##print 'my_init_posix: changing gcc to g++'
    save_init_posix()
    g = sysconfig._config_vars
    g['CC'] = 'g++'
    g['LDSHARED'] = 'g++ -shared'
sysconfig._init_posix = my_init_posix

include_dirs = ['/lib/core/include', 
                '/lib/api/include', 
                '/lib/md5/include', 
                '/lib/sha1/include', 
                '/server/core/include', 
                '/server/icat/include',
                '/server/drivers/include', 
                '/server/re/include']

extra_objects = ['/lib/core/obj/libRodsAPIs.a']

irods = Extension("_irods",
                  sources=['irods_wrap.c'],
                  include_dirs=include_dirs,
                  library_dirs = ['/usr/local/globus-5.2.4/lib64'],
                  libraries=['globus_gss_assist', 'globus_gssapi_gsi',
                             'globus_gsi_credential', 'globus_gsi_proxy_core',
                             'globus_gsi_callback', 'globus_oldgaa',
                             'globus_gsi_sysconfig', 'globus_gsi_cert_utils',
                             'globus_openssl_error', 'globus_openssl',
                             'globus_proxy_ssl', 'ssl', 'crypto',
                             'globus_common', 'globus_callout', 'ltdl'],
                  extra_objects=extra_objects)

from distutils.command.build import build

class MyBuild(build):

    build.user_options.append( ('irods-dir=', ".", "irods directory") )
    
    def initialize_options (self):
        build.initialize_options(self)
        self.irods_dir = "."
        
    def finalize_options (self):
        build.finalize_options(self)
        for i in xrange(len(include_dirs)):
            include_dirs[i] = self.irods_dir + include_dirs[i]
            
        for i in xrange(len(extra_objects)):
            extra_objects[i] = self.irods_dir + extra_objects[i]

setup(name="PyRods", 
      version="3.3.4",
      author = "Jerome Fuselier",
      author_email = "jerome.fuselier@free.fr",
      license = "LGPL",
      description = 'python client API for iRODS',
      url="http://code.google.com/p/irodspython",
      cmdclass = { "build" : MyBuild },
      long_description = """The iRODS python project is an implementation of a 
client in python for the iRODS project. iRODS is an open source datagrid written 
in C. This project aims at the creation of a python binding to access the server 
from python scripts.""",
      platforms=["Linux"],
      ext_modules=[irods],
      py_modules = ["irods"])
