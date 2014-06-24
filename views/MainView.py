import wx 
  
class mainView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main View") 
        pnl = wx.Panel(self)
        width = 400
        height = 250        
        wx.Button(pnl, id=1, label='Next', pos=(width + 40, 35))
        wx.Button(pnl, id=2, label='Prev', pos=(width + 40, 70))
#-----------------Radio Buttons--------------------------------------------------------- 
        labelBox = wx.StaticBox(pnl, label="Label", pos=(width+25, 110), size=(180, height-40))
        self.bug_rb = wx.RadioButton(pnl, label='Bug Report', pos=(width+40, 135),style=wx.RB_GROUP)
        self.feature_rb = wx.RadioButton(pnl, label='Feature Request', pos=(width+40, 170))
        self.feedback_rb = wx.RadioButton(pnl, label='Feature Feedback', pos=(width+40, 205))
        self.other_rb = wx.RadioButton(pnl, label='Other', pos=(width+40, 240))
        self.other_label = wx.TextCtrl(pnl,style= wx.TE_MULTILINE,pos=(width+40,265) ,size = wx.Size(150,40))

        self.projectName = wx.StaticText(pnl,pos=(10, 5))        
        self.groupBox = wx.StaticBox(pnl, label="feedback", pos=(4, 30), size=(width, height + 40))
        staticBoxSizer = wx.StaticBoxSizer(self.groupBox,orient = wx.VERTICAL)
        self.comment = wx.TextCtrl(pnl,style=wx.TE_READONLY| wx.TE_MULTILINE,pos=(14,50) ,size = wx.Size(width -25,height))
        staticBoxSizer.Add(self.comment)

        self.ratings = wx.StaticText(pnl,pos=(10, height+75))        

        self.SetSize((630 , 400))
        self.Centre()    

    def setComment(self,text):
        self.comment.SetValue(str(text))
    def setTitle(self,text):
        self.groupBox.SetLabel(text)
    def setProjectName(self,text):
        self.projectName.SetLabel("App: "+text)
    def setRatings(self,text):
        self.ratings.SetLabel("Stars: "+str(text))

        
        