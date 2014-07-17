import peewee
from peewee import *
import BaseModel as baseModel
        
class labeledReview(baseModel.BaseModel):
    project_id = CharField()
    review_id = CharField()
    user_id = CharField()
    sentiment = IntegerField()
    bug_report = BooleanField()
    feature_request = BooleanField()
    feature_feedback = BooleanField()
    other = CharField()