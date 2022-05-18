import wx
import sys
import wx.lib.agw.flatnotebook as fnb
from dark import darkMode
import importplayers
import data
import grf
import bracketfuncs
import bracketio
from options import Options
#
# Tested with wx version 4 (phoenix) and python 3.6.1
#
VERSION_NUMBER = 2.0000
VERTICAL = 0
HORIZONTAL = 1


class MFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MFrame, self).__init__(*args, **kwargs)
        self.darkToggled = True
        self.setup()

    def setup(self):
        menubar = wx.MenuBar()
        filem = wx.Menu()
        helpm = wx.Menu()
        setm = wx.Menu()
        new = filem.Append(wx.ID_NEW, '&New Tournament\tCtrl+N')
        open_ = filem.Append(wx.ID_OPEN, '&Open Tournament\tCtrl+O')
        filem.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.new_event, new)
        qmi = wx.MenuItem(filem, wx.ID_EXIT, '&Quit\tCtrl+W')
        filem.Append(qmi)

        about = helpm.Append(wx.ID_ANY, '&About BP5000')
        options = setm.Append(wx.ID_ANY, '&Options')

        # setm.AppendSeparator()
        # # dark_ = setm.Append(wx.ID_ANY, '&Toggle Dark Mode\tCtrl+D')
        # dark_ = setm.Append(wx.ID_ANY, '&Toggle Dark Mode')
        # self.Bind(wx.EVT_MENU, self.dark_event, dark_)

        self.Bind(wx.EVT_MENU, self.quit_event, qmi)
        self.Bind(wx.EVT_MENU, self.load_event, open_)
        self.Bind(wx.EVT_MENU, self.about_event, about)
        self.Bind(wx.EVT_MENU, self.options_event, options)

        self.options = Options()
        menubar.Append(filem, '&File')
        menubar.Append(setm, '&Settings')
        menubar.Append(helpm, '&Help')
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

    def about_event(self, e):
        hlptxt = (" https://github.com/ftick/bp5000 \n"
                  "Bracket Program 5000 developed by"
                  " Isaiah (IR) & ftick.\n\nVersion "+str(VERSION_NUMBER))
        dia = wx.MessageDialog(self, hlptxt, "About BP5000")
        dia.ShowModal()

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
        name = dia.GetFilename().replace(".bp5", "")
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

    def options_event(self, e):
        d = wx.Dialog(None)
        
        o = self.options
        y = 10
        components = []
        for opt in o.listopt():
            t = type(opt[2])
            if t == type(2):
                #sc = wx.SpinCtrl(d, pos=(180, y),
                pass
            if t == type(True):
                chk = wx.CheckBox(d, pos=(180, y) , label=opt[1])
                chk.SetValue(opt[2])
                if opt[0] == "exprender":
                    for i01 in range(0, self.nb.GetPageCount()):
                        if isinstance(self.nb.GetPage(i01), BracketPage):
                            chk.Disable()
                components.append((opt[0], chk))
            y += 30
        d.SetTitle("Options")
        d.SetSize((250, y+100))
        d.ShowModal()
        for x in components:
            o.update(**{x[0]:x[1].GetValue()})
        self.options = o
        
    def dark_event(self, e):
        darkMode(self, self.darkToggled)
        self.darkToggled = not self.darkToggled

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
        t4 = 'Import players from Challonge'
        challongebtn = wx.Button(self.opanel, label=t4)
        t5 = 'Import players from StartGG'
        startggbtn = wx.Button(self.opanel, label=t5)
        savebtn = wx.Button(self.opanel, id=wx.ID_SAVE,  label="Save")

        self.hsplit.Add(vsplit, 1, wx.ALIGN_LEFT | wx.EXPAND)
        self.hsplit.Add(self.opanel, 1, wx.ALIGN_RIGHT | wx.EXPAND)
        btnsz = wx.StaticBoxSizer(wx.StaticBox(self.opanel,
                                               label="Tournament Utilities"),
                                  wx.VERTICAL)
        btnsz.Add(projbtn, 0, wx.EXPAND)
        btnsz.Add(placebtn, 0, wx.EXPAND)
        btnsz.Add(genbtn, 0, wx.EXPAND)
        btnsz.Add(challongebtn, 0, wx.EXPAND)
        btnsz.Add(startggbtn, 0, wx.EXPAND)
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
        rsdstr = "Avoid rematches in losers bracket when possible"
        self.reseed = wx.CheckBox(self.opanel, label=rsdstr)
        opsz.Add(self.reseed, 0, wx.EXPAND)
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

        def projhtxt(e):
            prjt0 = "View the projected bracket, a bracket where the "
            prjt1 = "expected winners are shown by seed."
            self.helplbl.SetLabel(prjt0+prjt1)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        self.Bind(wx.EVT_BUTTON, self.proj, projbtn)
        projbtn.Bind(wx.EVT_ENTER_WINDOW, projhtxt)
        projbtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)

        def genhtxt(e):
            ght = "Generate a list of entrants from a template."
            self.helplbl.SetLabel(ght)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        self.Bind(wx.EVT_BUTTON, self.gen, genbtn)
        genbtn.Bind(wx.EVT_ENTER_WINDOW, genhtxt)
        genbtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)

        def placehtxt(e):
            plct = "View each entrants placing in the tournament."
            self.helplbl.SetLabel(plct)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        self.Bind(wx.EVT_BUTTON, self.place, placebtn)
        placebtn.Bind(wx.EVT_ENTER_WINDOW, placehtxt)
        placebtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)

        def challongehtxt(e):
            cht = "Import players from a Challonge bracket."
            self.helplbl.SetLabel(cht)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        self.Bind(wx.EVT_BUTTON, self.challonge, challongebtn)
        challongebtn.Bind(wx.EVT_ENTER_WINDOW, challongehtxt)
        challongebtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)

        def startgghtxt(e):
            sggt = "Import players from a Challonge bracket."
            self.helplbl.SetLabel(sggt)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        self.Bind(wx.EVT_BUTTON, self.startgg, startggbtn)
        startggbtn.Bind(wx.EVT_ENTER_WINDOW, startgghtxt)
        startggbtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)
        
        def updatehtxt(e):
            ut = "Update or start the tournament with the provided entrants."
            self.helplbl.SetLabel(ut)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()
        
        self.Bind(wx.EVT_BUTTON, self.update, updatebtn)
        updatebtn.Bind(wx.EVT_ENTER_WINDOW, updatehtxt)
        updatebtn.Bind(wx.EVT_LEAVE_WINDOW, blankhtxt)

        def savehtxt(e):
            st1 = "Save the tournament to a file,"
            st2 = " so it can be loaded at a later time."
            self.helplbl.SetLabel(st1+st2)
            self.helplbl.Wrap(self.helpsz.GetSize()[0])
            e.Skip()

        self.Bind(wx.EVT_BUTTON, self.save, savebtn)
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
            if len(brackets) == 1:
                return
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
        brackets = data.create(players, int(self.elim), self.reseed.GetValue())
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

        if len(brackets) == 1:
            return  # Single elim, no finals
        fb = FinalPage(self.parent, brackets)
        fb.sname = self.name
        self.parent.AddPage(fb, self.name + ": Finals")

    def proj(self, e):
        players = self.elist.GetValue().split("\n")
        if (players[-1] == ''):
            players = players[:-1]
        brackets = data.create(players, int(self.elim), self.reseed.GetValue())
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

        if len(brackets) == 1:
            return
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
    
    def challonge(self, e):
        h = 220
        d = wx.Dialog(None)
        # orgl = wx.StaticText(d, pos=(20, 7), label="Organization ID")
        # org = wx.TextCtrl(d, pos=(20, 24), size=(190, 20), )
        # urll = wx.StaticText(d, pos=(20, 57), label="Tournament URL")
        # url = wx.TextCtrl(d, pos=(20, 74), size=(190, 20))
        urll = wx.StaticText(d, pos=(20, 57), label="Tournament URL")
        url = wx.TextCtrl(d, pos=(20, 74), size=(190, 20))
        okbtn = wx.Button(d, label='OK', pos=(30, h-70))

        def newev(e):
            d.Close()
            bstr = ""
            challongeURL = url.GetValue()
            entrants = importplayers.entrants_challongeurl(challongeURL)
            for entrant in entrants:
                bstr += entrant + "\n"
            self.elist.SetValue(bstr)

        d.Bind(wx.EVT_BUTTON, newev, okbtn)
        cancelbtn = wx.Button(d, label='Cancel', pos=(150, h-70))

        def c(e):
            d.Close()

        d.Bind(wx.EVT_BUTTON, c, cancelbtn)
        d.SetSize((250, h))
        d.SetTitle("Challonge Import")
        d.Show(True)
    
    def startgg(self, e):
        h = 220
        d = wx.Dialog(None)
        # evtl = wx.StaticText(d, pos=(20, 7), label="Event ID")
        # evt = wx.TextCtrl(d, pos=(20, 24), size=(190, 20), )
        # urll = wx.StaticText(d, pos=(20, 57), label="Tournament ID")
        # url = wx.TextCtrl(d, pos=(20, 74), size=(190, 20))
        urll = wx.StaticText(d, pos=(20, 57), label="Tournament URL")
        url = wx.TextCtrl(d, pos=(20, 74), size=(190, 20))
        okbtn = wx.Button(d, label='OK', pos=(30, h-70))

        def newev(e):
            d.Close()
            bstr = ""
            startggURL = url.GetValue()
            entrants = importplayers.entrants_startggurl(startggURL)
            for entrant in entrants:
                bstr += entrant + "\n"
            self.elist.SetValue(bstr)

        d.Bind(wx.EVT_BUTTON, newev, okbtn)
        cancelbtn = wx.Button(d, label='Cancel', pos=(150, h-70))

        def c(e):
            d.Close()

        d.Bind(wx.EVT_BUTTON, c, cancelbtn)
        d.SetSize((250, h))
        d.SetTitle("StartGG Import")
        d.Show(True)


class BracketPage(wx.Panel):

    def __init__(self, parent, bracket):
        self.bracket = bracket
        self.oldx = None
        self.oldy = None

        self.ax = 0
        self.ay = 0
        self.bx = 0
        self.by = 0
        self.extimg = None
        wx.Panel.__init__(self, parent)
        self.x = 0
        self.y = 0
        self.updatebracketimg()
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.mouse)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.none)

    def none(self, ev):
        pass

    def paint(self, ev):
        dc = wx.PaintDC(ev.GetEventObject())
        if self.dirty:
            dc.Clear()
            self.dirty = False
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
        # update if within 100px of borders
        if self.GetParent().GetParent().GetParent().options.get("exprender"):
            if ((self.x < 100 and self.ax > 0) or (self.y < 100 and self.ay > 0)) or ((self.x + w > 1900) or (self.y + h > 1900)):
                self.updatebracketimg()
        sub = wx.Rect(self.x, self.y, w, h)
        bimg = wx.Bitmap(self.img.GetSubImage(sub))
        dc.DrawBitmap(bimg, bx, by)
        if self.extimg:
            param0 = wx.Bitmap(piltowx(self.extimg[0]))
            param1 = self.extimg[1]-self.x+self.bx
            param2 = self.extimg[2]-self.y+self.by
            dc.DrawBitmap(param0, param1, param2)

    def mouse(self, ev):
        comp = False
        x, y = (ev.GetX(), ev.GetY())
        delta = ev.GetWheelDelta()
        rote = ev.GetWheelRotation()
        if(delta > 0 and abs(rote) >= delta):
            axis = ev.GetWheelAxis() # 0 = vertical, 1 = horizontal
            rotes = rote / delta
            if (axis == VERTICAL):
                self.y -= rotes * 50
                if(self.y < 0):
                    self.y = 0
            if (axis == HORIZONTAL):
                self.x += rotes * 50
                if(self.x < 0):
                    self.x = 0
            self.Refresh()
        else:
            if(ev.LeftIsDown() or ev.MiddleIsDown()):
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
        if self.GetParent().GetParent().GetParent().options.get("exprender"):
            self.extimg = None
        else:
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
        #self.x, self.y -> screen position relative to buffer
        #self.ax, self.ay -> buffer loc
        #
        if not self.GetParent().GetParent().GetParent().options.get("exprender"):
            self.ax = 0
            self.ay = 0
            self.img = piltowx(grf.drawbracket(self.bracket))
            self.dirty = True
            self.Refresh()
            return

        print("TrueposORIG: ("+str(self.ax+self.x) + ", "+str(self.ay+self.y)+")")
        box = (2000, 2000)
        self.ax = int(self.ax + self.x - ((box[0]-self.GetSize()[0])/2))
        self.ay = int(self.ay + self.y - ((box[1]-self.GetSize()[1])/2))
        dy = 0
        dx = 0
        if self.ax < 0:
            dx = self.ax
            self.ax = 0
        if self.ay < 0:
            dy = self.ay
            self.ay = 0
        self.x = int((box[0]-self.GetSize()[0])/2) + dx
        self.y = int((box[1]-self.GetSize()[1])/2) + dy
        self.oldx = None
        self.oldy = None
        print("Updating img: @ ("+str(self.ax)+", "+str(self.ay)+") setxy ("+str(self.x)+", "+str(self.y)+")") 
        print("TrueposAFT: ("+str(self.ax+self.x) + ", "+str(self.ay+self.y)+")")
        imgp = grf.drawbracketFAST(self.bracket, (self.ax, self.ay, box[0], box[1]))
        self.img = piltowx(imgp)
        self.dirty = True
        self.Refresh()


class FinalPage(BracketPage):

    def updatebracketimg(self):
        self.img = piltowx(grf.drawfinals(self.bracket))
        self.dirty = True
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
        nw = wx.Button(self.pbot, label="no result", pos=(50, 15))
        rw = wx.Button(self.pbot, label="confirm", pos=(150, 15))
        self.vsplit.Add(self.ptop, 1, wx.ALIGN_TOP | wx.EXPAND)
        self.vsplit.Add(self.pbot, 1, wx.ALIGN_BOTTOM | wx.EXPAND)
        self.SetSizer(self.vsplit)

        def nowinner(e):
            self.match.settbd()
            self.parent.updatebracketimg()
            self.Close()
        
        def setwinner(e):
            self.match.setscore(pan.w1.GetValue(), pan.w2.GetValue())
            self.parent.updatebracketimg()
            self.Close()

        self.Bind(wx.EVT_BUTTON, nowinner, nw)
        self.Bind(wx.EVT_BUTTON, setwinner, rw)
        self.SetSize((300, 170))
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
        self.match = match
        self.parent = parent
        wx.Dialog.__init__(self, parent)
        self.vsplit = wx.BoxSizer(wx.VERTICAL)
        self.ptop = wx.Panel(self)
        self.pbot = wx.Panel(self)
        pan = ScoresPanel(self.ptop, match, self)
        nw = wx.Button(self.pbot, label="no result", pos=(50, 15))
        rw = wx.Button(self.pbot, label="confirm", pos=(150, 15))
        self.vsplit.Add(self.ptop, 1, wx.ALIGN_TOP | wx.EXPAND)
        self.vsplit.Add(self.pbot, 1, wx.ALIGN_BOTTOM | wx.EXPAND)
        self.SetSizer(self.vsplit)

        def nowinner(e):
            self.match.settbd()
            self.parent.updatebracketimg()
            self.Close()
        
        def setwinner(e):
            if(self.match.doscore(pan.w1.GetValue(), pan.w2.GetValue())):
                self.parent.updatebracketimg()
                self.Close()
            else:
                pan.w1.SetValue(0)
                pan.w2.SetValue(0)

        self.Bind(wx.EVT_BUTTON, nowinner, nw)
        self.Bind(wx.EVT_BUTTON, setwinner, rw)
        self.SetSize((300, 170))
        self.SetTitle("Report Scores")
        self.Show()


class ScoresPanel(wx.Panel):

    def __init__(self, parent, match, dilog, pos=(0, 0)):
        wx.Panel.__init__(self, parent, pos=pos, size=(300, 75))
        lbltext = "Report Scores"
        lbl = wx.StaticText(self, label=lbltext, pos=(30, 0))
        # l1 = wx.StaticText(self, label=str(match.part1), pos=(23, 60))
        # l2 = wx.StaticText(self, label=str(match.part2), pos=(173,60))
        l1 = wx.StaticText(self, label="0", pos=(23, 60))
        l2 = wx.StaticText(self, label="0", pos=(173,60))
        self.w1 = wx.SpinCtrl(self, min=-99, max=99, pos=(30, 20), size=(50, 30))
        self.w2 = wx.SpinCtrl(self, min=-99, max=99, pos=(180, 20), size=(50,30))

        #self.Bind(wx.EVT_BUTTON, dilog.winner1, w1)
        #self.Bind(wx.EVT_BUTTON, dilog.winner2, w2)


def piltowx(pil):
    wxi = wx.Image(*pil.size)
    wxi.SetData(pil.copy().convert('RGB').tobytes())
    return wxi


a = wx.App()
MFrame(None)
a.MainLoop()
