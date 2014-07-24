from peewee import *
import BaseModel as baseModel
from models.Review import reviews

        
class labeledReview(baseModel.BaseModel):
    id = CharField(primary_key=True)
    review_id = IntegerField()
    review = ForeignKeyField(reviews)
    project_id = IntegerField()
    user_id = IntegerField()
    sentiment = IntegerField()
    bug_report = BooleanField()
    feature_request = BooleanField()
    feature_feedback = BooleanField()
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
        result = []        
        for l in labeledReview.select().join(reviews).where((labeledReview.user_id == userId) & (labeledReview.project_id == projectId)):
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
            return int(f.count)

    def getNumberOfLabeledReviewsByUserId(self, userId):        
        for f in labeledReview.select(fn.Count(labeledReview.id).alias('count')).join(reviews).where((labeledReview.user_id == userId)):
            return int(f.count)
        
