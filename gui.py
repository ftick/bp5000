import wx
import data
import grf
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
        save = filem.Append(wx.ID_SAVE, '&Save Tournament')
        filem.AppendSeparator()
        
        self.Bind(wx.EVT_MENU, self.new_event, new)
        
        qmi = wx.MenuItem(filem, wx.ID_EXIT, '&Quit\tCtrl+W')
        filem.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.quit_event, qmi)

        menubar.Append(filem, '&File')
        self.SetMenuBar(menubar)
        
        p = wx.Panel(self)
        self.nb = wx.Notebook(p)

        sz = wx.BoxSizer()
        sz.Add(self.nb, 1, wx.EXPAND)
        p.SetSizer(sz)

        self.SetSize((950, 650))
        self.SetTitle('BP5000')
        self.Centre()
        self.Show(True)
    
    def new_event(self, e):
        h = 220
        d = wx.Dialog(None)
        sc = wx.SpinCtrl(d, pos= (180,10), min=1, initial=2, max=99, size=(40,40))
        scl = wx.StaticText(d, pos= (10,17), label="# of eliminations")
        name = wx.TextCtrl(d, pos= (20, 74), value="My Tournament", size=(190,40))
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
        d.SetSize((250,h))
        d.SetTitle("Create new")
        d.Show(True)
        
    
    def quit_event(self, e):
        self.Close()
        exit()


class ManagementPage(wx.Panel):
    def __init__(self, parent, name="tournament", elim="2"):
        self.elim = elim
        self.name = name
        self.parent = parent
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, pos=(20, 30), label="Entrants List (Ordered by seed), 1 per line")
        self.elist = wx.TextCtrl(self, pos=(20, 60), size = (500, 500), style = wx.TE_MULTILINE)
        updatebtn = wx.Button(self, label='Update', pos=(840, 540))
        self.Bind(wx.EVT_BUTTON, self.update, updatebtn)

    def update(self, e):
        brackets = data.create(self.elist.GetValue().split(), int(self.elim))
        if type(brackets) == type(""):
            w = wx.MessageDialog(self.parent, "Need more entrants for that # of elims", "Error", wx.OK)
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
            self.parent.AddPage(page, self.name +": "+ ename)


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
        #self.br = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(piltowx(grf.drawbracket(bracket))))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.mouse)

    def paint(self, ev):
        dc = wx.PaintDC(ev.GetEventObject())
        dc.Clear()
        w = min(self.GetSize()[0], self.img.GetWidth()-self.x)
        h = min(self.GetSize()[1], self.img.GetHeight()-self.y)
        bx, by = (0,0)
        if self.img.GetWidth() > self.GetSize()[0]:
            if self.x + self.GetSize()[0] > self.img.GetWidth():
                self.x = self.img.GetWidth() - self.GetSize()[0]
        else:
            bx = int(.5*(self.GetSize()[0] - self.img.GetWidth()))
            self.x = 0
            self.bx = bx
        if self.img.GetHeight() > self.GetSize()[1]:
            if self.y + self.GetSize()[1] > self.img.GetHeight():
                self.y = self.img.GetHeight() - self.GetSize()[1]
        else:
            by = int(.5*(self.GetSize()[1] - self.img.GetHeight()))
            self.y = 0
            self.by = by
        sub = wx.Rect(self.x, self.y, w, h)
        print(sub)
        #import pdb; pdb.set_trace()
        bimg = wx.BitmapFromImage(self.img.GetSubImage(sub))
        dc.DrawBitmap(bimg, bx, by)
        if self.extimg:
            dc.DrawBitmap(wx.BitmapFromImage(piltowx(self.extimg[0])), self.extimg[1]-self.x+self.bx, self.extimg[2]-self.y+self.bx)

    def mouse(self, ev):
        x, y = (ev.GetX(), ev.GetY())
        if(ev.LeftIsDown()):
            if self.oldx is None:
                self.oldx = x
                self.oldy = y
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
            self.oldx = None
            self.oldy = None
        old = self.extimg
        self.extimg = grf.mouse_ev(self.x+x-self.bx,self.y+y-self.by,self.bracket)
        if old != self.extimg:
            self.Refresh()

    def updatebracketimg(self):
        self.img = piltowx(grf.drawbracket(self.bracket))
    

def piltowx(pil):
    wxi = wx.EmptyImage(*pil.size)
    pilCopy = pil.copy()
    pilCopyRGB = pilCopy.convert('RGB')
    pilRgbData = pilCopyRGB.tobytes()
    wxi.SetData(pilRgbData)

    return wxi

a = wx.App()
MFrame(None)
a.MainLoop()


