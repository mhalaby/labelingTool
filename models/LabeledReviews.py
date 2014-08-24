from peewee import *
import BaseModel as baseModel
from models.Review import reviews
from sympy.core.trace import Tr

        
class labeledReview(baseModel.BaseModel):
    id = CharField(primary_key=True)
    review_id = IntegerField()
    review = ForeignKeyField(reviews)
    project_id = IntegerField()
    user_id = IntegerField()
    sentiment = IntegerField()
    bug_report = BooleanField()
    feature_request = BooleanField()
    feature_feedback = BooleanField() #feature strength    
    feature_shortcoming = BooleanField()
    usage_scenario = BooleanField()
    praise = BooleanField()
    complaint = BooleanField()
    noise = BooleanField()
    other = CharField()
    done = BooleanField()
    
    def getLabeledReviews(self):
        labeledReview = []
        for l in self.select():
            labeledReview.append(l)
        return labeledReview
    
    def doesUserExist(self, userId):
        result = []        
        for l in labeledReview.select().join(reviews).where((labeledReview.user_id == userId)):
            result.append(l)
        if len(result) > 0 :
            return True
        return False
    
    def getLabeledReviewsByUserId(self, userId, projectId):
        print userId, projectId
        result = []        
        for l in labeledReview.select().join(reviews).where((labeledReview.user_id == userId) & (labeledReview.project_id == projectId)):
            result.append(l)
        return result

    def getAllLabeledReviewsByUserId(self, userId):
        result = []        
        for l in labeledReview.select().join(reviews).where((labeledReview.user_id == userId)):
            result.append(l)
        return result
    
    def getLabeledReviewsByReviewId(self, userId, reviewId):
        result = []        
        for l in labeledReview.select().join(reviews).where((labeledReview.user_id == userId) & (labeledReview.review_id == reviewId)):
            result.append(l)
        return result    

    def getLastReviewByProjectId(self,userId,projectId):
        result = []                
        for l in labeledReview.select().where((labeledReview.user_id == userId) & (labeledReview.done == 1) & (labeledReview.project_id == projectId)):
            result.append(l)
        if not result:
            return None
        return result[len(result)-1]
        
    def getDoneReviews(self,userId):
        for f in labeledReview.select(fn.Count(labeledReview.id).alias('count')).where((labeledReview.user_id == userId) & (labeledReview.done == 1)):
            if f.count == '' or f.count == None:
                return 0 
            return int(f.count)

    def getDoneReviewByProject(self,userId,projectId):
        for f in labeledReview.select(fn.Count(labeledReview.id).alias('count')).where((labeledReview.user_id == userId) & (labeledReview.project_id == projectId) & (labeledReview.done == 1)):
            if f.count == '' or f.count == None:
                return 0
            return int(f.count)

    def getNumberOfLabeledReviewsByUserId(self, userId):        
        for f in labeledReview.select(fn.Count(labeledReview.id).alias('count')).join(reviews).where((labeledReview.user_id == userId)):
            return int(f.count)
    
    
    def __str__(self):
        return str(self.__dict__)
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
    
    def equals(self, other):
        if self.bug_report == other.bug_report and self.bug_report == True and other.bug_report == True:
            return True
        if self.feature_feedback == other.feature_feedback and self.feature_feedback == True and other.feature_feedback == True:
            return True
        if self.feature_request == other.feature_request and self.feature_request == True and other.feature_request == True:
            return True
        if self.feature_shortcoming == other.feature_shortcoming and self.feature_shortcoming == True and other.feature_shortcoming == True:
            return True
        if self.praise == other.praise and self.praise == True and other.praise == True:
            return True
        if self.complaint == other.complaint and self.complaint == True and other.complaint == True:
            return True
        if self.noise == other.noise and self.noise == True and other.noise == True:
            return True
        if self.usage_scenario == other.usage_scenario and self.usage_scenario == True and other.usage_scenario == True:
            return True
        if len(str(self.other)) > 1 and len(str(other.other)) > 1:
            return True
        return False