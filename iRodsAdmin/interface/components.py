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

"""Specific components for the application"""

import wx
import wx.lib.mixins.listctrl as listmix
import os
import cPickle


DESIGN_SELECT_MODE = "select_mode"
DESIGN_ARROW_MODE = "arrow_mode"
DESIGN_DOTLINE_MODE = "dotted_line_mode"
DESIGN_UNKNOWN_MODE = "Unknown mode"


class AutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """"A list control with auto width activated for the columns"""

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class CollectionDropTarget(wx.PyDropTarget):
    """The drop target for the tree collection control (used for drag&drop
    support)"""

    def __init__(self, window):
        wx.PyDropTarget.__init__(self)
        self.window = window
        self.mdl = self.window.mdl
        self.do = wx.DataObjectComposite()
        self.data = wx.CustomDataObject("selFiles")
        self.filedo = wx.FileDataObject()
        self.do.Add(self.filedo)
        self.do.Add(self.data)
        self.SetDataObject(self.do)

    def OnData(self, x, y, d):
        """Called when a data object is dropped on the tree"""
        if self.GetData():
            df = self.do.GetReceivedFormat().GetType()
            if df == wx.DF_PRIVATE:  # for wx.CustomDataObject("selFiles")
                coll_path_dst = self.window.get_dropped_collection(x, y)
                # convert the data back to a list of files or directory
                drag_data = self.data.GetData()
                drag_struct = cPickle.loads(drag_data)
                file_list = drag_struct.get('files', [])
                coll_path_src = drag_struct.get('dir', None)
                if file_list:
                    self.window.move_files(file_list, coll_path_dst)
                if coll_path_src:
                    # Add the basename to the destination path
                    base = coll_path_src.split('/')[-1][:-1]
                    coll_path_dst = coll_path_dst + '/' + base
                    self.window.move_collection(coll_path_src, coll_path_dst)
            elif df == wx.DF_FILENAME:
                filenames = self.filedo.GetFilenames()
                coll_path_dst = self.window.get_dropped_collection(x, y)
                self.window.upload_paths(filenames, coll_path_dst)
                self.window.populate_collection_tree(coll_path_dst)
        return d


class CollectionTreeCtrl(wx.TreeCtrl):
    """A tree control for iRODS collections"""

    def __init__(self, parent, _id=-1, style=wx.TR_DEFAULT_STYLE,
                 allow_drag=False):
        wx.TreeCtrl.__init__(self, parent, _id, style=style)
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,
                                                       wx.ART_OTHER,
                                                       isz))
        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,
                                                           wx.ART_OTHER,
                                                           isz))
        self.fileidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE,
                                                       wx.ART_OTHER,
                                                       isz))
        self.SetImageList(il)
        self.il = il
        self.parent = parent
        if allow_drag:
            self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnStartDrag)

    def GetItemPathPos(self, x, y):
        """Return the item data associated to the x,y position in the
        control"""
        item_id, _ = self.HitTest((x, y))
        return self.GetPyData(item_id)

    def OnStartDrag(self, evt):
        """Called when a data object is dragged from the control"""
        drag_infos = {'files': [],
                      'dir': self.parent.get_selected_collection()}
        drag_struct = cPickle.dumps(drag_infos, 1)
        drag_data = wx.CustomDataObject("selFiles")
        drag_data.SetData(drag_struct)
        tds = wx.DropSource(self)
        tds.SetData(drag_data)
        tds.DoDragDrop(True)


class FileBrowser(wx.TreeCtrl):
    """The GenericDirCtrl components is too slow at the instantiation. I
    prefer this lighter version (it will probably not work on every system)"""

    def __init__(self, parent, id=-1, style=wx.TR_DEFAULT_STYLE):
        wx.TreeCtrl.__init__(self, parent, id, style=style)
        self.parent = parent
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,
                                                       wx.ART_OTHER,
                                                       isz))
        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,
                                                           wx.ART_OTHER,
                                                           isz))
        self.fileidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE,
                                                       wx.ART_OTHER,
                                                       isz))
        self.harddisk = il.Add(wx.ArtProvider_GetBitmap(wx.ART_HARDDISK,
                                                        wx.ART_OTHER,
                                                        isz))
        self.SetImageList(il)
        self.il = il
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.populate()

    def OnMouseEvent(self, event):
        """Track mouse events to expand/collapse an element"""
        if event.LeftDown() and not self.HasFlag(wx.TR_MULTIPLE):
            ht_item, ht_flags = self.HitTest(event.GetPosition())
            if (ht_flags & wx.TREE_HITTEST_ONITEM) != 0:
                self.SetFocus()
                if self.IsExpanded(ht_item):
                    self.Collapse(ht_item)
                else:
                    self.SelectItem(ht_item)
                    self.expand_item(ht_item)
            else:
                event.Skip()
        else:
            event.Skip()

    def expand_item(self, item):
        """Expand an item of the tree control (parse a local dir)"""
        sel_path = self.GetPyData(item)
        # Delete the previous children (in case of update)
        self.DeleteChildren(item)
        try:
            paths = [(p, sel_path + os.sep + p)
                     for p in os.listdir(sel_path)
                     if os.path.isdir(sel_path + os.sep + p)]
            paths.sort()
        except OSError:
            paths = []
        for name, _ in paths:
            child = self.AppendItem(item, name)
            self.SetPyData(child, sel_path + os.sep + name)
            self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.fldropenidx,
                              wx.TreeItemIcon_Expanded)
        self.Expand(item)

    def GetItemPathPos(self, x, y):
        """Return the item data associated to the x,y position in the
        control"""
        item_id, _ = self.HitTest((x, y))
        return self.GetPyData(item_id)

    def populate(self):
        """Populate the tree control"""
        if wx.Platform == '__WXMSW__':
            root_path = "c:\\"
        elif wx.Platform == '__WXGTK__':
            root_path = "/"
        else:
            # OSX ?
            # Need additional testing with MS Windows
            return
        self.DeleteAllItems()
        root = self.AddRoot(root_path)
        self.SetPyData(root, root_path)
        self.SetItemImage(root, self.harddisk, wx.TreeItemIcon_Normal)
        paths = [(p, root_path + p)
                 for p in os.listdir(root_path)
                 if os.path.isdir(root_path + p)]
        paths.sort()
        for name, path in paths:
            child = self.AppendItem(root, name)
            self.SetPyData(child, path)
            self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.fldropenidx,
                              wx.TreeItemIcon_Expanded)
        self.Expand(root)


class FileListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """A list control with auto width activated for the columns"""

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.parent = parent
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnStartDrag)

    def OnStartDrag(self, e):
        """Called when a data object is dragged from the control"""
        drag_infos = {'files': self.parent.get_selected_files(),
                      'dir': []}
        drag_struct = cPickle.dumps(drag_infos, 1)
        drag_data = wx.CustomDataObject("selFiles")
        drag_data.SetData(drag_struct)
        tds = wx.DropSource(self)
        tds.SetData(drag_data)
        tds.DoDragDrop(True)


class FileListDropTarget(wx.FileDropTarget):
    """The drop target for the file list control (used for drag&drop
    support)"""

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.mdl = self.window.mdl

    def OnDropFiles(self, x, y, filenames):
        """Called when a data object is dropped on the list"""
        cur_coll = self.window.get_selected_collection()
        filenames = [f.encode("ascii") for f in filenames]
        self.window.upload_paths(filenames, cur_coll)
        self.window.populate_collection_tree(cur_coll)


class LocalDirDropTarget(wx.PyDropTarget):
    """The drop target for the local filesystem tree control (used for
    drag&drop support)"""

    def __init__(self, window):
        wx.PyDropTarget.__init__(self)
        self.window = window
        self.mdl = self.window.mdl
        self.data = wx.CustomDataObject("selFiles")
        self.SetDataObject(self.data)

    def OnData(self, x, y, d):
        """Called when a data object is dropped on the tree"""
        if self.GetData():
            local_dir = self.window.get_dropped_local_dir(x, y)
            # convert the data back to a list of files or directory
            drag_data = self.data.GetData()
            drag_struct = cPickle.loads(drag_data)
            file_list = drag_struct.get('files', [])
            coll_path = drag_struct.get('dir', None)
            if file_list:
                file_list = [((col + '/' + fi).encode("ascii"),
                              res,
                              (local_dir + os.sep + fi).encode("ascii"))
                             for (col, fi, res) in file_list]
                self.window.download_files(file_list)
            if coll_path:
                self.window.download_collection(coll_path, local_dir)
        return d
