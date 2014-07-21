from models.Users import User
from controllers.controller import Controller
class Session():
    sessionkey = 0
    user = User()
    c = Controller()
    
    def __init__(self,key,u,c):
        self.sessionkey = key
        self.user = u
        self.c = c
    def getSessionKey(self):
        return self.sessionkey
    def getSessionUser(self):
        return self.user
    def getSessionController(self):
        return self.c
        