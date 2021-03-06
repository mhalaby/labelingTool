import peewee
from peewee import *
import BaseModel as baseModel
from models.Project import projects
        
class reviews(baseModel.BaseModel):
    review_id = CharField(primary_key=True)
    title = CharField()
    stars = IntegerField()
    comment = TextField()
    project = ForeignKeyField(projects)
    
    def getReviewsByProjectName(self, name):
        reviews = []
        for review in self.select().join(projects).where(projects.name == name):
            reviews.append(review)
        return reviews
    def getReivewById(self,r_id):
        rs = []
        for review in reviews.select().where(reviews.review_id == r_id):
            rs.append(review)
        return rs[0]
    def __getitem__(self,key):
        return self



