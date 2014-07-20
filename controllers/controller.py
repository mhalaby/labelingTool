from flask import Flask
from models.Review import reviews
from models.Project import projects
from models.LabeledReviews import labeledReview
from controllers.Strat import Strat

app = Flask(__name__)


class Controller():
    def __init__(self):
        self.reviews = labeledReview()
        self.projects = projects()
        self.userId = 1
        self.review_id = 0
        self.currentProject = self.projects.getProjects()[0].name
        self.rs = self.reviews.getLabeledReviewsByUserId(self.userId, self.projects.getProjectIdByName(self.currentProject))
   
    def OnNext(self):
        self.review_id += 1 
    
    def OnPrev(self):
        if(self.review_id != 0):
            self.review_id -= 1

    def getReivew(self):        
        print self.rs[self.review_id].review.review_id
        return self.rs[self.review_id]    
           
    def getProjects(self):
        return self.projects.getProjects()
    
    def getCurrentProject(self):
        return self.currentProject
    
    def setCurrentProject(self, currentProjectName):
        self.currentProject = currentProjectName
        self.review_id = 0
        self.rs = self.reviews.getLabeledReviewsByUserId(self.userId, self.projects.getProjectIdByName(currentProjectName))
        
    def saveLabeledReview(self):        
        self.rs[self.review_id].save()
        
    def setBugReport(self, val):
        self.rs[self.review_id].bug_report = val
        
    def setSentiment(self, val):
        self.rs[self.review_id].sentiment = val
        
    def setFeatureRequest(self, val):
        self.rs[self.review_id].feature_request = val
        
    def setFeatureFeedback(self, val):
        self.rs[self.review_id].feature_feedback = val
        
    def setOther(self, val):
        self.rs[self.review_id].other = val
        
    def setReview(self, review):
        self.rs = review
        
    def runStrat(self):
        s = Strat()
        allProjects = self.getProjects()
        for p in allProjects:
            i = p.project_id
            print i
            result = s.runStrat(int(i))
            for rating in range(0, 5):
                reviews_per_rating = result[rating]                
                for review in reviews_per_rating:
                    l = labeledReview()
                    l.project_id = i
                    l.review_id = review.review_id
                    l.user_id = 1
                    l.save()
            
#---------------------------------------------------- if __name__ == '__main__':
    #------------------------------------------------------- app = wx.App(False)
    #---------------------------------------------- controller = Controller(app)
    #------------------------------------------------------------ app.MainLoop()

