import peewee
from peewee import *
from models.BaseModel import BaseModel
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
        try:
         # do your database stuff
            rs = []
            for u in User.select().where(User.user_id == uid):
                rs.append(u)
            return rs[0]
        except:
            BaseModel()._connect()
            self.getUserById(uid)
    
    def getUserbyUsername(self,username):
        try:
         # do your database stuff
            rs = []
            for u in User.select().where(User.username == username):
                rs.append(u)        
            if not rs :
                return rs            
            return rs[0]
        except:
            BaseModel()._connect()
            self.getUserbyUsername(username)
