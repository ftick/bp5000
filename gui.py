import wx
import sys
import wx.lib.agw.flatnotebook as fnb
import data
import grf
import bracketfuncs
import bracketio
#
# Tested with wx version 3 and python 2.7
#


class MFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MFrame, self).__init__(*args, **kwargs)
        self.setup()

    def setup(self):
        menubar = wx.MenuBar()
        filem = wx.Menu()
        new = filem.Append(wx.ID_NEW, '&New Tournament')
        open_ = filem.Append(wx.ID_OPEN, '&Open Tournament')
        filem.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.new_event, new)
        qmi = wx.MenuItem(filem, wx.ID_EXIT, '&Quit\tCtrl+W')
        filem.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.quit_event, qmi)
        self.Bind(wx.EVT_MENU, self.load_event, open_)
        menubar.Append(filem, '&File')
        self.SetMenuBar(menubar)
        p = wx.Panel(self)
        self.nb = fnb.FlatNotebook(p, agwStyle=fnb.FNB_X_ON_TAB)

        def pagechanged(event):
            col = wx.Colour(hash(self.nb.GetPage(event.GetSelection()).sname))
            self.nb.SetActiveTabColour(col)
            if isinstance(self.nb.GetPage(event.GetSelection()), BracketPage):
                self.nb.GetPage(event.GetSelection()).updatebracketimg()

        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, pagechanged)
        sz = wx.BoxSizer()
        sz.Add(self.nb, 1, wx.EXPAND)
        p.SetSizer(sz)
        self.Bind(wx.EVT_CLOSE, self.quit_event)
        self.SetSize((950, 650))
        self.SetTitle('BP5000')
        self.Centre()
        self.Show(True)

    def load_event(self, e):
        dia = wx.FileDialog(self, "Load Bracket",
                            "", "", "bp5000 bracket|*.bp5", wx.FD_OPEN)
        if dia.ShowModal() == wx.ID_CANCEL:
            return
        brs = bracketio.read_bracket(dia.GetPath())
        if isinstance(brs, str):
            w = wx.MessageDialog(self, brs, "Error", wx.ICON_ERROR)
            w.ShowModal()
            w.Destroy()
            return
        name = dia.GetPath().replace(".bp5", "")
        pg = ManagementPage(self.nb, name, len(brs), brs)
        self.nb.InsertPage(0, pg, name)

    def new_event(self, e):
        h = 220
        d = wx.Dialog(None)
        sc = wx.SpinCtrl(d, pos=(180, 10), min=1,
                         initial=2, max=99, size=(40, 40))
        scl = wx.StaticText(d, pos=(10, 17), label="# of eliminations")
        name = wx.TextCtrl(d, pos=(20, 74),
                           value="My Tournament", size=(190, 40))
        namel = wx.StaticText(d, pos=(20, 57), label="Tournament Name")
        okbtn = wx.Button(d, label='OK', pos=(30, h-70))

        def newev(e):
            d.Close()
            page = ManagementPage(self.nb, name.GetValue(), sc.GetValue())
            self.nb.AddPage(page, name.GetValue())

        d.Bind(wx.EVT_BUTTON, newev, okbtn)
        cancelbtn = wx.Button(d, label='Cancel', pos=(150, h-70))

        def c(e):
            d.Close()

        d.Bind(wx.EVT_BUTTON, c, cancelbtn)
        d.SetSize((250, h))
        d.SetTitle("Create new")
        d.Show(True)

    def quit_event(self, e):
        self.Destroy()
        sys.exit(0)


class ManagementPage(wx.Panel):

    def __init__(self, parent, name="tournament", elim="2", brackets=None):
        self.elim = elim
        self.name = name
        self.parent = parent
        self.sname = name
        wx.Panel.__init__(self, parent)
        self.hsplit = wx.BoxSizer(wx.HORIZONTAL)
        self.opanel = wx.Panel(self)
        t1 = "Entrants List (Ordered by seed), 1 per line"
        t = wx.StaticText(self, label=t1)
        self.elist = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        vsplit = wx.BoxSizer(wx.VERTICAL)
        vsplit.Add(t, 0, 0, 0)
        vsplit.Add(self.elist, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL)
        updatebtn = wx.Button(self.opanel, label='Update')
        t2 = 'Projected Bracket'
        projbtn = wx.Button(self.opanel, label=t2)
        t0 = 'Generate player list'
        genbtn = wx.Button(self.opanel, label=t0)
        t3 = 'View player placings'
        placebtn = wx.Button(self.opanel, label=t3)
        savebtn = wx.Button(self.opanel, id=wx.ID_SAVE,  label="Save")
        self.hsplit.Add(vsplit, 1, wx.ALIGN_LEFT | wx.EXPAND)
        self.hsplit.Add(self.opanel, 1, wx.ALIGN_RIGHT | wx.EXPAND)
        btnsz = wx.StaticBoxSizer(wx.StaticBox(self.opanel,
                                               label="Tournament Utilities"),
                                  wx.VERTICAL)
        btnsz.Add(projbtn, 0, wx.EXPAND)
        btnsz.Add(placebtn, 0, wx.EXPAND)
        btnsz.Add(genbtn, 0, wx.EXPAND)
        btnsz2 = wx.StaticBoxSizer(wx.StaticBox(self.opanel,
                                                label="Tournament Management"),
                                   wx.VERTICAL)
        btnsz2.Add(updatebtn, 0, wx.EXPAND)
        btnsz2.Add(savebtn, 0, wx.EXPAND)
        bsz = wx.BoxSizer(wx.VERTICAL)
        hsz = wx.BoxSizer(wx.HORIZONTAL)
        hsz.Add(btnsz, 1, wx.ALIGN_LEFT | wx.EXPAND)
        hsz.Add(btnsz2, 1, wx.ALIGN_RIGHT | wx.EXPAND)
        bsz.Add(hsz, 1, wx.ALIGN_TOP | wx.EXPAND)
        opsz = wx.StaticBoxSizer(wx.StaticBox(self.opanel,
                                              label="Tournament Options"),
                                 wx.VERTICAL)
        # add options
        self.helpsz = wx.StaticBoxSizer(wx.StaticBox(self.opanel,
                                                     label="Help"),
                                        wx.VERTICAL)
        self.helplbl = wx.StaticText(self.opanel, label="")
        self.helpsz.Add(self.helplbl)

        osz = wx.BoxSizer(wx.HORIZONTAL)
        osz.Add(opsz, 1, wx.ALIGN_RIGHT | wx.EXPAND)
        osz.Add(self.helpsz, 1, wx.ALIGN_LEFT | wx.EXPAND)
        bsz.Add(osz, 1, wx.ALIGN_BOTTOM | wx.EXPAND)
        self.opanel.SetSizer(bsz)
        self.SetSizer(self.hsplit)

        def blankhtxt(e):
            self.helplbl.SetLabel("")
            e.Skip()
        self.Bind(wx.EVT_BUTTON, self.update, updatebtn)

        def updatehtxt(e):
            ut = "Update or start the tournament with the provided entrants."
            self.helplbl.SetLabel(ut)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        updatebtn.Bind(wx.EVT_ENTER_WINDOW, updatehtxt)
        updatebtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)
        self.Bind(wx.EVT_BUTTON, self.proj, projbtn)

        def projhtxt(e):
            pt0 = "View the projected bracket, a bracket where the "
            pt1 = "expected winners are shown by seed."
            self.helplbl.SetLabel(pt0+pt1)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        projbtn.Bind(wx.EVT_ENTER_WINDOW, projhtxt)
        projbtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)
        self.Bind(wx.EVT_BUTTON, self.gen, genbtn)

        def genhtxt(e):
            HELPFULTEXT5000 = "Generate a list of entrants from a template."
            self.helplbl.SetLabel(HELPFULTEXT5000)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        genbtn.Bind(wx.EVT_ENTER_WINDOW, genhtxt)
        genbtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)
        self.Bind(wx.EVT_BUTTON, self.place, placebtn)

        def placehtxt(e):
            p196 = "View each entrants placing in the tournament."
            self.helplbl.SetLabel(p196)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        placebtn.Bind(wx.EVT_ENTER_WINDOW, placehtxt)
        placebtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)
        self.Bind(wx.EVT_BUTTON, self.save, savebtn)

        def savehtxt(e):
            t234 = "Save the tournament to a file,"
            t2345 = " so it can be loaded at a later time."
            self.helplbl.SetLabel(t234+t2345)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        savebtn.Bind(wx.EVT_ENTER_WINDOW, savehtxt)
        savebtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)
        if brackets:
            self.brackets = brackets
            i = -1

            # get participants from bracket, sorted.
            plist = []
            for m in brackets[0]:
                if not m.part1.isbye() and m.part1 not in plist:
                    plist.append(m.part1)
                if not m.part2.isbye() and m.part2 not in plist:
                    plist.append(m.part2)
            sortedplist = [None]*len(plist)
            # O(n) sort
            for i123 in plist:
                sortedplist[i123.seed-1] = i123

            self.elist.SetValue("\n".join([x.tag for x in sortedplist]))
            for b in brackets:
                i += 1
                page = BracketPage(self.parent, b)
                ename = "%sx LB" % i
                if i == 0:
                    ename = "WB"
                if i == 1:
                    ename = "LB"
                page.sname = self.name
                self.parent.AddPage(page, self.name + ": " + ename)
            fb = FinalPage(self.parent, brackets)
            fb.sname = self.name
            self.parent.AddPage(fb, self.name + ": Finals")

    def save(self, e):
        if not hasattr(self, "brackets"):
            errortext = "Make bracket before doing that"
            w = wx.MessageDialog(self.parent, errortext,
                                 "Error", wx.ICON_ERROR)
            w.ShowModal()
            w.Destroy()
            return
        dia = wx.FileDialog(self, "Save Bracket",
                            "", self.sname, "bp5000 bracket|*.bp5",
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dia.ShowModal() == wx.ID_CANCEL:
            return

        bracketio.write_bracket(dia.GetPath(), self.brackets)

    def place(self, e):
        if not hasattr(self, "brackets"):
            errortext = "Make bracket before doing that"
            w = wx.MessageDialog(self.parent, errortext,
                                 "Error", wx.ICON_ERROR)
            w.ShowModal()
            w.Destroy()
            return
        placel = bracketfuncs.placing(self.brackets)
        d = wx.Dialog(None)
        d.SetTitle("Results")
        a = wx.TextCtrl(d, style=wx.TE_MULTILINE)
        a.SetEditable(False)
        ptxt = ""
        for p in placel:
            if not p.isbye():
                ptxt += str(placel[p]) + ". " + p.tag + "\n"
        a.SetValue(ptxt)
        d.SetSize((250, 320))
        d.Show(True)

    def update(self, e):
        players = self.elist.GetValue().split("\n")
        if (players[-1] == ''):
            players = players[:-1]
        brackets = data.create(players, int(self.elim))
        self.brackets = brackets
        if isinstance(brackets, str):
            errortext = "Need more entrants for that # of elims"
            w = wx.MessageDialog(self.parent, errortext,
                                 "Error", wx.ICON_ERROR)
            w.ShowModal()
            w.Destroy()
            return
        i = -1

        for b in brackets:
            i += 1
            page = BracketPage(self.parent, b)
            ename = "%sx LB" % i
            if i == 0:
                ename = "WB"
            if i == 1:
                ename = "LB"
            page.sname = self.name
            self.parent.AddPage(page, self.name + ": " + ename)

        fb = FinalPage(self.parent, brackets)
        fb.sname = self.name
        self.parent.AddPage(fb, self.name + ": Finals")

    def proj(self, e):
        players = self.elist.GetValue().split("\n")
        if (players[-1] == ''):
            players = players[:-1]
        brackets = data.create(players, int(self.elim))
        if isinstance(brackets, str):
            errortext = "Need more entrants for that # of elims"
            w = wx.MessageDialog(self.parent,
                                 errortext, "Error", wx.ICON_ERROR)
            w.ShowModal()
            w.Destroy()
            return
        i = -1
        bracketfuncs.projected(brackets)

        for b in brackets:
            i += 1
            page = BracketPage(self.parent, b)
            ename = "%sx LB" % i
            if i == 0:
                ename = "WB"
            if i == 1:
                ename = "LB"
            page.sname = self.name+" [P]"
            self.parent.AddPage(page, self.name + " [P] : " + ename)

        fb = FinalPage(self.parent, brackets)
        fb.sname = self.name + " [P]"
        self.parent.AddPage(fb, self.name + " [P] : Finals")

    def gen(self, e):
        h = 220
        d = wx.Dialog(None)
        sc = wx.SpinCtrl(d, pos=(160, 10), size=(70, 40),
                         min=4, initial=32, max=1024*8)
        scl = wx.StaticText(d, pos=(10, 17), label="# of Players")
        name = wx.TextCtrl(d, pos=(20, 74), value="Player #", size=(190, 40))
        namel = wx.StaticText(d, pos=(20, 57), label="Player Template")
        okbtn = wx.Button(d, label='OK', pos=(30, h-70))

        def newev(e):
            d.Close()
            bstr = ""
            for i in range(1, sc.GetValue()+1):
                bstr += name.GetValue().replace("#", str(i)) + "\n"
            self.elist.SetValue(bstr)

        d.Bind(wx.EVT_BUTTON, newev, okbtn)
        cancelbtn = wx.Button(d, label='Cancel', pos=(150, h-70))

        def c(e):
            d.Close()

        d.Bind(wx.EVT_BUTTON, c, cancelbtn)
        d.SetSize((250, h))
        d.SetTitle("Create new")
        d.Show(True)


class BracketPage(wx.Panel):

    def __init__(self, parent, bracket):
        self.bracket = bracket
        self.oldx = None
        self.oldy = None
        self.x = 0
        self.y = 0
        self.bx = 0
        self.by = 0
        self.extimg = None
        wx.Panel.__init__(self, parent)
        self.updatebracketimg()
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.mouse)

    def paint(self, ev):
        dc = wx.PaintDC(ev.GetEventObject())
        dc.Clear()
        w = min(self.GetSize()[0], self.img.GetWidth()-self.x)
        h = min(self.GetSize()[1], self.img.GetHeight()-self.y)
        bx, by = (0, 0)
        if self.img.GetWidth() > self.GetSize()[0]:
            if self.x + self.GetSize()[0] > self.img.GetWidth():
                self.x = self.img.GetWidth() - self.GetSize()[0]
            self.bx = 0
        else:
            bx = int(.5*(self.GetSize()[0] - self.img.GetWidth()))
            self.x = 0
            self.bx = bx
        if self.img.GetHeight() > self.GetSize()[1]:
            if self.y + self.GetSize()[1] > self.img.GetHeight():
                self.y = self.img.GetHeight() - self.GetSize()[1]
            self.by = 0
        else:
            by = int(.5*(self.GetSize()[1] - self.img.GetHeight()))
            self.y = 0
            self.by = by
        sub = wx.Rect(self.x, self.y, w, h)
        bimg = wx.BitmapFromImage(self.img.GetSubImage(sub))
        dc.DrawBitmap(bimg, bx, by)
        if self.extimg:
            param0 = wx.BitmapFromImage(piltowx(self.extimg[0]))
            param1 = self.extimg[1]-self.x+self.bx
            param2 = self.extimg[2]-self.y+self.by
            dc.DrawBitmap(param0, param1, param2)

    def mouse(self, ev):
        comp = False
        x, y = (ev.GetX(), ev.GetY())
        if(ev.LeftIsDown()):
            if self.oldx is None:
                self.oldx = x
                self.oldy = y
                self.extimgc = self.extimg
                return
            self.x = self.x - (x - self.oldx)
            self.y = self.y - (y - self.oldy)
            self.oldx = x
            self.oldy = y
            if(self.x < 0):
                self.x = 0
            if(self.y < 0):
                self.y = 0
            self.Refresh()
        else:
            if not (self.oldx is None):
                comp = True
            self.oldx = None
            self.oldy = None
        old = self.extimg
        mevx, mevy = (self.x+x-self.bx, self.y+y-self.by)
        self.extimg = grf.mouse_ev(mevx, mevy, self.bracket)
        if old != self.extimg:
            self.Refresh()
        if comp and (self.extimg is not None) and self.extimg == self.extimgc:
            m = grf.mouse_ev(mevx, mevy, self.bracket, True)
            if m.part1 and m.part2:
                if m.isspecial():
                    SpecMatchDialog(self, m)
                else:
                    MatchDialog(self, m)

    def updatebracketimg(self):
        self.img = piltowx(grf.drawbracket(self.bracket))
        self.Refresh()


class FinalPage(BracketPage):

    def updatebracketimg(self):
        self.img = piltowx(grf.drawfinals(self.bracket))
        self.Refresh()


class MatchDialog(wx.Dialog):

    def __init__(self, parent, match):
        self.match = match
        self.parent = parent
        wx.Dialog.__init__(self, parent)
        self.vsplit = wx.BoxSizer(wx.VERTICAL)
        self.ptop = wx.Panel(self)
        self.pbot = wx.Panel(self)
        pan = ScoresPanel(self.ptop, match, self)
        nw = wx.Button(self.pbot, label="no result", pos=(100, 15))
        self.vsplit.Add(self.ptop, 1, wx.ALIGN_TOP | wx.EXPAND)
        self.vsplit.Add(self.pbot, 1, wx.ALIGN_BOTTOM | wx.EXPAND)
        self.SetSizer(self.vsplit)

        def nowinner(e):
            self.match.settbd()
            self.parent.updatebracketimg()
            self.Close()

        self.Bind(wx.EVT_BUTTON, nowinner, nw)
        self.SetSize((300, 150))
        self.SetTitle("Report Scores")
        self.Show()

    def winner1(self, e):
        self.match.setwinner(self.match.part1)
        self.parent.updatebracketimg()
        self.Close()

    def winner2(self, e):
        self.match.setwinner(self.match.part2)
        self.parent.updatebracketimg()
        self.Close()


class SpecMatchDialog(MatchDialog):
    def __init__(self, parent, match):
        if match.winner != 0:
            self.match = match
            self.parent = parent
            wx.Dialog.__init__(self, parent)
            self.vsplit = wx.BoxSizer(wx.VERTICAL)
            self.ptop = wx.Panel(self)
            self.pbot = wx.Panel(self)
            nw = wx.Button(self.pbot, label="no result", pos=(100, 15))
            self.vsplit.Add(self.ptop, 1, wx.ALIGN_TOP | wx.EXPAND)
            self.vsplit.Add(self.pbot, 1, wx.ALIGN_BOTTOM | wx.EXPAND)
            self.SetSizer(self.vsplit)

            def nowinner(e):
                self.match.settbd()
                self.parent.updatebracketimg()
                self.Close()

            self.Bind(wx.EVT_BUTTON, nowinner, nw)
            self.SetSize((300, 150))
            self.SetTitle("Report Scores")
            self.Show()
        else:
            super(SpecMatchDialog, self).__init__(parent, match)

    def winner1(self, e):
        self.match.lowerleft = self.match.lowerleft - 1
        if self.match.lowerleft == 0:
            self.match.setwinner(self.match.part1, self.match.upperleft)
            self.parent.updatebracketimg()
            self.Close()
        else:
            self.addpanel()

    def winner2(self, e):
        self.match.upperleft = self.match.upperleft - 1
        if self.match.upperleft == 0:
            self.match.setwinner(self.match.part2, self.match.lowerleft)
            self.parent.updatebracketimg()
            self.Close()
        else:
            self.addpanel()

    def addpanel(self):
        if hasattr(self, "ypos"):
            self.ypos += 70
        else:
            self.ypos = 70
        pan0 = ScoresPanel(self.ptop, self.match, self, pos=(0, self.ypos))
        self.SetSize((300, 150+self.ypos))


class ScoresPanel(wx.Panel):

    def __init__(self, parent, match, dilog, pos=(0, 0)):
        wx.Panel.__init__(self, parent, pos=pos, size=(300, 60))
        lbltext = "Pick the Winner of the Match"
        lbl = wx.StaticText(self, label=lbltext, pos=(30, 0))
        w1 = wx.Button(self, label=str(match.part1), pos=(30, 20))
        w2 = wx.Button(self, label=str(match.part2), pos=(180, 20))

        self.Bind(wx.EVT_BUTTON, dilog.winner1, w1)
        self.Bind(wx.EVT_BUTTON, dilog.winner2, w2)


def piltowx(pil):
    wxi = wx.EmptyImage(*pil.size)
    wxi.SetData(pil.copy().convert('RGB').tobytes())
    return wxi


a = wx.App()
MFrame(None)
a.MainLoop()
