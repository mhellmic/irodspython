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

""""A set of dialogbox/frames (Created and modified from wxGlade)"""

import wx


class ConfirmCloseDialog(wx.Dialog):
    """A specific dialog to confirm closing"""

    def __init__(self,  parent):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        self.cfg = parent.cfg
        self.bitmap_1 = self.cfg.get_static_bmp(self, "warning2.png")
        self.label_1 = wx.StaticText(self, -1,
                        "Save changes to document before closing ?")
        self.label_2 = wx.StaticText(self, -1,
            "If you don't save, changes from the last save" +
            " will be permanently lost.")
        self.b_close = wx.Button(self, wx.ID_CLOSE, "Close without Saving")
        self.b_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.b_save = wx.Button(self, wx.ID_SAVE, "Save")
        self.label_1.SetMinSize((250, 40))
        self.label_1.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_2.SetMinSize((250, 40))
        self.do_layout()
        self.Bind(wx.EVT_BUTTON, self.end_modal, self.b_close)
        self.Bind(wx.EVT_BUTTON, self.end_modal, self.b_cancel)
        self.Bind(wx.EVT_BUTTON, self.end_modal, self.b_save)

    def end_modal(self, evt):
        """End the dialog box"""
        self.EndModal(evt.GetId())

    def do_layout(self):
        """Layout the dialog"""
        sz_main = wx.BoxSizer(wx.VERTICAL)
        sz_but = wx.BoxSizer(wx.HORIZONTAL)
        sz_infos = wx.BoxSizer(wx.HORIZONTAL)
        sz_label = wx.BoxSizer(wx.VERTICAL)
        sz_infos.Add(self.bitmap_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 20)
        sz_label.Add(self.label_1, 1, wx.TOP|wx.BOTTOM, 10)
        sz_label.Add(self.label_2, 1, wx.TOP|wx.BOTTOM, 10)
        sz_infos.Add(sz_label, 1, wx.ALL|wx.EXPAND, 10)
        sz_main.Add(sz_infos, 1, wx.EXPAND, 0)
        sz_but.Add(self.b_close, 0, wx.ALL, 5)
        sz_but.Add(self.b_cancel, 0, wx.ALL, 5)
        sz_but.Add(self.b_save, 0, wx.ALL, 5)
        sz_main.Add(sz_but, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 15)
        self.SetSizer(sz_main)
        sz_main.Fit(self)
        self.Layout()


class ConfirmReplaceDialog(wx.Dialog):
    """A dialog to confirm overwriting a file"""

    def __init__(self,  parent, title, txt):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION,
                                       wx.ART_CMN_DIALOG, (64,64))
        self.bmp = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        self.lbl_txt = wx.StaticText(self, -1, txt)
        self.b_yes = wx.Button(self, wx.ID_YES, "Yes")
        self.b_yes_all = wx.Button(self, wx.ID_YESTOALL, "Yes to All")
        self.b_no = wx.Button(self, wx.ID_NO, "No")
        self.b_no_all = wx.Button(self, wx.ID_NOTOALL, "No to All")
        self.SetTitle(title)
        self.do_layout()
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.b_yes)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.b_yes_all)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.b_no)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.b_no_all)

    def do_layout(self):
        """Layout the dialog"""
        sz_dlg = wx.BoxSizer(wx.VERTICAL)
        sz_but = wx.BoxSizer(wx.HORIZONTAL)
        sz_main = wx.BoxSizer(wx.HORIZONTAL)
        sz_main.Add(self.bmp, 0, 0, 0)
        sz_main.Add(self.lbl_txt, 0, 0, 0)
        sz_dlg.Add(sz_main, 1, wx.ALL | wx.EXPAND, 10)
        sz_but.Add(self.b_yes, 0, wx.ALL, 5)
        sz_but.Add(self.b_yes_all, 0, wx.ALL, 5)
        sz_but.Add(self.b_no, 0, wx.ALL, 5)
        sz_but.Add(self.b_no_all, 0, wx.ALL, 5)
        sz_dlg.Add(sz_but, 1,
                   wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL,
                   20)
        self.SetSizer(sz_dlg)
        sz_dlg.Fit(self)
        self.Layout()

    def OnClick(self, evt):
        """Click on any of the button"""
        self.EndModal(evt.GetId())


class ConnectionDialog(wx.Dialog):
    """The dialog box for a connection to a server"""

    def __init__(self, config, username, hostname, zone, port, password):
        self.ID_CONNECT = wx.NewId()
        wx.Dialog.__init__(self, None, -1, "iRODS Login", size=(430, 200),
                          style=wx.SYSTEM_MENU | wx.CAPTION)
        self.label_5 = wx.StaticText(self, -1, "Name :", style=wx.ALIGN_RIGHT)
        self.tc_name = wx.TextCtrl(self, -1, username)
        self.label_6 = wx.StaticText(self, -1, "Host:", style=wx.ALIGN_RIGHT)
        self.tc_host = wx.TextCtrl(self, -1, hostname)
        self.label_7 = wx.StaticText(self, -1, "Zone:", style=wx.ALIGN_RIGHT)
        self.tc_zone = wx.TextCtrl(self, -1, zone)
        self.label_8 = wx.StaticText(self, -1, "Port:", style=wx.ALIGN_RIGHT)
        self.tc_port = wx.TextCtrl(self, -1, port)
        self.label_9 = wx.StaticText(self, -1, "Password:",
                                     style=wx.ALIGN_RIGHT)
        self.tc_password = wx.TextCtrl(self, -1, password,
                                       style=wx.TE_PASSWORD)
        self.b_conn = wx.Button(self, wx.ID_OK, "Connect")
        self.b_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.b_conn.SetDefault()
        self.cfg = config
        self.set_properties()
        self.do_layout()
        self.Bind(wx.EVT_BUTTON, self.OnButtonConnect, self.b_conn)

    def OnButtonConnect(self, event):
        """Click on the connect button"""
        if not self.tc_port.GetValue().isdigit():
            error(self, "The port number should be an integer value")
            self.tc_port.SetValue(str(self.cfg.irods_port))
        else:
            self.cfg.irods_username = self.tc_name.GetValue().encode("ascii")
            self.cfg.irods_hostname = self.tc_host.GetValue().encode("ascii")
            self.cfg.irods_zone = self.tc_zone.GetValue().encode("ascii")
            self.cfg.irods_port = int(self.tc_port.GetValue())
            event.Skip()

    def set_properties(self):
        """Set some properties for the components"""
        self.tc_name.SetMinSize((200, 27))
        self.tc_host.SetMinSize((200, 27))
        self.tc_zone.SetMinSize((200, 27))
        self.tc_port.SetMinSize((200, 27))
        self.tc_password.SetMinSize((200, 27))

    def do_layout(self):
        """Layout the dialog"""
        sz_main = wx.BoxSizer(wx.VERTICAL)
        sz_but = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_main = wx.FlexGridSizer(5, 2, 0, 0)
        grid_sizer_main.Add(self.label_5, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.tc_name, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.label_6, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.tc_host, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.label_7, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.tc_zone, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.label_8, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.tc_port, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.label_9, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        grid_sizer_main.Add(self.tc_password, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        sz_main.Add(grid_sizer_main, 6, wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 10)
        sz_but.Add(self.b_conn, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sz_but.Add(self.b_cancel, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sz_main.Add(sz_but, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 15)
        self.SetSizer(sz_main)
        sz_main.Fit(self)
        self.Layout()


class DialogAddMeta(wx.Dialog):
    """"A dialog box to add metadata"""

    def __init__(self, parent, name, value, units):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        self.st_title = wx.StaticText(self, -1, "Enter the new metadata",
                                      style=wx.ALIGN_CENTRE)
        self.st_name = wx.StaticText(self, -1, "Name :")
        self.tc_name = wx.TextCtrl(self, -1, "")
        self.st_value = wx.StaticText(self, -1, "Value :")
        self.tc_value = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.st_units = wx.StaticText(self, -1, "Units :")
        self.tc_units = wx.TextCtrl(self, -1, "")
        self.static_line_1 = wx.StaticLine(self, -1)
        self.b_ok = wx.Button(self, wx.ID_OK, "Ok")
        self.b_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.set_properties()
        self.do_layout()
        self.tc_name.SetValue(name)
        self.tc_value.SetValue(value)
        self.tc_units.SetValue(units)

    def do_layout(self):
        """Layout the dialog"""
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.st_title, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_2.Add(self.st_name, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_2.Add(self.tc_name, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_1.Add(sizer_2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_3.Add(self.st_value, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_3.Add(self.tc_value, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_1.Add(sizer_3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_4.Add(self.st_units, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_4.Add(self.tc_units, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_1.Add(sizer_4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_1.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_5.Add(self.b_ok, 0, wx.ALL, 20)
        sizer_5.Add(self.b_cancel, 0, wx.ALL, 20)
        sizer_1.Add(sizer_5, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def get_name(self):
        """Return the text control value for the name"""
        return self.tc_name.GetValue().encode("ascii")

    def get_units(self):
        """Return the text control value for the unit"""
        return self.tc_units.GetValue().encode("ascii")

    def get_value(self):
        """Return the text control value for the value"""
        return self.tc_value.GetValue().encode("ascii")

    def set_properties(self):
        """Set some properties for the components"""
        self.SetTitle("New Metadata")
        self.st_title.SetFont(wx.Font(14, wx.ROMAN, wx.NORMAL, wx.BOLD, 0, ""))
        self.st_name.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.tc_name.SetMinSize((180, 27))
        self.st_value.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.tc_value.SetMinSize((180, 108))
        self.st_units.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.tc_units.SetMinSize((180, 27))


class SingleChoiceDialog(wx.Dialog):
    """A single choice box dialog"""

    def __init__(self, parent, title, text, choices):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        self.text = wx.StaticText(self, -1, text, style=wx.ALIGN_CENTRE)
        self.lb_choice = wx.ListBox(self, -1, choices=choices, style=wx.LB_SINGLE)
        self.b_ok = wx.Button(self, wx.ID_OK, "Ok")
        self.b_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.title = title
        self.set_properties()
        self.do_layout()

    def do_layout(self):
        """Layout the dialog"""
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.text, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_1.Add(self.lb_choice, 1, wx.ALL|wx.EXPAND, 5)
        sizer_2.Add(self.b_ok, 0, wx.ALL, 10)
        sizer_2.Add(self.b_cancel, 0, wx.ALL, 10)
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def GetStringSelection(self):
        """Get the value"""
        return self.lb_choice.GetStringSelection()

    def set_properties(self):
        """Set some properties for the components"""
        self.SetTitle(self.title)
        self.lb_choice.SetSelection(0)


class UserInfoFrame(wx.Frame):
    """A frame to display information on a user"""

    def __init__(self, config, name, group, uid, zone, comment, info, creation,
                 modif):
        wx.Frame.__init__(self, None, -1, style=wx.DEFAULT_FRAME_STYLE)
        self.name = name
        self.SetTitle("Information for user : %s" % self.name)
        self.comment = comment
        self.info = info
        self.bitmap_1 = config.get_static_bmp(self, "user_big.png")
        self.st_name = wx.StaticText(self, -1, "%s (%s)" % (name, group))
        self.st_id = wx.StaticText(self, -1, "Id : %s - Zone : %s" % (uid, zone))
        self.st_comment = wx.StaticText(self, -1, comment)
        self.st_userinfo = wx.StaticText(self, -1, info)
        self.st_creation = wx.StaticText(self, -1, "Creation : %s - Modification : %s" % (creation, modif))
        self.do_layout()

    def do_layout(self):
        """Layout the dialog"""
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.bitmap_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(self.st_name, 0, wx.TOP|wx.BOTTOM, 10)
        sizer_4.Add(self.st_id, 0, wx.TOP|wx.BOTTOM, 10)
        sizer_3.Add(sizer_4, 1, wx.ALL|wx.EXPAND, 20)
        sizer_2.Add(sizer_3, 1, wx.LEFT|wx.RIGHT, 20)
        if self.comment:
            sizer_2.Add(self.st_comment, 0, wx.ALL, 10)
        if self.info:
            sizer_2.Add(self.st_userinfo, 0, wx.ALL, 10)
        sizer_2.Add(self.st_creation, 0, wx.ALL, 10)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()


def error(parent, message):
    """An error message"""
    dlg = wx.MessageDialog(parent, message, 'Error', wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()


def information(parent, message):
    """An information message"""
    dlg = wx.MessageDialog(parent, message, 'Information', wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


def irodsError(mdl, errorCode):
    """An irods error message with the irods error code"""
    myErrName, mySubErrName = mdl.rodsErrorName(errorCode)
    error(None, "irods error: %d %s %s" % (errorCode, myErrName, mySubErrName))

