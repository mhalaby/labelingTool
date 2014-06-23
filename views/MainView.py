import wx 
  
class mainView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View") 
        pnl = wx.Panel(self)
        width = 400
        height = 250        
        self.groupBox = wx.StaticBox(pnl, label="feedback", pos=(4, 5), size=(width, height + 40))
        sizer = wx.GridBagSizer(hgap=3, vgap=5)
        self.comment = wx.TextCtrl(pnl,style=wx.TE_READONLY| wx.TE_MULTILINE, size = wx.Size(width -25,height))
                    
        sizer.Add(self.comment, pos=(1,1),flag=wx.ALL, border=5)    
        pnl.SetSizer(sizer)
        self.SetSize((600 , 500))
        self.Centre()    

    def setComment(self,text):
        self.comment.SetValue(str(text))
    def setTitle(self,text):
        self.groupBox.SetLabel(text)
        