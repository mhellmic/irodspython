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
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
#
# Author       : Jerome Fuselier
# Creation     : August, 2009

"""The main frame of the application"""

import sys

import wx
import wx.lib.ogl as ogl
import wx.aui as aui
import os
from interface.dialogs import UserInfoFrame, DialogAddMeta, error, irodsError
from interface.dialogs import SingleChoiceDialog
from interface.dialogs import ConfirmReplaceDialog

from interface.utils import create_menubar
from interface.components import AutoWidthListCtrl, FileListCtrl
from interface.components import FileListDropTarget, LocalDirDropTarget
from interface.components import FileBrowser, CollectionTreeCtrl
from interface.components import CollectionDropTarget
from interface.app_menu import AppMenu

from interface.editor import EditorFrame

# These ID are used for the toolbar
ID_HighValue = wx.ID_HIGHEST + 1

ID_Toolbar_DownloadF = ID_HighValue + 1
ID_Toolbar_UploadF = ID_HighValue + 2
ID_Toolbar_DownloadC = ID_HighValue + 3
ID_Toolbar_UploadC = ID_HighValue + 4
ID_Toolbar_Refresh = ID_HighValue + 5
ID_Toolbar_UserInfo = ID_HighValue + 6


class MainFrame(wx.Frame):
    """The main frame of the application.
    The frame is managed from aui, it allows the creation of perspective (like
    eclipse), with specific toolbars/components for each perspective"""
    
    
    def __init__(self, model, title, pos=(0, 0), size=(1000, 1000),
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, None, -1, title, pos, size, style)
        
        # This creates some pens and brushes that the OGL library uses.
        ogl.OGLInitialize()
        
        # tell the aui FrameManager to manage this frame
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        
        # The model of the application
        self.mdl = model
        # The config of the application (variables, parsers, ...)        
        self.cfg = model.get_config()
        # Title of the frame
        self.title = title
        # The perspectives created with aui
        self._perspectives = {}
        self.cur_sel = None
        self.files_pydata = {}
        self.col_item = None

        self.cur_persp = 'treeview'
        self.menu = AppMenu(self, self.create_menu_admin)

        self.statusbar = None
        self.create_statusbar()

        ###############################
        # Create the common controls ##
        ###############################
        
        # The list control for information on files for a collection
        self.lc_data = FileListCtrl(self, -1, style=wx.LC_REPORT 
                                                    | wx.LC_SORT_ASCENDING
                                                    | wx.LC_VRULES
                                                    | wx.LC_HRULES)
        
        # The list control for metadata information on a file
        self.lc_meta_file = AutoWidthListCtrl(self, -1, style=wx.LC_REPORT 
                                                    | wx.LC_SORT_ASCENDING
                                                    | wx.LC_SINGLE_SEL
                                                    | wx.LC_VRULES
                                                    | wx.LC_HRULES)
        
        # The list control for metadata information on a collection
        self.lc_meta_collection = AutoWidthListCtrl(self, -1, 
                                                    style=wx.LC_REPORT 
                                                        | wx.LC_SORT_ASCENDING
                                                        | wx.LC_SINGLE_SEL
                                                        | wx.LC_VRULES
                                                        | wx.LC_HRULES)
           
        # The tree control for collection hierarchy
        self.tc_collection = CollectionTreeCtrl(self, allow_drag=True)
        
        #The tree for the local filesystem (drag&drop support)
        self.tc_local = FileBrowser(self)
        
        self.cb_resc = None
        # Toolbar for input/output (upload, download, ... - tree perspective)
        self.tb_io = self.create_toolbar_io()
        # Toolbar for information on iRODS system (user)
        self.tb_infos = self.create_toolbar_infos()
        
        # Add information in controls (in online mode only)
        self.populate_collection_tree(self.mdl.get_current_dir())
        self.populate_data_list(self.mdl.get_current_dir())
            
            
        ################        
        # Drag & Drop ##
        ################        
        
        # Add Drag and Drop support in the file list control   
        dt = FileListDropTarget(self)
        self.lc_data.SetDropTarget(dt)
        
        # Add Drag and Drop support in the local filesystem tree control
        dt = LocalDirDropTarget(self)
        self.tc_local.SetDropTarget(dt)
        
        # Add Drag and Drop support in the collection tree control
        dt = CollectionDropTarget(self)
        self.tc_collection.SetDropTarget(dt)
        
        
        ######################        
        # Aui frame manager ##
        ######################
        
        # Add all components to the frame manager
        
        self._mgr.AddPane(self.tc_collection, aui.AuiPaneInfo().
                          Name("collTree").Left().BestSize((200, 100)).
                          Caption("Collection Tree").CloseButton(False))
        
        self._mgr.AddPane(self.tc_local, aui.AuiPaneInfo().Name("localTree").
                          Right().BestSize((200, 100)).Caption("Local Tree").
                          CloseButton(True))
        
        self._mgr.AddPane(self.lc_data, aui.AuiPaneInfo().Center().
                          Name("fileList").Caption("Files").CloseButton(False))
        
        self._mgr.AddPane(self.tb_infos, aui.AuiPaneInfo().Name("tbinfo").
                          Caption("Information Toolbar").ToolbarPane().Top().
                          CloseButton(False))
        
        self._mgr.AddPane(self.tb_io, aui.AuiPaneInfo().Name("tbio").
                          Caption("IO Toolbar").ToolbarPane().Top().
                          CloseButton(False))

        self._mgr.AddPane(self.lc_meta_file, aui.AuiPaneInfo().Bottom().
                          Name("metaFile").Caption("File metadata").
                          CloseButton(False).BestSize((200, 200)))

        self._mgr.AddPane(self.lc_meta_collection, aui.AuiPaneInfo().Bottom().
                          Name("metaColl").Caption("Collection metadata").
                          CloseButton(False).BestSize((200, 200)))

        # Create some perspectives
        all_panes = self._mgr.GetAllPanes()

        # The tree view perspective with collection hierarchy, file information
        # and metadata information

        # Hide everything (even toolbar)
        for ii in xrange(len(all_panes)):
            all_panes[ii].Hide()

        self._mgr.GetPane("collTree").Show() 
        self._mgr.GetPane("fileList").Show() 
        self._mgr.GetPane("tbinfo").Show() 
        self._mgr.GetPane("tbio").Show()
        self._mgr.GetPane("metaFile").Show() 
        self._mgr.GetPane("metaColl").Show()
        self._mgr.Update()
        self._perspectives['treeview'] = self._mgr.SavePerspective()

        self._mgr.LoadPerspective(self._perspectives[self.cur_persp])

        ###################
        # Events binding ##
        ###################

        self.Bind(wx.EVT_CLOSE, self.OnMenu_Close)
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSel_Coll, self.tc_collection)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRC_Coll, 
                  self.tc_collection)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSel_File, self.lc_data)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDesel_File, self.lc_data)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRC_File, self.lc_data)
        self.lc_data.Bind(wx.EVT_LEFT_DCLICK, self.OnDC_File)

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRC_CollMeta, 
                  self.lc_meta_collection)

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRC_FileMeta, 
                  self.lc_meta_file)

        # I/O toolbar
        self.Bind(wx.EVT_TOOL, self.OnTool_DownFile, id=ID_Toolbar_DownloadF)
        self.Bind(wx.EVT_TOOL, self.OnTool_UpFile, id=ID_Toolbar_UploadF)
        self.Bind(wx.EVT_TOOL, self.OnTool_DownCollection, 
                  id=ID_Toolbar_DownloadC)
        self.Bind(wx.EVT_TOOL, self.OnTool_UpCollection, id=ID_Toolbar_UploadC) 
        self.Bind(wx.EVT_TOOL, self.OnTool_Refresh, id=ID_Toolbar_Refresh)

        # User Toolbar 
        self.Bind(wx.EVT_TOOL, self.OnTool_UserInfo, id=ID_Toolbar_UserInfo)

    def OnDC_File(self, evt):
        """Left double click on an element of the file list to edit the file"""
        path, filename, resc = self.files_pydata[self.cur_sel]
        
        # For known file types we open the editor
        if filename.endswith(".py") or \
           filename.endswith(".txt") or \
           filename.endswith(".ir") or \
           filename.endswith(".irb"):  
            frame = EditorFrame(self, self.mdl, path, filename, resc)
            frame.Show()
        
        evt.Skip()
        
        
    def OnDesel_File(self, evt):
        """Deselect a file in the list data"""
        # If no file is selected, disable the download file tool
        if self.lc_data.GetSelectedItemCount() == 0:
            self.tb_io.EnableTool(ID_Toolbar_DownloadF, False)
          
      
    def OnMenu_About(self, evt):
        """Display the about menu"""
        if self.mdl.get_offline():
            self.menu.about("PyRuleDesigner ", self.cfg.app_version, 
                "http://code.google.com/p/irodspython/wiki/PyRuleDesigner", 
                "PyRuleDesigner homepage")
        else:
            self.menu.about("PyRodsAdmin ", self.cfg.app_version, 
                "http://code.google.com/p/irodspython/wiki/PyRodsAdmin", 
                "PyRodsAdmin homepage")

    def OnMenu_Close(self, evt):
        """Close the application"""
        self.Destroy()

    def OnMenu_LocalFilesystem(self, evt):
        """Display or hide the local file system tree control"""
        if self.menu.is_local_dir_checked():
            self._mgr.GetPane("localTree").Show()
        else:
            self._mgr.GetPane("localTree").Hide()
        self._mgr.Update()

    def OnPaneClose(self, evt):
        """Close a panel of the aui manager"""
        name = evt.GetPane().name

        if name == "localTree":
            # Update the menu accordingly
            self.menu.check_local_dir(False)

    def OnPop_CollCopyPath(self, evt):
        """Put the selected irods path in the clipboard"""
        clipdata = wx.TextDataObject()
        clipdata.SetText(self.get_selected_collection())
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()

    def OnPop_CollDelete(self, evt):
        """Delete the selected collection"""
        msg = "This will delete the directory and its content recursively.\n"
        msg += "Do you want to continue ?"
        dlg = wx.MessageDialog(self, msg, 'Information',
                                wx.ICON_INFORMATION | wx.YES_NO)
        res = dlg.ShowModal()
        dlg.Destroy()
        if res == wx.ID_YES:
            col_path = self.tc_collection.GetPyData(self.col_item)
            self.mdl.delete_collection(col_path)
            self.refresh_data_list()
            self.tc_collection.Delete(self.col_item)

    def OnPop_CollDownload(self, evt):
        """Download a collection (and its content)"""
        curr_name = self.tc_collection.GetPyData(self.col_item)
        self.download_collection_dlg(curr_name)

    def OnPop_CollMetaAdd(self, evt):
        """Add metadata for an irods collection"""
        name = ""
        value = ""
        units = ""
        valid_entry = False
        cancel = False

        while not valid_entry and not cancel:
            dlg = DialogAddMeta(self, name, value, units)
            res = dlg.ShowModal()
            name = dlg.get_name()
            value = dlg.get_value()
            units = dlg.get_units()
            cancel = res != wx.ID_OK
            valid_entry = (name != '' and value != '')
            if not valid_entry and not cancel:
                error(self, "The name and value fields are mandatory")
            dlg.Destroy()

        if not cancel:
            irods_path = self.get_selected_collection()
            self.mdl.add_collection_metadata(irods_path, name, value, units)
            self.populate_metadata_collection(irods_path)

    def OnPop_CollMetaDel(self, evt):
        """Remove a metadata for an irods collection"""
        item = self.cur_sel
        lc_meta = self.lc_meta_collection
        name = lc_meta.GetItemText(item).encode("ascii")
        value = lc_meta.GetItem(item, 1).GetText().encode("ascii")
        units = lc_meta.GetItem(item, 2).GetText().encode("ascii")
        irods_path = self.get_selected_collection()
        self.mdl.rm_collection_metadata(irods_path, name, value, units)
        self.populate_metadata_collection(irods_path)

    def OnPop_CollNewCollection(self, evt):
        """Create a new collection in irods"""
        dlg = wx.TextEntryDialog(self, 'Enter the name of the collection : ',
                                 'New Collection',
                                 "New Collection")
        if dlg.ShowModal() == wx.ID_OK:
            root_path = self.tc_collection.GetPyData(self.col_item)
            new_name = root_path + '/' + dlg.GetValue()
            new_name = new_name.encode("ascii")
            tree = self.tc_collection
            self.mdl.new_collection(new_name)
            item = self.tc_collection.AppendItem(self.col_item, dlg.GetValue())
            self.tc_collection.SetPyData(item, new_name)
            self.tc_collection.SetItemImage(item, tree.fldridx,
                                            wx.TreeItemIcon_Normal)
            self.tc_collection.SetItemImage(item, tree.fldropenidx,
                                            wx.TreeItemIcon_Expanded)
        dlg.Destroy()

    def OnPop_CollRename(self, evt):
        """Rename a collection"""
        dlg = wx.TextEntryDialog(self,
                                 'Enter the new name for the collection : ',
                                 'Change Name',
                                 self.tc_collection.GetItemText(self.col_item))
        if dlg.ShowModal() == wx.ID_OK:
            curr_name = self.tc_collection.GetPyData(self.col_item)
            old_name = self.tc_collection.GetItemText(self.col_item)
            new_name = curr_name.replace(old_name, dlg.GetValue())
            new_name = new_name.encode("ascii")
            self.mdl.rename_collection(curr_name, new_name)
            self.tc_collection.SetItemText(self.col_item, dlg.GetValue())
            self.tc_collection.SetPyData(self.col_item, new_name)
            self.refresh_data_list()
        dlg.Destroy()

    def OnPop_FileCopyPath(self, evt):
        """Put the current irods object path in the clipboard"""
        tmp = self.files_pydata[self.cur_sel]
        clipdata = wx.TextDataObject()
        clipdata.SetText('/'.join([tmp[0], tmp[1]]))
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()

    def OnPop_FileDelete(self, evt):
        """Delete selected file(s)"""
        msg = "This will delete all selected files.\n"
        msg += "Do you want to continue ?"
        dlg = wx.MessageDialog(self, msg, 'Information',
                                wx.ICON_INFORMATION | wx.YES_NO)
        res = dlg.ShowModal()
        dlg.Destroy()
        if res == wx.ID_YES:
            self.mdl.delete_files(self.get_selected_files())
            self.refresh_data_list()

    def OnPop_FileDownload(self, evt):
        """Download the selected file"""
        sel_item = self.files_pydata[self.cur_sel]
        self.download_files_dlg([sel_item])

    def OnPop_FileEditor(self, evt):
        """Edit the selected file"""
        path, filename, resc = self.files_pydata[self.cur_sel]
        frame = EditorFrame(self, self.mdl, path, filename, resc)
        frame.Show()

    def OnPop_FileMetaAdd(self, evt):
        """Add metadata to the selected file"""
        name = ""
        value = ""
        units = ""
        valid_entry = False
        cancel = False

        while not valid_entry and not cancel:
            dlg = DialogAddMeta(self, name, value, units)
            res = dlg.ShowModal()
            name = dlg.get_name()
            value = dlg.get_value()
            units = dlg.get_units()
            cancel = res != wx.ID_OK
            valid_entry = (name != '' and value != '')
            if not valid_entry and not cancel:
                error(self, "The name and value fields are mandatory")
            dlg.Destroy()

        if not cancel:
            file_info = self.get_selected_files()[0]
            irods_path = file_info[0] + '/' + file_info[1]
            self.mdl.add_file_metadata(irods_path, name, value, units)
            self.populate_metadata_file(irods_path)

    def OnPop_FileMetaDel(self, evt):
        """Delete metadata to the selected file"""
        item = self.cur_sel
        name = self.lc_meta_file.GetItemText(item).encode("ascii")
        value = self.lc_meta_file.GetItem(item, 1).GetText().encode("ascii")
        units = self.lc_meta_file.GetItem(item, 2).GetText().encode("ascii")
        file_info = self.get_selected_files()[0]
        irods_path = file_info[0] + '/' + file_info[1]
        self.mdl.rm_file_metadata(irods_path, name, value, units)
        self.populate_metadata_file(irods_path)

    def OnPop_FileRename(self, evt):
        """Rename to the selected file"""
        sel_item = self.files_pydata[self.cur_sel]
        dlg = wx.TextEntryDialog(self, 'Enter the new name for the file : ',
                                 'Change Name', sel_item[1])
        if dlg.ShowModal() == wx.ID_OK:
            self.mdl.rename_file(sel_item, dlg.GetValue().encode("ascii"))
            self.refresh_data_list()
        dlg.Destroy()

    def OnPop_FileReplicate(self, evt):
        """Replicate the selected file"""
        sel_item = self.files_pydata[self.cur_sel]
        src_resc = sel_item[2]
        rescs = self.mdl.get_list_resources()
        
        if src_resc in rescs:
            rescs.remove(src_resc)
        
        dlg = wx.SingleChoiceDialog(
                self, 'Select Destination Resource', 'Replicate File',
                rescs, wx.CHOICEDLG_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.mdl.replicate_file(sel_item,
                                    dlg.GetStringSelection().encode("ascii"))
            self.refresh_data_list()
            
        dlg.Destroy()
        
        
    def OnRC_Coll(self, evt):
        """Right Click on a collection in the collection tree => Display a 
        popup menu"""
        id_new = wx.NewId()
        id_delete = wx.NewId()
        id_rename = wx.NewId()
        id_download = wx.NewId()
        id_copy_collection_clipboard = wx.NewId()
        
        self.col_item = evt.GetItem()
        
        self.Bind(wx.EVT_MENU, self.OnPop_CollNewCollection, id=id_new)
        self.Bind(wx.EVT_MENU, self.OnPop_CollDelete, id=id_delete)
        self.Bind(wx.EVT_MENU, self.OnPop_CollRename, id=id_rename)
        self.Bind(wx.EVT_MENU, self.OnPop_CollDownload, id=id_download)
        self.Bind(wx.EVT_MENU, self.OnPop_CollCopyPath, 
                  id=id_copy_collection_clipboard)
        
        menu = wx.Menu()
        menu.Append(id_new, "Make new Collection")
        menu.Append(id_rename, "Rename")
        menu.Append(id_delete, "Delete")
        menu.Append(id_download, "Download")
        menu.AppendSeparator()
        menu.Append(id_copy_collection_clipboard, 
                    "Copy iRODS path to clipboard")
        
        self.PopupMenu(menu)
        
        menu.Destroy()
        
     
    def OnRC_CollMeta(self, evt):
        """Right Click on a collection metadata => Display a popup menu"""  
        id_add = wx.NewId()
        id_delete = wx.NewId()
        
        self.cur_sel = evt.m_itemIndex
        
        self.Bind(wx.EVT_MENU, self.OnPop_CollMetaAdd, id=id_add)
        self.Bind(wx.EVT_MENU, self.OnPop_CollMetaDel, id=id_delete)
        
        menu = wx.Menu()
        menu.Append(id_add, "Add metadata")
        
        # If we click on the list but not on an element
        if self.lc_meta_collection.GetSelectedItemCount() != 0:
            menu.Append(id_delete, "Delete metadata")
        
        self.PopupMenu(menu)
        menu.Destroy()
        
        
    def OnRC_File(self, evt):
        """Right click on a file in the list data => Display a popup menu""" 
        if self.get_selected_files():
            
            id_delete = wx.NewId()
            id_rename = wx.NewId()
            id_replicate = wx.NewId()
            id_download = wx.NewId()
            id_copy_path_clipboard = wx.NewId()
            id_editor = wx.NewId()
            
            self.cur_sel = evt.m_itemIndex
            
            self.Bind(wx.EVT_MENU, self.OnPop_FileDelete, id=id_delete)
            self.Bind(wx.EVT_MENU, self.OnPop_FileRename, id=id_rename)
            self.Bind(wx.EVT_MENU, self.OnPop_FileReplicate, id=id_replicate)
            self.Bind(wx.EVT_MENU, self.OnPop_FileDownload, id=id_download)
            self.Bind(wx.EVT_MENU, self.OnPop_FileCopyPath, 
                      id=id_copy_path_clipboard)
            self.Bind(wx.EVT_MENU, self.OnPop_FileEditor, id=id_editor)
            
            menu = wx.Menu()
            menu.Append(id_delete, "Delete")
            menu.Append(id_rename, "Rename")
            menu.Append(id_replicate, "Replicate")
            menu.Append(id_download, "Download")
            menu.AppendSeparator()
            menu.Append(id_copy_path_clipboard, "Copy iRODS path to clipboard")
            
            path, filename, resc = self.files_pydata[self.cur_sel]
            
            menu.AppendSeparator()
            
            if filename.endswith(".py"):
                menu.Append(id_editor, "Edit the script")
            else:
                menu.Append(id_editor, "View the file")
                            
            self.PopupMenu(menu)
            
            menu.Destroy()
            
     
    def OnRC_FileMeta(self, evt):
        """Right click on a file metadata => Display a popup menu"""
        if self.get_selected_files():
            id_add = wx.NewId()
            id_delete = wx.NewId()
            
            self.cur_sel = evt.m_itemIndex
            
            self.Bind(wx.EVT_MENU, self.OnPop_FileMetaAdd, id=id_add)
            self.Bind(wx.EVT_MENU, self.OnPop_FileMetaDel, id=id_delete)
            
            menu = wx.Menu()
            menu.Append(id_add, "Add metadata")
        
            # If we click on the list but not on an element
            if self.lc_meta_file.GetSelectedItemCount() != 0:
                menu.Append(id_delete, "Delete metadata")                
                
            self.PopupMenu(menu)
            menu.Destroy()
            
            
    def OnSel_Coll(self, evt):
        """Modify the selection of the collection tree control"""
        item = evt.GetItem()
        if item:       
            irods_path = self.tc_collection.GetPyData(item)
            tree = self.tc_collection
            # Delete the previous children (in case of update)
            tree.DeleteChildren(item)
            
            subcollections = self.mdl.get_collection_subCollections(irods_path)
            
            for child_name in subcollections:   
                child = tree.AppendItem(item, child_name)
                if irods_path == '/':
                    tree.SetPyData(child, irods_path + child_name)
                else:
                    tree.SetPyData(child, irods_path + '/' + child_name)
                tree.SetItemImage(child, tree.fldridx, wx.TreeItemIcon_Normal)
                tree.SetItemImage(child, tree.fldropenidx, 
                                  wx.TreeItemIcon_Expanded)
            
            tree.Expand(item)
            
            self.populate_data_list(irods_path)
            self.populate_metadata_collection(irods_path)
            
            
    def OnSel_File(self, evt):
        """Select a file in the list data"""
        self.tb_io.EnableTool(ID_Toolbar_DownloadF, True)
        self.cur_sel = evt.m_itemIndex
        tmp = self.files_pydata[self.cur_sel]
        # Update metadata list for this data object
        self.populate_metadata_file(tmp[0] + '/' + tmp[1])
        
        
    def OnTool_DownCollection(self, evt):
        """Toolbar : Download the selected collection"""
        curr_name = self.get_selected_collection()
        self.download_collection_dlg(curr_name)
        
        
    def OnTool_DownFile(self, evt):
        """Toolbar : Download the selected file(s)"""
        sel_files = self.get_selected_files()
        self.download_files_dlg(sel_files)
        
        
    def OnTool_Refresh(self, evt):
        """Toolbar : Refresh the collection tree and the file list"""
        # This will trigger the data list refresh
        self.refresh_collection_tree()
        
        
    def OnTool_UpCollection(self, evt):
        """Toolbar : Upload a collection in the selected collection"""
        curr_name = self.get_selected_collection()
        self.upload_collection(curr_name)
        tree = self.tc_collection
        
        # Update the tree control
        parent = tree.GetSelection()
        irods_path = tree.GetPyData(parent)
        
        col_name = self.get_selected_collection()
        children_irods = self.mdl.get_collection_subCollections(col_name)        
        children_tree = self.get_children_name(parent)
        
        for child in children_irods:
            if not child in children_tree:
                item = tree.AppendItem(parent, child)
                tree.SetPyData(item, irods_path + '/' + child)
                tree.SetItemImage(item, tree.fldridx, wx.TreeItemIcon_Normal)
                tree.SetItemImage(item, tree.fldropenidx, 
                                  wx.TreeItemIcon_Expanded)

    def OnTool_UpFile(self, evt):
        """Toolbar : Upload file(s) in the selected collection"""
        wildcard = "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Choose file(s)",
                            defaultDir=os.getcwd(),
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            paths = dlg.GetPaths()
        dlg.Destroy()
        paths = [p.encode("ascii") for p in paths]
        if res == wx.ID_OK:
            self.upload_paths(paths,
                              self.get_selected_collection())

    def OnTool_UserInfo(self, evt):
        """Toolbar : Display user information"""
        userinfo = self.mdl.get_user_infos(self.cfg.irods_username)
        f = UserInfoFrame(self.cfg,
                          userinfo['user_name'],
                          userinfo['user_type_name'],
                          userinfo['user_id'],
                          userinfo['zone_name'],
                          userinfo['r_comment'],
                          userinfo['user_info'],
                          userinfo['create_ts'],
                          userinfo['modify_ts'])
        f.Show()

    def align_shapes(self):
        """Align the shapes of the displayed canvas"""
        self.ogl_irules.align_shapes()
        
        
    def create_menu_admin(self):
        """Create the main menu for the collection view"""
        menu_infos = (("&File",
                        ("&Close Application", "Close the application", 
                         self.OnMenu_Close, 0)),

                      ("&View",
                        ("&Local Filesystem", "View local filesystem tree", 
                         self.OnMenu_LocalFilesystem, 1)),

                      ("&Help",
                        ("&About...", "", 
                         self.OnMenu_About, 0))
                      )

        return create_menubar(self, menu_infos) 

    def create_new_microservice(self):
        """Add a new microservice in the current canvas"""
        self.ogl_irules.create_new_microservice()

    def create_statusbar(self):
        """Create a status bar with 3 fields"""
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-3, -2])
        self.statusbar.SetStatusText("", 0)

    def create_toolbar_infos(self):
        """Create the toolbar for information on user/..."""
        tb = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        
        tb.SetToolBitmapSize(wx.Size(24, 24))
        tb.AddLabelTool(ID_Toolbar_UserInfo, "User information", 
                        self.cfg.get_bmp('user.png'), 
                        shortHelp = "Get User Information")
        tb.Realize()
        
        return tb
    
    
    def delete_selected_rule(self):
        """Delete the selected rule"""
        self.ogl_irules.rm_selected_rule()   
        self.enable_delete_toolRule(False)
                
    
    def create_toolbar_io(self):
        """Create the i/o toolbar, for upload/download"""
        tb = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        
        rescs = self.mdl.get_list_resources()
        self.cb_resc = wx.ComboBox(tb, -1, self.mdl.get_default_resource(), 
                                   size=(160, -1), choices=rescs,
                                   style=wx.CB_DROPDOWN | 
                                         wx.CB_READONLY | 
                                         wx.CB_SORT)
                
        tb.SetToolBitmapSize(wx.Size(24, 24))
        tb.AddLabelTool(ID_Toolbar_DownloadF, "Download files", 
                        self.cfg.get_bmp('down_file.png'), 
                        shortHelp = "Download Files")
        tb.AddLabelTool(ID_Toolbar_UploadF, "Upload files", 
                        self.cfg.get_bmp('up_file.png'), 
                        shortHelp = "Upload Files")
                        
        tb.AddSeparator()
        
        tb.AddLabelTool(ID_Toolbar_DownloadC, "Download Collection", 
                        self.cfg.get_bmp('down_collection.png'), 
                        shortHelp = "Download Collection")
        tb.AddLabelTool(ID_Toolbar_UploadC, "Upload Collection", 
                        self.cfg.get_bmp('up_collection.png'), 
                        shortHelp = "Upload Collection")
        
        tb.AddSeparator()
        
        tb.AddLabelTool(ID_Toolbar_Refresh, "Refresh View", 
                        self.cfg.get_bmp('refresh.png'), 
                        shortHelp = "Refresh View")
        
        tb.AddSeparator()
        
        tb.AddControl(self.cb_resc)
        tb.Realize()
        tb.EnableTool(ID_Toolbar_DownloadF, False)
        
        return tb
        
        
    def download_collection(self, collection_path, local_dir): 
        """Download an irods collection to a local directory. If some files are 
        present ask for each one if we want to replace them."""  
        to_download, to_create = self.mdl.download_collection(collection_path, 
                                                              local_dir)
                
        nb_coll = len(to_create)
        
        dlg = wx.ProgressDialog("Transfer collections",
                                "Creating local directory",
                                maximum = nb_coll,
                                parent=self,
                                style = wx.PD_CAN_ABORT
                                 | wx.PD_APP_MODAL
                                 | wx.PD_ELAPSED_TIME
                                 #| wx.PD_ESTIMATED_TIME
                                 | wx.PD_REMAINING_TIME)
        keepGoing = True

        # Create Collections
        count = 0
        while keepGoing and count < nb_coll:
            self.mdl.mkdirR(local_dir, to_create[count])
            keepGoing, _ = dlg.Update(count)
            count += 1
        dlg.Destroy()
        self.download_files(to_download)

    def download_collection_dlg(self, collection_path):
        """Download a collection from irods and let the user choose the local
        directory."""
        dlg = wx.DirDialog(self,
                           "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.download_collection(collection_path,
                                     dlg.GetPath().encode("ascii"))
        dlg.Destroy()

    def download_files(self, file_list, overwrite=False):
        """Download files from irods to the local filesystem. The file_list
        contains the irods path and the local directory. If some files are
        present ask for each one if we want to replace them"""
        already_there = []
        nb_files = len(file_list)
        dlg = wx.ProgressDialog("Transfer collections",
                                "Downloading Files",
                                maximum=nb_files,
                                parent=self,
                                style=wx.PD_CAN_ABORT
                                 | wx.PD_APP_MODAL
                                 | wx.PD_ELAPSED_TIME
                                 #| wx.PD_ESTIMATED_TIME
                                 | wx.PD_REMAINING_TIME)
        keepGoing = True

        # Download Files
        count = 0
        while keepGoing and count < nb_files:
            irods_path, resc, local_file = file_list[count]
            exist = self.mdl.download_file(irods_path, local_file, resc,
                                           overwrite)
            if exist:
                already_there.append(file_list[count])
            (keepGoing, _) = dlg.Update(count)
            count += 1

        dlg.Destroy()
        if already_there:
            to_redownload = []
            res = 0
            count = 0
            maxC = len(already_there)
            while count < maxC and res not in [wx.ID_NOTOALL, wx.ID_YESTOALL]:
                irods_path, resc, local_path = already_there[count]
                if res != wx.ID_YESTOALL:
                    msg = local_path + ' already exists\n'
                    msg += "Do you want to overwrite it ?"
                    title = "Upload Error"
                    dlg = ConfirmReplaceDialog(self, title, msg)
                    res = dlg.ShowModal()
                if res == wx.ID_YES:
                    to_redownload.append(already_there[count])
                elif res == wx.ID_YESTOALL:
                    to_redownload += already_there[count:]
                count += 1
            self.download_files(to_redownload, True)

    def download_files_dlg(self, file_list):
        """Download files from irods to a local directory. If some files are
        present ask for each one if we want to replace them. Ask for the
        local dir"""
        dlg = wx.DirDialog(self,
                           "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            file_list = [((col + '/' + fi).encode("ascii"),
                          res,
                          (path + os.sep + fi).encode("ascii"))
                         for (col, fi, res) in file_list]
            self.download_files(file_list)

        dlg.Destroy()

    def expand_file_list(self, paths, coll_path, coll_to_add):
        """Take the list of local files and create a list of tuples (local
        path, collection target in iRODS). The list of local paths may contain
        directories so these directories are scanned recursively.
        The returned list contains all the files we need to upload.
        coll_to_add contains the new collections to create in iRODS"""
        coll_to_add = []
        filenames = [ (path, coll_path) for path in paths if os.path.isfile(path)]
        dirnames = [ path for path in paths if os.path.isdir(path)]
        
        root_path = os.path.dirname(paths[0])

        while dirnames:
            dir_path = dirnames.pop(0)

            new_coll_path = dir_path.replace(root_path, coll_path)
            coll_to_add.append(new_coll_path)

            new_paths = [ dir_path + '/' + el_path for el_path in os.listdir(dir_path)]
            filenames += [ (path, new_coll_path) for path in new_paths if os.path.isfile(path)]
            dirnames += [ path for path in new_paths if os.path.isdir(path)]
            
        return filenames, coll_to_add
        
        
    def get_children_name(self, item):
        """Return a list of children names for a specific element of the tree 
        control"""
        res = []
        (child, cookie) = self.tc_collection.GetFirstChild(item)
        
        while child.IsOk():
            res.append(self.tc_collection.GetItemText(child))
            (child, cookie) = self.tc_collection.GetNextChild(item, cookie)
        
        return res
    
    
    def get_dropped_collection(self, x, y):
        """Get the local dir where we drop an irods path (the selection is not
        always the wanted path)"""
        return self.tc_collection.GetItemPathPos(x, y)
    
    
    def get_dropped_local_dir(self, x, y):
        """Get the local dir where we drop an irods path (the selection is not
        always the wanted path)"""
        return self.tc_local.GetItemPathPos(x, y)
       
        
    def get_mode(self):
        """Get the current edition mode for the designer (wf or recovery)"""
        if self.cur_persp == 'iruleWf':
            return 'wf'
        else:
            return 'rec'
    
    
    def get_resource(self):
        """Get the selected resource from the combo box of the i/o toolbar"""
        return self.cb_resc.GetValue().encode("ascii")
    
    
    def get_selected_collection(self):
        """Get the information associated with the selected element in the data 
        list control"""
        item = self.tc_collection.GetSelection()
        return self.tc_collection.GetPyData(item)
    
    
    def get_selected_files(self):
        """Get a list of information associated with the selected elements in 
        the data list control"""
        l = [] 
        index = self.lc_data.GetFirstSelected()
        
        while index != -1:
            l.append(self.files_pydata[self.lc_data.GetItemData(index)])
            index = self.lc_data.GetNextSelected(index)
            
        return l
        
        
    def get_session_variables(self):
        """Return a list of session variable for the selected rule (starts 
        with $)"""
        return self.mdl.get_session_variables()
    
    
    def get_state_variables(self):
        """Return a list of state variable for the selected rule (starts 
        with *)"""
        return self.mdl.get_state_variables()
        
        
    def move_collection(self, coll_path_src, coll_path_dst):
        """Move a collection in the specified collection"""
        status = self.mdl.move_collection(coll_path_src, coll_path_dst)
        if status == 0:
            self.populate_collection_tree(coll_path_dst)
        else:
            irodsError(self.mdl, status)


    def move_files(self, paths, coll_path):  
        """Move a list of files in the specified collection"""
        already_there = self.mdl.move_files(paths, coll_path)
            
        if already_there:
            for local_file in already_there:
                coll_name, file_name, src_resc = local_file
                irods_path_dst = coll_path + '/' + file_name
                
                msg = irods_path_dst + ' already exists\n'
                msg += "Do you want to overwrite it ?"
                dlg = wx.MessageDialog(self, msg, 'Error', 
                                       wx.ICON_INFORMATION | wx.YES_NO)
                res = dlg.ShowModal()
                dlg.Destroy()
                
                if res == wx.ID_YES:
                    self.mdl.move_files([local_file], coll_path, True)
                        
        self.populate_data_list(self.get_selected_collection())

    def populate_collection_tree(self, irods_path): 
        """Add elements in the tree control for collection according to the 
        path given in parameter. Add all the elements from the root to the 
        path, the brother of the path and the child collection of the path. 
        Each element have a PyData associated which is the full logical path 
        in irods"""
        tree = self.tc_collection
        
        tree.DeleteAllItems()  
        list_coll = irods_path.split('/')
        list_coll[0] = '/'
        
        path = '/'
        
        root = tree.AddRoot('/')
        tree.SetPyData(root, '/')
        tree.SetItemImage(root, tree.fldridx, wx.TreeItemIcon_Normal)
        tree.SetItemImage(root, tree.fldropenidx, wx.TreeItemIcon_Expanded)
        
        parent = root
        
        for coll in list_coll[1:]:
            # child1 is the child that belongs to the irods_path we want 
            # to display
            child1 = tree.AppendItem(parent, coll)
            
            if path == '/':
                tree.SetPyData(child1, path + coll)
            else:
                tree.SetPyData(child1, path + '/' + coll)
                
            tree.SetItemImage(child1, tree.fldridx, wx.TreeItemIcon_Normal)
            tree.SetItemImage(child1, tree.fldropenidx, 
                              wx.TreeItemIcon_Expanded)
            
            # Insert the brother of coll as well
            for child_name in self.mdl.get_collection_subCollections(path):
                if child_name != coll:
                    child2 = tree.AppendItem(parent, child_name)
                    tree.SetPyData(child2, path + '/' + child_name)
                    tree.SetItemImage(child2, tree.fldridx, 
                                      wx.TreeItemIcon_Normal)
                    tree.SetItemImage(child2, tree.fldropenidx, 
                                      wx.TreeItemIcon_Expanded)
            
            parent = child1
            if path == '/':
                path = path + coll
            else:
                path = path + '/' + coll
        
        # Add sub collection for the home directory   
        for child_name in self.mdl.get_collection_subCollections(irods_path):
            child2 = tree.AppendItem(parent, child_name)
            if irods_path == '/':
                tree.SetPyData(child2, irods_path + child_name)
            else:
                tree.SetPyData(child2, irods_path + '/'  + child_name)
                
            tree.SetItemImage(child2, tree.fldridx, wx.TreeItemIcon_Normal)
            tree.SetItemImage(child2, tree.fldropenidx, 
                              wx.TreeItemIcon_Expanded)
            
        tree.SelectItem(parent, True)
        self.tc_collection.Expand(parent)
                    
        self.populate_metadata_collection(irods_path)
        
        
    def populate_data_list(self, irods_path):
        """Add information for the files which are contained in the collection
         passed in parameter"""
        self.tb_io.EnableTool(ID_Toolbar_DownloadF, False)
        
        l_data = self.lc_data
        self.files_pydata = {}
        cpt_idx = 0
        
        l_data.ClearAll()
        
        l_data.InsertColumn(0, "Name")
        l_data.InsertColumn(1, "Type", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(2, "Replica", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(3, "Size", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(4, "Owner", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(5, "Owner Zone", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(6, "Resource", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(7, "Modified Time", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(8, "Creation Time", wx.LIST_FORMAT_RIGHT)   
        
        l_objects = self.mdl.get_collection_objects(irods_path)
        for (file_name, resc_name) in l_objects:
            full_path = irods_path + '/' + file_name
            d_info = self.mdl.get_file_info(full_path, resc_name)
            
            index = l_data.InsertStringItem(sys.maxint, file_name)
            l_data.SetStringItem(index, 1, d_info['data_type_name'])
            l_data.SetStringItem(index, 2, d_info['data_repl_num'])
            l_data.SetStringItem(index, 3, d_info['data_size'])
            l_data.SetStringItem(index, 4, d_info['data_owner_name'])
            l_data.SetStringItem(index, 5, d_info['data_owner_zone'])
            l_data.SetStringItem(index, 6, d_info['resc_name'])
            l_data.SetStringItem(index, 7, d_info['modify_ts'])
            l_data.SetStringItem(index, 8, d_info['create_ts'])
            self.files_pydata[cpt_idx] = (irods_path, file_name, resc_name)
            l_data.SetItemData(index, cpt_idx)
            cpt_idx += 1
            
        if  self.mdl.get_collection_nb_objects(irods_path) > 0:
            l_data.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            l_data.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            l_data.SetColumnWidth(2, 50)
            l_data.SetColumnWidth(3, wx.LIST_AUTOSIZE)
            l_data.SetColumnWidth(4, wx.LIST_AUTOSIZE)
            l_data.SetColumnWidth(5, wx.LIST_AUTOSIZE)
            l_data.SetColumnWidth(6, wx.LIST_AUTOSIZE)
            l_data.SetColumnWidth(7, wx.LIST_AUTOSIZE)
            l_data.SetColumnWidth(8, wx.LIST_AUTOSIZE)
        
        self.populate_metadata(self.lc_meta_file, [])
        
        
    def populate_irule_list(self):
        """Update the irule list"""
        self.p_irules.populate_irule_list()
        
        
    def populate_metadata(self, l_data, metas): 
        """Add metadatas information to a list control"""   
        l_data.ClearAll()
        
        l_data.InsertColumn(0, "Name")
        l_data.InsertColumn(1, "Value", wx.LIST_FORMAT_RIGHT)
        l_data.InsertColumn(2, "Units", wx.LIST_FORMAT_RIGHT)
        
        for (name, value, units) in metas:
            index = l_data.InsertStringItem(sys.maxint, name)
            l_data.SetStringItem(index, 1, value)
            l_data.SetStringItem(index, 2, units)
        
        l_data.SetColumnWidth(0, 100)
        l_data.SetColumnWidth(1, 100)
        l_data.SetColumnWidth(2, 150)
        
        
    def populate_metadata_collection(self, irods_path):
        """Add metadatas information for a collection"""
        metas = self.mdl.get_collection_metadatas(irods_path)
        self.populate_metadata(self.lc_meta_collection, metas)
        
        
    def populate_metadata_file(self, irods_path):
        """Add metadatas information for a file"""
        metas = self.mdl.get_file_metadatas(irods_path)
        self.populate_metadata(self.lc_meta_file, metas)
        
        
    def populate_ms(self, shape):
        """Add microservice information in the ms panel"""
        self.p_ms.populate(shape)
        
        
    def refresh_canvas(self):
        """Refresh the current canvas"""
        self.ogl_irules.refresh()
        
        
    def refresh_collection_tree(self):
        """Refresh the collection tree"""
        cur_coll = self.get_selected_collection()
        self.populate_collection_tree(cur_coll)
        
        
    def refresh_data_list(self):
        """Refresh the data list information when the selected collection in 
        the tree control change"""
        cur_coll = self.get_selected_collection()
        self.populate_data_list(cur_coll)

    def rm_selected_rule(self):
        """Delete the selected rule"""
        self.ogl_irules.rm_selected_rule()
        
    
    def rm_selected_shape(self):
        """Delete the selected shape"""
        self.ogl_irules.rm_selected_shape()
        
        
        
        
    def upload_collection(self, collection_path):
        """Upload a local collection in collection_path. If some files are 
        present ask for each one if we want to replace them"""
        dlg = wx.DirDialog(self, 
                           "Choose a directory:", 
                           style=wx.DD_DEFAULT_STYLE )
        
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            path =  dlg.GetPath().encode("ascii")
            
        dlg.Destroy()
        
        if res == wx.ID_OK:  
            self.upload_paths([path], collection_path)
            
        
    def upload_files(self, file_list, overwrite=False):
        """Upload a list of local files in the current collection, collections 
        are already created. paths is a list of tuples (org file, dst 
        collection)"""
        already_there = []
        nb_files = len(file_list)
        dlg = wx.ProgressDialog("Transfer collections",
                                "Uploading Files",
                                maximum=nb_files,
                                parent=self,
                                style=wx.PD_CAN_ABORT
                                 | wx.PD_APP_MODAL
                                 | wx.PD_ELAPSED_TIME
                                 #| wx.PD_ESTIMATED_TIME
                                 | wx.PD_REMAINING_TIME
                                 )
        keepGoing = True

        # Upload Files
        count = 0
        while keepGoing and count < nb_files:
            file_path, coll_path = file_list[count]
            irods_path = coll_path + '/' + os.path.basename(file_path)
            exist = self.mdl.upload_file(file_path, irods_path,
                                         self.get_resource(),
                                         overwrite)
            if exist:
                already_there.append(file_list[count])
            (keepGoing, _) = dlg.Update(count)
            count += 1
             
        dlg.Destroy()
              
        if already_there:
            to_reupload = []
            
            res = 0
            count = 0
            maxC = len(already_there)
            while count < maxC and res not in [wx.ID_NOTOALL, wx.ID_YESTOALL]:
                
                file_path, coll_path = already_there[count]
                
                if res != wx.ID_YESTOALL:
                    f_path = coll_path + '/' + os.path.basename(file_path)
                    msg = f_path + ' already exists\n'
                    msg += "Do you want to overwrite it ?"
                    title = "Upload Error"
                    dlg = ConfirmReplaceDialog(self, title, msg)
                    res = dlg.ShowModal()
                    
                if res == wx.ID_YES:
                    to_reupload.append(already_there[count])
                elif res == wx.ID_YESTOALL:
                    to_reupload += already_there[count:]
                    
                count += 1
                
            self.upload_files(to_reupload, True)
            
        
    def update_rule_box(self):
        """Update the shape for the rule"""
        self.ogl_irules.update_rule_box()
        

    def upload_paths(self, paths, root_coll_path, overwrite=False):
        """Upload a list of local files (or directory) in the current
        collection"""
        new_collections = []
        file_list, new_collections = self.expand_file_list(paths,
                                                           root_coll_path,
                                                           new_collections)
        
        nb_coll = len(new_collections)
        
        dlg = wx.ProgressDialog("Transfer collections",
                                "Creating new collections",
                                maximum = nb_coll,
                                parent=self,
                                style = wx.PD_CAN_ABORT
                                 | wx.PD_APP_MODAL
                                 | wx.PD_ELAPSED_TIME
                                 #| wx.PD_ESTIMATED_TIME
                                 | wx.PD_REMAINING_TIME
                                 )
        keepGoing = True
        # Create Collections
        count = 0
        while keepGoing and count < nb_coll:
            self.mdl.new_collection(new_collections[count])
            (keepGoing, _) = dlg.Update(count)
            count += 1

        dlg.Destroy()
        self.upload_files(file_list, overwrite)
        self.populate_data_list(root_coll_path)
