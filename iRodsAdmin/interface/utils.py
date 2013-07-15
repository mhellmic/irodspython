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

"""Some useful functions"""

import wx


def create_menu(frame, menus_datas):
    """Create a menu

    @param frame: The parent frame of the menu
    @type frame: wx.Frame
    @param menus_datas: The menu ofr a specific element of the menubar
    @type menus_datas: see create_menubar
    @rtype: wx.Menu
    @return: The submenu for the element (File for instance)
    """
    items = {}
    menu = wx.Menu()
    for label, help_string, handler, is_checkable in menus_datas:
        if not label:
            menu.AppendSeparator()
        else:
            if is_checkable:
                menu_item = menu.AppendCheckItem(-1, label, help_string)
            else:
                menu_item = menu.Append(-1, label, help_string)
            items[label.replace('&', '')] = menu_item
            frame.Bind(wx.EVT_MENU, handler, menu_item)
    return menu, items


def create_menubar(frame, menubar_data):
    """Create a new menubar, informations are in the tuple menu_data

    @param frame: The parent frame of the menu
    @type frame: wx.Frame
    @param menubar_data: example for menu_data :
    (("&File", ("&Open", "Open in status bar", self.OnOpen, isCheckable),
               ("&Quit", "Quit", self.OnCloseWindow, isCheckable)),
     ("&Edit", ("&Copy", "Copy", self.OnCopy, isCheckable),
               ("", "", "", isCheckable),
               ("&Options...", "DisplayOptions", self.OnOptions, isCheckable)))
    """
    menu_items = {}
    menubar = wx.MenuBar()
    for data in menubar_data:
        label = data[0]
        menus_datas = data[1:]
        menu, items = create_menu(frame, menus_datas)
        menu_items[label.replace('&', '')] = items
        menubar.Append(menu, label)
    frame.SetMenuBar(menubar)

    return menu_items
