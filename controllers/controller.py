from flask import Flask
from models.Review import reviews
from models.Project import projects
#------------------------------------------- from views.MainView import mainView

app = Flask(__name__)


class Controller():
    def __init__(self):
        self.reviews = reviews()
        self.projects = projects()
        self.review_id = 0
        self.currentProject = self.projects.getProjects()[1].name
        self.rs = self.loadReviews()

    def loadReviews(self):
        return self.reviews.getReviewsByProjectName(self.currentProject)
    
    def setComment(self, reviews):
        self.view.setComment(reviews.comment)
    
    def setTitle(self, reviews):
        self.view.setTitle(reviews.title)
    
    def setProjectName(self):
        self.view.setProjectName(self.currentProject)    
    
    def setRatings(self):
        self.view.setRatings(reviews.stars)    
    
    def OnNext(self):
        self.review_id += 1        
    
    def OnPrev(self):
        if(self.review_id != 0):
            self.review_id -= 1
        #---------------------------------------------- self.updateView(self.rs)
    def getReivew(self):        
        return self.rs[self.review_id]

    def updateView(self, rs):
        rs = rs[self.review_id]
        self.setComment(rs)
        self.setTitle(rs)
        self.setProjectName()
        self.setRatings(rs)
        
#---------------------------------------------------- if __name__ == '__main__':
    #------------------------------------------------------- app = wx.App(False)
    #---------------------------------------------- controller = Controller(app)
    #------------------------------------------------------------ app.MainLoop()

