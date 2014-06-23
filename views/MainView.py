import wx 
  
class mainView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View") 
        pnl = wx.Panel(self)
        width = 400
        height = 250
        
        self.projectName = wx.StaticText(pnl,pos=(10, 5))        
        self.groupBox = wx.StaticBox(pnl, label="feedback", pos=(4, 30), size=(width, height + 40))
        staticBoxSizer = wx.StaticBoxSizer(self.groupBox,orient = wx.VERTICAL)
        self.comment = wx.TextCtrl(pnl,style=wx.TE_READONLY| wx.TE_MULTILINE,pos=(14,50) ,size = wx.Size(width -25,height))
        staticBoxSizer.Add(self.comment)
        
        self.ratings = wx.StaticText(pnl,pos=(10, height+75))        

        self.SetSize((600 , 500))
        self.Centre()    

    def setComment(self,text):
        self.comment.SetValue(str(text))
    def setTitle(self,text):
        self.groupBox.SetLabel(text)
    def setProjectName(self,text):
        self.projectName.SetLabel("App: "+text)
    def setRatings(self,text):
        self.ratings.SetLabel("Stars: "+str(text))
        