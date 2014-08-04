import math
import random
from itertools import groupby
from models.Review import reviews
from models.Project import projects
from itertools import repeat
from models.Users import User

class Strat:
    def __init__(self):
        self.review_id = 0
        self.newSampleSize= 30
        self.projects = projects()
#------------------------------------------------------------------------------ 
       
        
    def loadReviews(self,projectName):
        return self.reviews.getReviewsByProjectName(projectName)
#------------------------------------------------------------------------------ 
# returns an array of five items which contains the number
# sample based on each rating
    def calculateStrata(self, reviews,sampleSize):
        r1 = r2 = r3 = r4 = r5 = 0
        for r in reviews:
            if r.stars == 1:
                r1 += 1
            if r.stars == 2:
                r2 += 1
            if r.stars == 3:
                r3 += 1
            if r.stars == 4:
                r4 += 1
            if r.stars == 5:
                r5 += 1
        total = len(reviews)
        return [math.ceil(r1 * (float(sampleSize) / total)), 
                math.ceil (r2 * (float(sampleSize) / total)), 
                math.ceil (r3 * (float(sampleSize) / total)), 
                math.ceil (r4 * (float(sampleSize) / total)), 
                math.ceil (r5 * (float(sampleSize) / total))]
                      
    def createNewSampleReviews(self,reviews,strat):
        f = lambda x: x.stars
        gb = groupby(sorted(reviews, key=f), f)    
        i = 0
        l = [] 
        for key,group in gb:
            l.append(random.sample(list(group), int(strat[i])))
            i= i+1
        return l
                         
            
    def runStrat(self , projectId):
        self.reviews = reviews()
        currentProject = self.projects.getProjectNameById(projectId)
        print "Current Project ", currentProject
        self.reviews = self.loadReviews(currentProject)
        strat = self.calculateStrata(self.reviews,self.newSampleSize)     
        print "strat ", strat   
        self.newSampleList = self.createNewSampleReviews(self.reviews,strat)
        print "new sample size ", len(self.newSampleList[0]) +len(self.newSampleList[1])+len(self.newSampleList[2])+len(self.newSampleList[3])+len(self.newSampleList[4]) 
        return self.newSampleList
   # print Strat().aggregate(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p'],[1,2,3],6) 
    def aggregate(self,inputList,toBeAggregatedList,size):
        # create Lists based on the size of the the aggregated List
        aggregatedDict = {x:set([]) for x in toBeAggregatedList}
        duplicatedList = iter([x for item in inputList for x in repeat(item, 2)])
        
        indices = iter(toBeAggregatedList)
        index = indices.next()                    
        for i in range(0,size):  
            for y in toBeAggregatedList:
                aggregatedDict[y].add(duplicatedList.next()) 
        if not (size % 2 == 0) and not (len(toBeAggregatedList) % 2 == 0):
            aggregatedDict[index].add(duplicatedList.next())
        return aggregatedDict
    
    def runStratPerProject(self,users,projectId):
        self.reviews = reviews()
        currentProject = self.projects.getProjectNameById(projectId)
        self.reviews = self.loadReviews(currentProject)
        strat = self.calculateStrata(self.reviews,self.newSampleSize) 
        usersIdList = [x.user_id for x in users]  
        usersDict = {x.user_id:[] for x in users}
        print "strat ", strat
        #list of differences where we need to get more data based on the number of users
        newStrat = [math.ceil(((len(users) * s)/2))   for s in strat]
        print "difference = ", newStrat
        self.newSampleList = self.createNewSampleReviews(self.reviews,newStrat)
        print "new sample size ", len(self.newSampleList[0]) +len(self.newSampleList[1])+len(self.newSampleList[2])+len(self.newSampleList[3])+len(self.newSampleList[4])
        i = 0
        for s in self.newSampleList:
            aggregated = self.aggregate(s, usersIdList, int(strat[i]))            
            for userId in usersDict:
                usersDict[userId].append(list(aggregated[userId]))
            i +=1
        return usersDict
    
    def printHelper(self,usersDict):
        for i in usersDict:
            print "user id ",i
            rating = 1
            for x in usersDict[i]:
                print "rating ", rating
                rs = []
                for r in x:
                    rs.append(int(r.review_id))
                print "review ", rs
                rating += 1    

#--- users = [User().getUserById(1),User().getUserById(4),User().getUserById(2)]
#---------------------- Strat().printHelper(Strat().runStratPerProject(users,1))
# print Strat().aggregate(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p'],[1,2,3],6)