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

"""Application entry point"""

import sys
import os
import wx

from interface.main_frame import MainFrame
from interface.dialogs import ConnectionDialog, irodsError
from model.app_model import Config, AppModel


class MyApplication(wx.App):
    """The wx application"""

    def __init__(self, redirect=True, filename=None):
        """ Constructor
        @param redirect: Redirect the error logs in a file
        @type redirect: boolean
        @param filename: The file where the logs are redirected
        @type filename: string (a path)
        """
        self.mdl = None
        self.config = None
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        """ Initialize the application"""
        script_dir = sys.path[0]

        config_name = os.path.join(script_dir, 'config.ini')
        ms_name = os.path.join(script_dir, 'doc', 'microservices.ini')
        sess_var_name = os.path.join(script_dir, 'doc', 'session_variable.ini')
        var_sets_name = os.path.join(script_dir, 'doc', 'variable_sets.ini')
        rule_name = os.path.join(script_dir, 'doc', 'rules.ini')
        app_title = "iRods Admin"

        wx.InitAllImageHandlers()

        # The cfg variable stores some configuration variables for the
        # interface and for the connection to iRODS
        self.config = Config(script_dir, config_name, ms_name, sess_var_name,
                             var_sets_name, rule_name)
        self.mdl = AppModel(self.config)

        if self.config.quick_connect:
            # The quick init bypass the connection dialog box
            self.quick_init()
        else:
            self.init_conn_info()

        # If we don't want to work offline: Test the connection
        status = self.mdl.connect()
        if status != 0:
            irodsError(self.mdl, status)
            return 1

        main_frame = MainFrame(self.mdl, app_title)
        self.SetTopWindow(main_frame)
        main_frame.Show()

        return True

    def init_conn_info(self):
        """Display a connection dialog to select an iRods server to connect
        to"""
        status = -1
        model = self.mdl
        while status != 0:
            con_dlg = ConnectionDialog(self.config, self.config.irods_username,
                                       self.config.irods_hostname,
                                       self.config.irods_zone,
                                       str(self.config.irods_port), "")
            res = con_dlg.ShowModal()
            if res == wx.ID_CANCEL:
                sys.exit(0)
            elif res == wx.ID_OK:
                # If the user does not enter a password:
                #  -> we take the one from .irodsA
                if con_dlg.tc_password.GetValue() == "":
                    obf_password = model.get_password()
                else:
                    tc_pwd = con_dlg.tc_password.GetValue()
                    obf_password = model.encode(tc_pwd.encode("ascii"))
                self.config.set_password(obf_password)
                host = con_dlg.tc_host.GetValue().encode("ascii")
                port = int(con_dlg.tc_port.GetValue())
                user = con_dlg.tc_name.GetValue().encode("ascii")
                zone = con_dlg.tc_zone.GetValue().encode("ascii")
                status = model.connect_infos(host, port, user, zone)

            con_dlg.Destroy()
            if status != 0:
                irodsError(self.mdl, status)
            model.disconnect()

    def quick_init(self):
        """Use the information from the .irodsEnv file to connect to an iRods
        server"""
        self.config.set_password(self.mdl.get_password())

if __name__ == "__main__":
    # We can log the errors and the output of the console in a specific file
    log_file = False
    if log_file:
        app = MyApplication(redirect=True, filename='irodsAdmin.log')
    else:
        app = MyApplication(redirect=False)
    app.MainLoop()
    app.mdl.disconnect()
