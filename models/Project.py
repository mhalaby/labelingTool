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
    def getProjectNameById(self,id):
        result = []
        for p in projects.select().where(projects.project_id == id):
            result.append(p)
        return result[0].name
    def getProjectIdByName(self,name):
        result = []
        for p in projects.select().where(projects.name == name):
            result.append(p)
        return result[0].project_id
