from models.Review import reviews
from models.Project import projects
from models.BaseModel import BaseModel
import nltk.data
from models.LabeledReviews import labeledReview
from controllers.Strat import Strat

class Controller():

    def __init__(self):
        self.reviews = labeledReview()
        self.projects = projects()
        self.review_idx = 0
        self.userId = 0
        ####### when launching this value will be 0
        self.projectId = 1
        self.numberOfDoneReviews = 0
        self.numberOfOverallReviews = 0
        self.numberOfDoneReviewsPerProject = 0
    def CreateController(self):
        try:               
            self.projectsList = self.getProjects()
            self.currentProject = self.projects.getProjects()[self.projectId].name
            print "current project ",self.currentProject
            self.rs = self.reviews.getLabeledReviewsByUserId(self.getUserId(), self.projects.getProjectIdByName(self.currentProject))
            #self.runTestSample()
            self.setLastReviewIndex( self.projects.getProjects()[self.projectId].project_id)
            self.numberOfDoneReviews =  self.reviews.getDoneReviews(self.getUserId())
            self.numberOfOverallReviews = self.reviews.getNumberOfLabeledReviewsByUserId(self.getUserId())
            self.numberOfDoneReviewsPerProject = self.reviews.getDoneReviewByProject(self.getUserId(),self.projects.getProjects()[self.projectId].project_id)
        except Exception as e:
            BaseModel()._connect()
            print "init ERROR reconnecting, ", e
            self.CreateController()

    def setUserId(self, userId):
        self.userId = userId

    def getUserId(self):
        return self.userId

    def onNext(self):
        print "On next current review index = ", self.review_idx
        if self.review_idx < len(self.rs) - 1:
            self.review_idx += 1
            print "On next review index = ", self.review_idx

    def goTo(self,review_idx):
        print "On goto current review index = ", self.review_idx
        self.review_idx = int(review_idx)
        print "On goto review index = ", self.review_idx

    def onPrev(self):
        print "On prev current review index = ", self.review_idx
        if(self.review_idx != 0):
            self.review_idx -= 1
            print "On prev review index = ", self.review_idx

    def getReivew(self):        
        print "get current review =",self.rs[self.review_idx].review_id
        print "get current labeled review id = ",self.rs[self.review_idx].id
        print "current labeled review values bug = ", self.rs[self.review_idx].bug_report, " fr = ", self.rs[self.review_idx].feature_request, " ff = ",  self.rs[self.review_idx].feature_feedback, " fs = ",  self.rs[self.review_idx].feature_shortcoming, " pr = ",  self.rs[self.review_idx].praise, " co = ", self.rs[self.review_idx].complaint, " noise = ", self.rs[self.review_idx].noise, " other = ",  self.rs[self.review_idx].other, " sentiment = ", self.rs[self.review_idx].sentiment
        return self.rs[self.review_idx]

    def getProjects(self):
        try:
            return self.projects.getProjects()
        except Exception as e:
            BaseModel()._connect()
            print "getProjects ERROR reconnecting...", e
            return self.projects.getProjects()

    def getCurrentProject(self):
        return self.currentProject

    def getCurrentProjectId(self):
        return self.projects.getProjectIdByName(self.getCurrentProject())

    def getNumberOfReviewsPerProject(self):
        return len(self.rs) - 1

    def getNumberOfDoneReviewsPerProject(self):
        return self.numberOfDoneReviewsPerProject

    def setCurrentProject(self, currentProjectName):
        try:
            self.currentProject = currentProjectName
            projectId= self.projects.getProjectIdByName(currentProjectName)
            self.numberOfDoneReviewsPerProject = self.reviews.getDoneReviewByProject(self.getUserId(),projectId)
            self.rs = self.reviews.getLabeledReviewsByUserId(self.userId, projectId)
            self.setLastReviewIndex(projectId)
            print "review index", self.review_idx,"Project id", projectId

        except:
            BaseModel()._connect()
            print "ERROR setCurrentProject reconnecting..."
            self.setCurrentProject(currentProjectName)

    def saveLabeledReview(self):
        try:
            print 'saving into db for user ', self.rs[self.review_idx].user_id ," and review id", self.rs[self.review_idx].review_id," current review index ",self.review_idx
            self.rs[self.review_idx].save()
            self.numberOfDoneReviewsPerProject = self.reviews.getDoneReviewByProject(self.getUserId(),self.getCurrentProjectId())
        except:
            BaseModel()._connect()
            print "ERROR while saving reconnecting..."
            self.saveLabeledReview()

    def setBugReport(self, val):
        self.rs[self.review_idx].bug_report = val

    def setSentiment(self, val):
        self.rs[self.review_idx].sentiment = val

    def setFeatureRequest(self, val):
        self.rs[self.review_idx].feature_request = val

    def setFeatureShortcoming(self, val):
        self.rs[self.review_idx].feature_shortcoming = val

    def setPraise(self, val):
        self.rs[self.review_idx].praise = val
        
    def setComplaint(self, val):
        self.rs[self.review_idx].complaint = val
        
    def setNoise(self, val):
        self.rs[self.review_idx].noise = val

    def setUsageScenario(self, val):
        self.rs[self.review_idx].usage_scenario = val

    def setFeatureFeedback(self, val):
        self.rs[self.review_idx].feature_feedback = val

    def setOther(self, val):
        self.rs[self.review_idx].other = val

    def setReview(self, review):
        self.rs = review

    def setDone(self):
        self.rs[self.review_idx].done = True

    def setLastReviewIndex(self,projectId):
        self.lastReviewForCurrentProject = self.reviews.getLastReviewByProjectId(self.getUserId(), projectId)
        if self.lastReviewForCurrentProject is None:
            self.review_idx = 0
        else:
            self.review_idx = self.getLastReviewIndex(self.lastReviewForCurrentProject)
            if self.review_idx < len(self.rs) - 1:
                self.review_idx += 1

    def getLastReviewIndex(self,lastElement):        
        return [int(x.review.review_id) for x in self.rs].index(int(lastElement.review.review_id))

    def getReviewId(self):
        return self.review_idx
    
    def getNumberOfDoneReviews(self):
        return self.numberOfDoneReviews
    
    def setNumberOfDoneReviews(self):
        try:
            self.numberOfDoneReviews = self.reviews.getDoneReviews(self.getUserId())
            print "numberOfDoneReviews ", self.numberOfDoneReviews
        except Exception as e:
            BaseModel()._connect()
            print "setNumberOfDoneReviews ERROR reconnecting, ", e
            self.setNumberOfDoneReviews()

    def getNumberOfOverallReviews(self):
        return self.numberOfOverallReviews
    
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
                    l.feature_shortcoming = 0
                    l.praise= 0
                    l.complaint= 0
                    l.usage_scenario = 0                
                    l.sentiment = -1
                    l.other = ""
                    l.project_id = i
                    l.review_id = review.review_id
                    l.user_id = 10
                    l.save()

    def runTestSample(self):
        tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
        s = Strat()
        projectId = 2
        i=0
        counter  = 1000000        
        result = s.runStrat(projectId)
        for rating in range(0, 5):
            reviews_per_rating = result[rating]
            for review in reviews_per_rating:
                l = labeledReview()                
                l.bug_report = 0
                l.feature_feedback = 0
                l.feature_request = 0
                l.feature_shortcoming = 0
                l.praise= 0
                l.complaint= 0
                l.usage_scenario = 0                
                l.sentiment = -1
                l.other = ""
                l.noise= 0
                l.project_id = 2
                l.user_id = 11
                l.review_id = review.review_id
                print l.review_id, i 
                i +=1
                l.save()
                allText =  review.title + ". "+review.comment  
                list = tokenizer.tokenize(allText.strip())             
                for text in list:
                    l = labeledReview()
                    r= reviews()
                    r.comment= text
                    r.title=""
                    r.stars = rating + 1
                    r.project_id = 2
                    r.review_id = counter
                    l.review_id = r.review_id
                    r.save(force_insert=True)
                    l.bug_report = 0
                    l.feature_feedback = 0
                    l.feature_request = 0
                    l.feature_shortcoming = 0
                    l.praise= 0
                    l.complaint= 0
                    l.usage_scenario = 0                
                    l.sentiment = -1
                    l.other = ""
                    l.noise= 0
                    l.project_id = 2
                    counter +=1
                    l.user_id = 10
                    l.save()
                    print review.review_id, text

