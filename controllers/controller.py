import wx
from models.Review import reviews
from models.Project import projects
from views.MainView import mainView

class Controller:
    def __init__(self, app):
        self.reviews = reviews()
        self.projects = projects()
#------------------------------------------------------------------------------ 
        self.currentProject = self.projects.getProjects()[1].name
#------------------------------------------------------------------------------ 
        self.view = mainView(None)
        rs = self.loadReviews()
        self.setComment(rs)
        self.setTitle(rs)
        self.setProjectName()
        self.setRatings(rs)
        self.view.Show()

    def loadReviews(self):
        return self.reviews.getReviewsByProjectName(self.currentProject)[0]
    
    def setComment(self,reviews):
        self.view.setComment(reviews.comment)
    def setTitle(self,reviews):
        self.view.setTitle(reviews.title)
    def setProjectName(self):
        self.view.setProjectName(self.currentProject)    
    def setRatings(self,reviews):
        self.view.setRatings(reviews.stars)    
        
if __name__ == '__main__':
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()