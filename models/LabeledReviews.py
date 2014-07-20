import peewee
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
    
    def getLabeledReviews(self):
        labeledReview = []
        for l in self.select():
            labeledReview.append(l)
        return labeledReview
    
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
