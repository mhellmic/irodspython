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
# Creation     : November, 2010

"""Text editors"""


import wx
import wx.stc as stc
import keyword

from interface.dialogs import ConfirmCloseDialog


if wx.Platform == '__WXMSW__':
    faces = {'times': 'Times New Roman',
             'mono' : 'Courier New',
             'helv' : 'Arial',
             'other': 'Comic Sans MS',
             'size' : 10,
             'size2': 8,
             }
elif wx.Platform == '__WXMAC__':
    faces = {'times': 'Times New Roman',
             'mono' : 'Monaco',
             'helv' : 'Arial',
             'other': 'Comic Sans MS',
             'size' : 12,
             'size2': 10,
             }
else:
    faces = {'times': 'Times',
             'mono' : 'Courier',
             #'helv' : 'Helvetica',
             'helv' : 'Monospace',
             'other': 'new century schoolbook',
             'size' : 10,
             'size2': 10,
             }


class DefaultSTC(stc.StyledTextCtrl):
    """The default text editor"""

    def __init__(self, parent, frame, ID,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)
        self.parent = frame

        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        
        # Determine how to indicate bad indentation (1 = inconsistent)
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0, 0)

        self.SetViewWhiteSpace(False)   
        
        # Setup a margin to hold fold markers
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        self.StyleClearAll()  # Reset all to be like the default
        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     
                          "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  
                          "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, 
                          "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  
                          "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    
                          "fore:#000000,back:#FF0000,bold")        
                
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)        
        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(stc.EVT_STC_MODIFIED, self.OnModified)
        
        self.SetCaretForeground("BLUE")
        

    def OnDestroy(self, evt):
        """Destroy the editor"""
        wx.TheClipboard.Flush()
        evt.Skip()


    def OnKeyPressed(self, event):
        """Keydown event"""
        key = event.GetKeyCode()
        
        if 27 < key < 256:
            #self.parent.modified = True
            keyname = chr(key)
        else:
            keyname = None
           
        if keyname == 'S' and event.ControlDown(): # CTRL+S
            self.parent.save()        
        else:
            event.Skip()
        
        
    def OnModified(self, evt):
        """Modify the content => Update the title"""
        self.parent.load_title()


    def OnUpdateUI(self, evt): 
        """Refresh the editor"""        
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            
        #evt.Skip()
        
        
    def highlight(self, pos, length):
        """Highlight the text from the pos for length characters"""
        pass


class EditorFrame(wx.Frame):
    """The frame which contains the STC editor"""
    # The file should exist 
    def __init__(self, parent, model, path, filename, resc=None, 
                 assoc_shape=None):
        title = "%s/%s (%s)" % (path, filename, resc)
        wx.Frame.__init__(self, parent, -1, title, size=(800, 600), 
                          style=wx.DEFAULT_FRAME_STYLE)
        self.panel = wx.Panel(self, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.mdl = model
        self.assoc_shape = assoc_shape

        # Instantiate the right STC editor
        if filename.endswith(".py"):
            self.ed = PythonSTC(self.panel, self, -1)
        elif filename.endswith(".irb") or filename.endswith(".ir"):
            self.ed = IRBSTC(self.panel, self, -1)
        else:
            self.ed = DefaultSTC(self.panel, self, -1)
        self.path = path
        self.filename = filename
        self.resc = resc

        self.cfg = parent.cfg

        tsize = (24, 24)

        save_bmp =  wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        undo_bmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, tsize)
        redo_bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, tsize)
        cut_bmp = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)

        id_save = wx.NewId()
        id_revert = wx.NewId()
        id_close = wx.NewId()

        tb = wx.ToolBar(self, style=wx.TB_HORIZONTAL
                                    | wx.NO_BORDER
                                    | wx.TB_FLAT)
        tb.SetToolBitmapSize(tsize)

        tb.AddLabelTool(wx.ID_SAVE, "Save", save_bmp, shortHelp="Save", 
                        longHelp="Save the current file")

        tb.AddSeparator()

        tb.AddLabelTool(wx.ID_UNDO, "Undo\tCTRL+Z", undo_bmp, shortHelp="Undo", 
                        longHelp="Undo the last action")

        tb.AddLabelTool(wx.ID_REDO, "Redo\tCTRL+Y", redo_bmp, shortHelp="Redo", 
                        longHelp="Redo the last undone action")

        tb.AddSeparator()

        tb.AddLabelTool(wx.ID_CUT, "Cut", cut_bmp, shortHelp="Cut", 
                        longHelp="Cut the selection")

        tb.AddLabelTool(wx.ID_COPY, "Copy", copy_bmp, shortHelp="Copy", 
                        longHelp="Copy the selection")

        tb.AddLabelTool(wx.ID_PASTE, "Paste", paste_bmp, shortHelp="Paste", 
                        longHelp="Paste the clipboard")

        tb.Realize()
        self.SetToolBar(tb)

        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(id_save, "&Save", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(id_revert, "&Revert", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(id_close, "&Close", "", wx.ITEM_NORMAL)
        self.frame_menubar.Append(wxglade_tmp_menu, "&File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_UNDO, "&Undo", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_REDO, "&Redo", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_CUT, "Cu&t", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_COPY, "&Copy", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_PASTE, "&Paste", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_DELETE, "&Delete", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_SELECTALL, "Select &All", "", wx.ITEM_NORMAL)
        self.frame_menubar.Append(wxglade_tmp_menu, "&Edit")
        self.SetMenuBar(self.frame_menubar)

        # Statusbar
        self.frame_statusbar = self.CreateStatusBar(1, 0)
        self.frame_statusbar.SetStatusWidths([-1])
        frame_statusbar_fields = ["Test"]
        for i in range(len(frame_statusbar_fields)):
            self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)

        # Event binding

        self.Bind(wx.EVT_TOOL, self.OnUndo, id=wx.ID_UNDO)
        self.Bind(wx.EVT_TOOL, self.OnRedo, id=wx.ID_REDO)
        self.Bind(wx.EVT_TOOL, self.OnCut, id=wx.ID_CUT)
        self.Bind(wx.EVT_TOOL, self.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_TOOL, self.OnPaste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_TOOL, self.OnSelectAll, id=wx.ID_SELECTALL)
        self.Bind(wx.EVT_TOOL, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.OnRevert, id=id_revert)
        self.Bind(wx.EVT_TOOL, self.OnClose, id=id_close)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.do_layout()
        self.load_title()
        self.load_content()

    def OnClose(self, evt):
        """Close the frame"""
        if self.ed.GetModify():
            dlg = ConfirmCloseDialog(self) 
            res = dlg.ShowModal()
            dlg.Destroy()
            if res == wx.ID_CANCEL:
                return
            if res == wx.ID_SAVE:
                self.save()
        self.Destroy()

    def OnCopy(self, evt):
        """Toolbar event: copy"""
        self.ed.Copy()

    def OnCut(self, evt):
        """Toolbar event: cut"""
        self.ed.Cut()

    def OnPaste(self, evt):
        """Toolbar event: paste"""
        self.ed.Paste()

    def OnRedo(self, evt):
        """Toolbar event: redo"""
        self.ed.Redo()

    def OnRevert(self, evt):
        """Toolbar event: revert"""
        self.load_content()

    def OnSave(self, evt):
        """Toolbar event: save"""
        self.save()

    def OnSelectAll(self, evt):
        """Toolbar event: select all"""
        self.ed.SelectAll()

    def OnUndo(self, evt):
        """Toolbar event: undo"""
        self.ed.Undo() 
        self.modified = True

    def append_content(self, content):
        """Append text to the editor"""
        self.ed.AppendText(content)

    def do_layout(self):
        """Layout the frame"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add(self.ed, 1, wx.EXPAND)
        self.panel.SetSizer(s)
        self.panel.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()

    def highlight(self, pos, length):
        """Highlight the text from the pos for length characters"""
        self.ed.highlight(pos, length)

    def load_content(self): 
        """Load the content of an irods file"""
        if self.resc:
            txt = self.mdl.read_file(self.path + "/" + self.filename, self.resc)
        else:
            txt = self.mdl.read_file(self.path + "/" + self.filename)
        self.ed.SetText(txt)
        self.ed.EmptyUndoBuffer()
        self.ed.Colourise(0, -1)
        # line numbers in the margin
        self.ed.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.ed.SetMarginWidth(1, 25)

    def load_title(self):
        """Modify the title of the frame"""
        if self.resc:
            title = "%s/%s (%s)" % (self.path, self.filename, self.resc)
        else:
            title = "%s/%s" % (self.path, self.filename)
        if self.ed.GetModify():
            title = "*" + title
        self.SetTitle(title)

    def save(self):
        """Save the actual content to an iRODS file"""
        if self.resc:
            self.mdl.save_file(self.path + "/" + self.filename,
                               self.ed.GetText().encode("ascii"),
                               self.resc)
        else:
            self.mdl.save_file(self.path + "/" + self.filename,
                               self.ed.GetText().encode("ascii"))
        self.ed.SetSavePoint()
        self.load_title()
        if self.assoc_shape:
            self.assoc_shape.validate()

    def search(self, s):
        """Search a string in the editor"""
        return self.ed.FindText(0, self.ed.GetTextLength(), s)

    def search_method(self, method_name):
        """Search a Python method in a text file"""
        txt = self.ed.GetText()
        return self.cfg.get_python_parser().find_method_name(method_name, txt)

    def set_current_pos(self, method_idx):
        """Move the cursor to a specific position"""
        self.ed.GotoPos(method_idx)


class IRBSTC(DefaultSTC):
    """A STC editor for irb/ir files (iRODS rules)"""
    
    def __init__(self, parent, frame, ID,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        
        self.pos = -1
        self.length = -1
        DefaultSTC.__init__(self, parent, frame, ID, pos, size, style)
        
        self.SetLexer (wx.stc.STC_LEX_CONTAINER)    
        
        self.StyleClearAll()  # Reset all to be like the default    
        
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 
                          "fore:#000000,face:%(helv)s,size:%(size)d" % faces) 
        self.StyleSetSpec(IrbLexer.default_style, 
                          "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(IrbLexer.comment_style, 
                          "fore:#7F7F7F,size:%(size)d" % faces)
        self.StyleSetSpec(IrbLexer.rule_name_style, 
                          "fore:#FF0000,bold,size:%(size)d" % faces)
        self.StyleSetSpec(IrbLexer.ms_name_style, 
                          "fore:#00007F,italic,size:%(size)d" % faces)
        
        self.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyleNeeded)
                

    def OnKeyPressed(self, event):
        """Keydown event"""
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
                
        if 27 < key < 256 or key == 13:
            keyname = chr(key)
            #self.parent.modified = True
            #self.parent.load_title()
        else:
            keyname = None

        if key == 32 and event.ControlDown():
            kw = keyword.kwlist[:]

            kw.sort()  
            self.AutoCompSetIgnoreCase(False)  # so this needs to match

            for i in range(len(kw)):
                if kw[i] in keyword.kwlist:
                    kw[i] = kw[i]

            self.AutoCompShow(0, " ".join(kw))
        
        elif keyname == 'S' and event.ControlDown(): # CTRL+S
            self.parent.save()
        else:
            event.Skip()
            
        
    def OnStyleNeeded(self, evt):
        """Colorize"""
        text = self.GetText()
        parser = IrbParser()
        lexers = parser.parse(text)
        
#        # This leads to blinking :(
#        start = self.GetEndStyled()
#        end = evt.GetPosition()
#        self.StartStyling(0, 31) 
#        for pos in range(start, end): 
#            self.SetStyling(1, wx.stc.STC_STYLE_DEFAULT)
        
        
        # Colorize found lexers
        self.colorize_lexers(lexers)

        
    def colorize_lexers(self, lexers):
        """Apply colors to found lexers in the text"""
        for lexer in lexers:
            pos = lexer.position
            
            self.StartStyling(pos, 0xff)
            self.SetStyling(len(lexer.text), lexer.lex_style)           
            


class PythonSTC(DefaultSTC):
    """A STC editor for Python scripts"""
    
    def __init__(self, parent, frame, ID,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        DefaultSTC.__init__(self, parent, frame, ID, pos, size, style)

        self.ClearDocumentStyle()
        self.SetLexer(stc.STC_LEX_PYTHON)
        
        self.SetKeyWords(0, " ".join(keyword.kwlist))
        
        self.StyleClearAll()  # Reset all to be like the default    

        # Python styles
        # Default 
        self.StyleSetSpec(stc.STC_P_DEFAULT, 
                          "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, 
                          "fore:#800000,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, 
                          "fore:#00AA00,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, 
                          "fore:#00AA00,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, 
                          "fore:#0000FF,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, 
                          "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, 
                          "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, 
                          "fore:#000000,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, 
                          "fore:#000000,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, 
                          "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, 
                          "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, 
                          "fore:#7F7F7F,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, 
                          "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, 
                          "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        self.IndicatorSetStyle(2, wx.stc.STC_INDIC_MAX)
        self.IndicatorSetForeground(2, wx.Colour(100, 100, 0)) 
        

    def OnKeyPressed(self, event):
        """Keydown event"""
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
                
        if 27 < key < 256:
            keyname = chr(key)
            #self.parent.modified = True
            #self.parent.load_title()
        else:
            keyname = None

        if key == 32 and event.ControlDown():
            kw = keyword.kwlist[:]

            kw.sort()  # Python sorts are case sensitive
            self.AutoCompSetIgnoreCase(False)  # so this needs to match

            for i in range(len(kw)):
                if kw[i] in keyword.kwlist:
                    kw[i] = kw[i]

            self.AutoCompShow(0, " ".join(kw))
        
        elif keyname == 'S' and event.ControlDown(): # CTRL+S
            self.parent.save()
        
        else:
            event.Skip()
            
            
    def highlight(self, pos, length):
        """Highlight a specific position in the script (the method name)"""
        self.StartStyling(pos, wx.stc.STC_INDICS_MASK)
        self.SetStyling(length, wx.stc.STC_INDIC2_MASK)

            

        
    
        
        
        