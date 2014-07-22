from models.Review import reviews
from models.Project import projects
from models.BaseModel import BaseModel
from itertools import cycle

from models.LabeledReviews import labeledReview
from controllers.Strat import Strat

class Controller():

    def __init__(self):
        self.reviews = labeledReview()
        self.projects = projects()
        self.review_id = 0
        self.userId = 0
        self.projectId = 0 
        
    def init(self):        
        try:
            if not self.reviews.doesUserExist(self.getUserId()):
                self.runStrat()
            self.projectsList = self.getProjects()
            self.currentProject = self.projects.getProjects()[self.projectId].name
            self.rs = self.reviews.getLabeledReviewsByUserId(self.getUserId(), self.projects.getProjectIdByName(self.currentProject))
            self.setLastReviewIndex( self.projects.getProjects()[self.projectId].project_id)
        except:
            BaseModel()._connect()
            print "init ERROR reconnecting"
            self.init()
            
    def setUserId(self, userId):
        self.userId = userId
   
    def getUserId(self):
        return self.userId
    
    def onNext(self):
        print "ON NEXT",self.review_id,len(self.rs) - 1
        if self.review_id < len(self.rs) - 1:
            self.review_id += 1                    
            
    def onPrev(self):
        if(self.review_id != 0):
            self.review_id -= 1
                  
    def getReivew(self):                       
        return self.rs[self.review_id]
           
    def getProjects(self):
        try:            
            return self.projects.getProjects()      
        except:             
            BaseModel()._connect()
            print "getProjects ERROR reconnecting..."
            self.getProjects()
    
    def getCurrentProject(self):
        return self.currentProject
    
    def getCurrentProjectId(self):
        return self.projects.getProjectIdByName(self.getCurrentProject())
    
    def setCurrentProject(self, currentProjectName):
        try:
            self.currentProject = currentProjectName
            projectId= self.projects.getProjectIdByName(currentProjectName)
            self.rs = self.reviews.getLabeledReviewsByUserId(self.userId, projectId)            
            self.setLastReviewIndex(projectId)  
            print "review index", self.review_id,"Project id", projectId        
            
        except:
            BaseModel()._connect()
            print "ERROR setCurrentProject reconnecting..."
            self.setCurrentProject(currentProjectName)       
                 
    def saveLabeledReview(self): 
        try:
            print 'savelabel', self.rs[self.review_id].user_id , "user id", self.userId, self.rs[self.review_id].review_id
            self.rs[self.review_id].save()
        except:
            BaseModel()._connect()
            print "ERROR while saving reconnecting..."
            self.saveLabeledReview()

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

    def setDone(self):
        self.rs[self.review_id].done = True
     
    def setLastReviewIndex(self,projectId): 
        self.lastReviewForCurrentProject = self.reviews.getLastReviewByProjectId(self.getUserId(), projectId)
        print 'last review ', self.lastReviewForCurrentProject.review_id, 'project id ', projectId
        if self.lastReviewForCurrentProject is None:
            self.review_id = 0
        else:           
            self.review_id = self.getLastReviewIndex(self.lastReviewForCurrentProject)
            if self.review_id < len(self.rs) - 1:
                self.review_id += 1
            print 'last ', self.review_id, "length ", len(self.rs)
            
    def getLastReviewIndex(self,lastElement):        
        return [x.review_id for x in self.rs].index(lastElement.review_id)
        
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
                    l.bug_report = 0
                    l.feature_feedback = 0
                    l.feature_request = 0
                    l.sentiment = -1
                    l.other = ""                
                    l.project_id = i
                    l.review_id = review.review_id
                    l.user_id = self.getUserId()
                    l.save()

    def getNextProject(self, currentProject): 
        projectsIteratable = cycle(self.projectsList)
        print currentProject      
        for p in projectsIteratable:
            if p.name == currentProject:
                return projectsIteratable.next().name
            projectsIteratable.next()
            
    def getPrevProject(self, currentProject):     
        temp = self.projectsList[len(self.projectsList) - 1].name
        for p in self.projectsList:
            if p.name == currentProject:
                return temp 
            temp = p.name
            
