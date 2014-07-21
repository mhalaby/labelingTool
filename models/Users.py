import peewee
from peewee import *
import BaseModel as baseModel
        
class User(baseModel.BaseModel):
    user_id = CharField(primary_key=True)
    password = CharField()
    username = CharField()
    authenticate = False
    def getAuthenticate(self):
        return self.authenticate
    
    def setAuthenticate(self):
        self.authenticate = True
               
    def getUserById(self,uid):
        rs = []
        for u in User.select().where(User.user_id == uid):
            rs.append(u)
        return rs[0]
    
    def getUserbyUsername(self,username):
        rs = []
        for u in User.select().where(User.username == username):
            rs.append(u)        
        if not rs :
            return rs            
        return rs[0]
    
