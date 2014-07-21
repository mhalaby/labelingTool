from controllers.Session import Session


class SessionManager():
    sessions=[]
    sessionKey = 0
    def createNewSession(self,user,controller):
        s = Session(self.sessionKey, user,controller) 
        self.sessionKey += 1
        self.sessions.append(s)
        
    def getSessionByUser(self,username):
        for s in self.sessions:
            if s.user.username == username:                
                return s
    #------------------------------------------ def removeSession(self,session):
        