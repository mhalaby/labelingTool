import peewee
from peewee import *
import BaseModel as baseModel
        
class projects(baseModel.BaseModel):
    project_id = CharField(primary_key=True)
    name = CharField()
    def getProjects(self):
        projects = []
        for p in self.select():
            projects.append(p)
        return projects