#!/usr/bin/python

import wx
import wx.lib.dialogs
import wx.stc as stc
import keyword
import os
from xml.dom.minidom import parse
import xml.dom.minidom

# Font for each Operating System platform
if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Monaco',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        self.filename = ''
        self.normalStylesFore = dict()
        self.normalStylesBack = dict()
        self.pythonStylesFore = dict()
        self.pythonStylesBack = dict()
        
        self.foldSymbols = 2
        self.lineNumbersEnabled = True
        self.leftMarginWidth = 25

        wx.Frame.__init__(self, parent, title=title, size=(1036, 652))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

# Inorder to Zoomin, hold Ctrl + '+'key
        self.control.CmdKeyAssign(ord('+'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
# Inorder to Zoomout, hold Ctrl + '-' Key        
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.control.SetLexer(stc.STC_LEX_PYTHON)
        self.control.SetKeyWords(0, " ".join(keyword.kwlist))

        self.control.SetViewWhiteSpace(False)
        self.control.SetProperty("fold", "1")
        self.control.SetProperty("tab.timmy.whinge.level", "1")

        self.control.SetMargins(5,0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        if self.foldSymbols == 0:
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.foldSymbols == 1:
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.foldSymbols == 2:
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

        elif self.foldSymbols == 3:
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")

        self.CreateStatusBar()
        self.UpdateLineCol(self)
        self.StatusBar.SetBackgroundColour((220,220,220))
# ToolBar, ToolBar icons and functions.
        toolBar = self.CreateToolBar()
        tb = toolBar
        newToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'New file',
                                             wx.Bitmap('icons/toolbar/new.png'))
        
        openToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Open file',
                                              wx.Bitmap('icons/toolbar/open.png'))
        
        saveToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Save file',
                                              wx.Bitmap('icons/toolbar/save.png'))
        
        saveasToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Save As',
                                                wx.Bitmap('icons/toolbar/saveas.png'))
        tb.AddSeparator()
        
        undoToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Undo',
                                              wx.Bitmap('icons/toolbar/undo.png'))
        
        redoToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Redo',
                                              wx.Bitmap('icons/toolbar/redo.png'))
        tb.AddSeparator()

        copyToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Copy',
                                              wx.Bitmap('icons/toolbar/copy.png'))

        cutToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Cut',
                                             wx.Bitmap('icons/toolbar/cut.png'))

        pasteToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Paste',
                                               wx.Bitmap('icons/toolbar/paste.png'))

        deleteToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Delete',
                                                wx.Bitmap('icons/toolbar/delete.png'))
        tb.AddSeparator()

        helpToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Help',
                                              wx.Bitmap('icons/toolbar/help.png'))

        bugToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'ReportBug',
                                             wx.Bitmap('icons/toolbar/bug.png'))

        infoToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Info',
                                              wx.Bitmap('icons/toolbar/info.png'))

        quitToolButton = toolBar.AddLabelTool(wx.ID_ANY, 'Quit',
                                              wx.Bitmap('icons/toolbar/quit.png'))
        toolBar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnNew, newToolButton)
        self.Bind(wx.EVT_TOOL, self.OnOpen, openToolButton)
        self.Bind(wx.EVT_TOOL, self.OnSave, saveToolButton)
        self.Bind(wx.EVT_TOOL, self.OnSaveAs, saveasToolButton)
        self.Bind(wx.EVT_TOOL, self.OnUndo, undoToolButton)
        self.Bind(wx.EVT_TOOL, self.OnRedo, redoToolButton)
        self.Bind(wx.EVT_TOOL, self.OnCopy, copyToolButton)
        self.Bind(wx.EVT_TOOL, self.OnCut, cutToolButton)
        self.Bind(wx.EVT_TOOL, self.OnPaste, pasteToolButton)
        self.Bind(wx.EVT_TOOL, self.OnDelete, deleteToolButton)
        self.Bind(wx.EVT_TOOL, self.OnHowTo, helpToolButton)
        self.Bind(wx.EVT_TOOL, self.OnReportBug, bugToolButton)
        self.Bind(wx.EVT_TOOL, self.OnAbout, infoToolButton)
        self.Bind(wx.EVT_TOOL, self.OnClose, quitToolButton)

# File menu
        filemenu = wx.Menu()
        menuNew = filemenu.Append(wx.ID_NEW, "&New", " Create a new document! (Ctrl+N)")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open File...", " Open a document/file (Ctrl+O)")
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", " Save it-> (Ctrl+S)")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save &As", " Save a new document or Save as(Alt+S)")
        filemenu.AppendSeparator()
        menuClose = filemenu.Append(wx.ID_EXIT, "&Close", " Close Grim(Ctrl+W)")
# Edit menu
        editmenu = wx.Menu()
        menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", " Undo your last action (Ctrl+Z)")
        menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", " Redo your last action (Ctrl+Y)")
        editmenu.AppendSeparator()
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "&Select All", " Select all the entire data in the document(Ctrl+A)")
        menuCopy = editmenu.Append(wx.ID_COPY, "&Copy", " Copies the selected text to clipboard (Ctrl+C)")
        menuCut = editmenu.Append(wx.ID_CUT, "C&ut", " Cuts the selected text and copies to clipboard (Ctrl+X)")
        menuPaste = editmenu.Append(wx.ID_PASTE, "&Paste", " Paste the copied text from the clipboard (Ctrl+V)")
        menuDelete = editmenu.Append(wx.ID_DELETE, "&Delete", "Delete Selected text (Del)")
# Preferences menu
        prefmenu = wx.Menu()
        menuLineNumbers = prefmenu.Append(wx.ID_ANY, "Toggle &with Line Numbers", " Show/Hide the line numbers column")
# Help menu
        helpmenu = wx.Menu()
        menuHowTo = helpmenu.Append(wx.ID_ANY, "&How To...", " Get help using Grim(F1)")
        helpmenu.AppendSeparator()
        menuBugReport = helpmenu.Append(wx.ID_ANY, "&Report Bug!", "Report a bug if you have faced one!")
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About", " Know about Grim(F2)")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(prefmenu, "&Preferences")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
# MenuBar-File menu
        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)
# MenuBar-Edit menu
        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)
        self.Bind(wx.EVT_MENU, self.OnDelete, menuDelete)
# MenuBar-Preferences menu
        self.Bind(wx.EVT_MENU, self.OnToggleLineNumbers, menuLineNumbers)
# MenuBar-Help menu
        self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)
        self.Bind(wx.EVT_MENU, self.OnReportBug, menuBugReport)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)
        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)
        self.control.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.control.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.control.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.control.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        self.Show()

        self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.control.StyleClearAll()

        self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.control.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.control.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.control.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
        self.control.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")

        self.ParseSettings("grim_themes/grim_normal_theme.xml")
        self.SetStyling()

    def SetStyling(self):
        pSFore = self.pythonStylesFore
        pSBack = self.pythonStylesBack
        nSFore = self.normalStylesFore
        nSBack = self.normalStylesBack

        self.control.StyleSetBackground(stc.STC_STYLE_DEFAULT, nSBack["Main"])
        self.control.SetSelBackground(True, "#333333")

        self.control.StyleSetSpec(stc.STC_P_DEFAULT, "fore:%s,back:%s" % (pSFore["Default"], pSBack["Default"]))
        self.control.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:%s,back:%s" % (pSFore["Comment"], pSBack["Comment"]))
        self.control.StyleSetSpec(stc.STC_P_COMMENTLINE, "face:%(other)s,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_NUMBER, "fore:%s,back:%s" % (pSFore["Number"], pSBack["Number"]))
        self.control.StyleSetSpec(stc.STC_P_NUMBER, "size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_STRING, "fore:%s,back:%s" % (pSFore["String"], pSBack["Number"]))
        self.control.StyleSetSpec(stc.STC_P_STRING, "face:%(helv)s,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_CHARACTER, "fore:%s,back:%s" % (pSFore["SingleQuoteString"], pSBack["SingleQuoteString"]))
        self.control.StyleSetSpec(stc.STC_P_CHARACTER, "face:%(helv)s,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_WORD, "fore:%s,back:%s" % (pSFore["Keyword"], pSBack["Keyword"]))
        self.control.StyleSetSpec(stc.STC_P_WORD, "bold,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_TRIPLE, "fore:%s,back:%s" % (pSFore["TripleQuote"], pSBack["TripleQuote"]))
        self.control.StyleSetSpec(stc.STC_P_TRIPLE, "size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:%s,back:%s" % (pSFore["TripleDoubleQuote"], pSBack["TripleDoubleQuote"]))
        self.control.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:%s,back:%s" % (pSFore["ClassName"], pSBack["ClassName"]))
        self.control.StyleSetSpec(stc.STC_P_CLASSNAME, "bold,underline,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_DEFNAME, "fore:%s,back:%s" % (pSFore["FunctionName"], pSBack["FunctionName"]))
        self.control.StyleSetSpec(stc.STC_P_DEFNAME, "bold,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_OPERATOR, "fore:%s,back:%s" % (pSFore["Operator"], pSBack["Operator"]))
        self.control.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:%s,back:%s" % (pSFore["Identifier"], pSBack["Identifier"]))
        self.control.StyleSetSpec(stc.STC_P_IDENTIFIER, "face:%(helv)s,size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:%s,back:%s" % (pSFore["CommentBlock"], pSBack["CommentBlock"]))
        self.control.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "size:%(size)d" % faces)

        self.control.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:%s,back:%s" % (pSFore["StringEOL"], pSBack["StringEOL"]))
        self.control.StyleSetSpec(stc.STC_P_STRINGEOL, "face:%(mono)s,eol,size:%(size)d" % faces)

        self.control.SetCaretForeground(pSFore["Caret"])
        self.control.SetCaretLineBackground(pSBack["CaretLine"])
        self.control.SetCaretLineVisible(True)

    def OnNew(self, e):
        self.filename = ""
        self.control.SetValue("")

    def OnOpen(self, e):
        try:
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'r')
                self.control.SetValue(f.read())
                f.close()
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Couldn't open file\nWere you trying to open a machine coded file?", "Error: Soul couldn't be recognised", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def OnSave(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.control.GetValue())
            f.close()
        except:
            try:
                dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if (dlg.ShowModal() == wx.ID_OK):
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
            except:
                pass

    def OnSaveAs(self, e):
        try:
            dlg = wx.FileDialog(self, "Save file as", self.dirname, self.filename, "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w')
                f.write(self.control.GetValue())
                f.close()
            dlg.Destroy()
        except:
            pass

    def OnClose(self, e):
        self.Close(True)

    def OnUndo(self, e):
        self.control.Undo()

    def OnRedo(self, e):
        self.control.Redo()

    def OnSelectAll(self, e):
        self.control.SelectAll()

    def OnCopy(self, e):
        self.control.Copy()

    def OnCut(self, e):
        self.control.Cut()

    def OnPaste(self, e):
        self.control.Paste()

    def OnDelete(self, event):
        frm, to = self.control.GetSelection()
        self.control.Remove(frm, to)

    def OnToggleLineNumbers(self, e):
        if (self.lineNumbersEnabled):
            self.control.SetMarginWidth(1,0)
            self.lineNumbersEnabled = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnabled = True

    def OnHowTo(self, e):
        f = open("help/HowTouse.soul", "r")
        msg = f.read()
        f.close()
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg, "How To?", size=(400, 500))
        dlg.ShowModal()
        dlg.Destroy()

    def OnReportBug(self, e):
        bug = wx.AboutDialogInfo()
        bug.Name = "How to report a bug?"
        bug.Description = "If you have faced any bug on Grim, then click the below link\nto report a bug. Make sure it's a bug.\nYou can also use the Report_Bug_here.html file located on help/ReportBug/ folder."
        bug.WebSite = ("https://tawk.to/chat/593cf9f4b3d02e11ecc6941c/default/?$_tawk_popout=true", "Report Bug here!")

        wx.AboutBox(bug)

    def OnAbout(self, e):
        info = wx.AboutDialogInfo()
        info.Name = "Grim Text Editor"
        info.Version = "v1.0.0(Stable)"
        info.Copyright = "(C) 2018 Master-Console_ Inc."
        info.Description = "This is Grim, an Advanced simple yet another Text Editor.\nWritten in: Python\nAvailable on Github"
        info.WebSite = ("http://www.masterconsoleblog.wordpress.com", "Visit Master-Console_ Inc.")
        info.Developers = ["Yet Zio, Master-Console_ Inc. Affiliates"]
        info.License = "This product is licensed under the MIT License (MIT)"
        
        wx.AboutBox(info)


    def UpdateLineCol(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "You are on Line: %s, Column: %s" % (line, col)
        self.StatusBar.SetStatusText(stat, 0)

    def OnLeftUp(self, e):
        self.UpdateLineCol(self)
        e.Skip()

    def OnCharEvent(self, e):
        keycode = e.GetKeyCode()
        controlDown = e.CmdDown()
        altDown = e.AltDown()
        shiftDown = e.ShiftDown()
        # Ctrl + N
        if (keycode == 14):
            self.OnNew(self)
        # Ctrl + O    
        elif (keycode == 15):
            self.OnOpen(self)
        # Ctrl + S   
        elif (keycode == 19):
            self.OnSave(self)
        # Alt + S   
        elif (altDown and (keycode == 115)):
            self.OnSaveAs(self)
        # Ctrl + W    
        elif (keycode == 23):
            self.OnClose(self)
        # Ctrl + A    
        elif (keycode == 1):
            self.OnSelectAll(self)
        # F1    
        elif (keycode == 340):
            self.OnHowTo(self)
        # F2    
        elif (keycode == 341):
            self.OnAbout(self)
        else:
            e.Skip()

    def OnUpdateUI(self, e):
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.control.GetCurrentPos()

        if (caretPos > 0):
            charBefore = self.control.GetCharAt(caretPos - 1)
            styleBefore = self.control.GetStyleAt(caretPos - 1)

        if (charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR):
            braceAtCaret = caretPos - 1

        if (braceAtCaret < 0):
            charAfter = self.control.GetCharAt(caretPos)
            styleAfter = self.control.GetStyleAt(caretPos)

            if (charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR):
                braceAtCaret = caretPos

        if (braceAtCaret >= 0):
            braceOpposite = self.control.BraceMatch(braceAtCaret)

        if (braceAtCaret != -1 and braceOpposite == -1):
            self.control.BraceBadLight(braceAtCaret)
        else:
            self.control.BraceHighlight(braceAtCaret,braceOpposite)

    def OnMarginClick(self, e):
        if (e.GetMargin() == 2):
            if (e.GetShift() and e.GetControl()):
                self.control.FoldAll()
            else:
                lineClicked = self.control.LineFromPosition(e.GetPosition())

                if (self.control.GetFoldLevel(lineClicked) & stc.STC_P_FOLDLEVELHEADERFLAG):
                    if (e.GetShift()):
                        self.control.SetFoldExpanded(lineClicked, True)
                        self.control.Expand(lineClicked, True, True, -1)
                    elif (e.GetControl()):
                        if (self.control.GetFoldExpaned(lineClicked)):
                            self.control.SetFoldExpanded(lineClicked, False)
                            self.control.Expand(lineClicked, False, True, 0)
                        else:
                            self.control.SetFoldExpanded(lineClicked, True)
                            self.control.Expand(lineClicked, True, True, 100)
                    else:
                        self.control.ToggleFold(lineClicked)

    def FoldAll(self):
        lineCount = self.control.GetLineCount()
        expanding = True

        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
                (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

        lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1

        return line

    def OnKeyPressed(self, e):
        if (self.control.CallTipActive()):
            self.control.CallTipCancel()
        key = e.GetKeyCode()

        if (key == 32 and e.ControlDown()):
            pos = self.control.GetCurrentPos()

            if (e.ShiftDown()):
                self.control.CallTipSetBackground("yellow")
                self.control.CallTipShow(pos, "Press <Ctrl> + <Space> for code completion")
            else:
                kw = keyword.kwlist[:]
                kw.sort()
                self.control.AutoCompSetIgnoreCase(False)
                self.control.AutoCompShow(0, " ".join(kw))
        else:
            e.Skip()


    def ParseSettings(self, settings_file):
        DOMTree = xml.dom.minidom.parse(settings_file)
        collection = DOMTree.documentElement

        styles = collection.getElementsByTagName("style")
        for s in styles:
            item = s.getElementsByTagName("item")[0].childNodes[0].data
            color = s.getElementsByTagName("color")[0].childNodes[0].data
            side = s.getElementsByTagName("side")[0].childNodes[0].data
            sType = s.getAttribute("type")
            if sType == "normal":
                if side == "Back":
                    self.normalStylesBack[str(item)] = str(color)
                else:
                    self.normalStylesFore[str(item)] = str(color)
            elif sType == "python":
                if side == "Back":
                    self.pythonStylesBack[str(item)] = str(color)
                else:
                    self.pythonStylesFore[str(item)] = str(color)
                    
    def OnTerminal(self, e):
        terminal_directory = self.GetCurrentPage().directory
        os.system("gnome-terminal --maximize --working-directory=" + terminal_directory)

app = wx.App(False)
frame = MainWindow(None, "Grim Text Editor")
frame.SetIcon(wx.Icon('icons/Grim_editor_stable.ico', wx.BITMAP_TYPE_ICO))
app.MainLoop()

# This file was
# Created by Yet Zio on 11th April 2018
# (C) 2018 Master-Console_ Inc.
# grim_main.py
