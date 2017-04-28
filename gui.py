import wx
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
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, pos=(20, 30), label="Entrants List (Ordered by seed), 1 per line")
        elist = wx.TextCtrl(self, pos=(20, 60), size = (500, 500), style = wx.TE_MULTILINE)
        updatebtn = wx.Button(self, label='Update', pos=(840, 540))

a = wx.App()
MFrame(None)
a.MainLoop()

