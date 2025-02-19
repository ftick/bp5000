import wx
try:
    from ObjectListView import ObjectListView
except:
    ObjectListView = False

#----------------------------------------------------------------------
def getWidgets(parent):
    """
    Return a list of all the child widgets
    """
    items = [parent]
    for item in parent.GetChildren():
        items.append(item)
        if hasattr(item, "GetChildren"):
            for child in item.GetChildren():
                items.append(child)
    return items

#----------------------------------------------------------------------
def darkRowFormatter(listctrl, dark=False):
    """
    Toggles the rows in a ListCtrl or ObjectListView widget. 
    Based loosely on the following documentation:
    http://objectlistview.sourceforge.net/python/recipes.html#recipe-formatter
    and http://objectlistview.sourceforge.net/python/cellEditing.html
    """
    
    listItems = [listctrl.GetItem(i) for i in range(listctrl.GetItemCount())]
    for index, item in enumerate(listItems):
        if dark:
            if index % 2:
                item.SetBackgroundColour("Dark Grey")
            else:
                item.SetBackgroundColour("Light Grey")
        else:
            if index % 2:
                item.SetBackgroundColour("Light Blue")
            else:
                item.SetBackgroundColour("Yellow")
        listctrl.SetItem(item)

#----------------------------------------------------------------------
def darkMode(self, dark_mode):
    """
    Sets dark mode
    """
    widgets = getWidgets(self)
    print(dark_mode)
    for widget in widgets:
        if dark_mode:
            if isinstance(widget, type(ObjectListView)) or isinstance(widget, type(wx.ListCtrl)):
                darkRowFormatter(widget, dark=True)
            widget.SetBackgroundColour("Dark Grey")
            widget.SetForegroundColour("White")
        else:
            if isinstance(widget, type(ObjectListView)) or isinstance(widget, type(wx.ListCtrl)):
                darkRowFormatter(widget)
            widget.SetBackgroundColour(wx.NullColour)
            widget.SetForegroundColour("Black")
    self.Refresh()
    return dark_mode
