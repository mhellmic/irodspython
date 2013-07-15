# Copyright (c) 2010, University of Liverpool
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
# Creation     : January, 2010

"""A class that manages the menu of the application"""

import wx
import os
from wx.lib.wordwrap import wordwrap


class AppMenu(object):
    """The application menu, It calls methods in the frame."""

    def __init__(self, parent, create_menu):
        self.frame = parent
        self.menu_items = create_menu()
        self.mdl = self.frame.mdl
        self.cfg = self.frame.cfg

    def about(self, name, version, website, website_name):
        """Display the about dialog box"""
        gpl_path = self.cfg.script_dir + os.sep + 'gpl.txt'
        f = open(gpl_path)
        licenseText = f.read()
        f.close()
        info = wx.AboutDialogInfo()
        info.Name = name
        info.Version = version
        info.Copyright = ""
        info.Description = wordwrap("", 350, wx.ClientDC(self.frame))
        info.WebSite = (website, website_name)
        info.Developers = ["Jerome Fuselier",
                           "University of Liverpool"]
        info.License = wordwrap(licenseText, 500, wx.ClientDC(self.frame))
        wx.AboutBox(info)

    def check_local_dir(self, checked):
        """Check the view local filesystem menu item"""
        self.check_menu_item("View", "Local Filesystem", checked)

    def check_menu_item(self, cat, item, checked):
        """Check a specific menu item"""
        if cat in self.menu_items:
            if item in self.menu_items[cat]:
                self.menu_items[cat][item].Check(checked)

    def enable_item(self, cat, item, enable):
        """Enable/Disable a menu item"""
        if cat in self.menu_items:
            if item in self.menu_items[cat]:
                self.menu_items[cat][item].Enable(enable)

    def is_checked(self, cat, item):
        """Check is a specific menu item is checked or not"""
        is_checked = True
        if cat in self.menu_items:
            if item in self.menu_items[cat]:
                is_checked = self.menu_items[cat][item].IsChecked()
        return is_checked

    def is_local_dir_checked(self):
        """Check if the local filesystem window menu is checked"""
        return self.is_checked("View", "Local Filesystem")
