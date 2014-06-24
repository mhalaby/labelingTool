import wx
from models.Review import reviews
from models.Project import projects
from views.MainView import mainView
class Controller:
    def __init__(self, app):
        self.reviews = reviews()
        self.projects = projects()
        self.review_id = 0
#------------------------------------------------------------------------------ 
        self.currentProject = self.projects.getProjects()[1].name
#------------------------------------------------------------------------------ 
        self.view = mainView(None)
        self.rs = self.loadReviews()
        self.updateView(self.rs)
        self.view.Bind(wx.EVT_BUTTON, self.OnNext, id=1)
        self.view.Bind(wx.EVT_BUTTON, self.OnPrev, id=2)

        self.view.Show()

    def loadReviews(self):
        return self.reviews.getReviewsByProjectName(self.currentProject)
    
    def setComment(self,reviews):
        self.view.setComment(reviews.comment)
    def setTitle(self,reviews):
        self.view.setTitle(reviews.title)
    def setProjectName(self):
        self.view.setProjectName(self.currentProject)    
    def setRatings(self,reviews):
        self.view.setRatings(reviews.stars)    
    def OnNext(self, e):
        self.review_id += 1
        self.updateView(self.rs)
    def OnPrev(self, e):
        if(self.review_id != 0):
            self.review_id -= 1
        self.updateView(self.rs)    
    def updateView(self,rs):
        rs = rs[self.review_id]
        self.setComment(rs)
        self.setTitle(rs)
        self.setProjectName()
        self.setRatings(rs)
if __name__ == '__main__':
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()