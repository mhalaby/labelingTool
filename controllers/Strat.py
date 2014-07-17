import wx
import math
import random
from itertools import groupby
from models.Review import reviews
from models.Project import projects

class Strat:
    def __init__(self):
        self.reviews = reviews()
        self.projects = projects()
        self.review_id = 0
        self.newSampleSize= 400
#------------------------------------------------------------------------------ 
        self.currentProject = self.projects.getProjects()[1].name 
        self.reviews = self.loadReviews()
        strat = self.calculateStrata(self.reviews,self.newSampleSize)        
        newSampleList = self.createNewSampleReviews(self.reviews,strat)
        
    def loadReviews(self):
        return self.reviews.getReviewsByProjectName(self.currentProject)
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
            
s = Strat()
