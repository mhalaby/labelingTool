import wx
from models.Review import reviews
from models.Project import projects
from views.MainView import mainView

class Controller:
    def __init__(self, app):
        self.reviews = reviews()
        self.projects = projects()
        self.view = mainView(None)
        rs = self.loadReviews()
        self.setComment(rs)
        self.setTitle(rs)
        self.view.Show()

    def loadReviews(self):
        r = reviews()
        p = projects()
        return r.getReviewsByProjectName(p.getProjects()[0].name)[0]
    
    def setComment(self,reviews):
        self.view.setComment(reviews.comment)
    def setTitle(self,reviews):
        self.view.setTitle(reviews.title)
if __name__ == '__main__':
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()