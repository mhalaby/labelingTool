__author__ = 'muhammad'
from models.LabeledReviews import labeledReview
from models.Project import projects
import math
from collections import defaultdict
import os
from tools.disagreedClass import disagreedClass
import copy
import  random
userIds = [10,13,21,22,24]
classes = ["feature_request","feature_feedback","feature_shortcoming","praise","complaint","usage_scenario","bug_report","noise"]
counter =  {'count':0}
def preprocessDataPerProject(project_id):
    dataDict = defaultdict()
    #projectsArray = [int(p.project_id) for p in projects().getProjects()]
    for idx in userIds:
        dataDict[idx]= labeledReview().getLabeledReviewsByUserId(idx,project_id)
    return dataDict

def calculateAggreementperClass(className,userId,dataDict):
    userReviewsList = dataDict[userId]
    count = 0
    for idx in userIds:
        if idx != userId:
            r1,r2 = reivewsIntersection(userReviewsList,dataDict[idx])
            if len(r1) != 0:
                sortedReviews1  = sorted(r1,key = lambda r:r.review_id)
                sortedReviews2  = sorted(r2,key = lambda r:r.review_id)
                disagreedr1 = []
                disagreedr2 = []
                for x,y in zip(sortedReviews1,sortedReviews2):
                    if getattr(x,className) != getattr(y,className):
                        ## check if contains two problematic coders
                        disagreedr1.append(x)
                        disagreedr2.append(y)
                    else:
                        count +=1

    return  math.floor(float(count)*100/len(userReviewsList))
    #return count

def reivewsIntersection(reviews1, reviews2):
    ids_l1 = set(x.review_id for x in reviews1)  # All ids in list 1
    ids_l2 = set(x.review_id for x in reviews2)  # All ids in list 1
    intersection = ids_l1.intersection(ids_l2)
    r1 = [r for r in reviews1 if r.review_id in intersection]
    r2 = [r for r in reviews2 if r.review_id in intersection]
    return r1,r2

def createUserClassAggreementDict(data):
    userDict= defaultdict()
    for idx in userIds:
        userDict[idx] = {}
        for c in classes:
            userDict[idx][c]= calculateAggreementperClass(c,idx,data)
        disagreementProcess(idx,data)
    return userDict

def disagreementProcess(userId,dataDict):
    userReviewsList = dataDict[userId]
    for idx in userIds:
        if idx != userId and userId < idx:
            r1,r2 = reivewsIntersection(userReviewsList,dataDict[idx])
            if len(r1) != 0:
                sortedReviews1  = sorted(r1,key = lambda r:r.review_id)
                sortedReviews2  = sorted(r2,key = lambda r:r.review_id)
                for x,y in zip(sortedReviews1,sortedReviews2):
                    newLabelledReview = labeledReview()
                    print "user " , x.user_id,"and" , y.user_id , "review ", x.review_id, "and", y.review_id

                    for className in classes:
                        print className, "x", getattr(x,className), "y", getattr(y,className)
                        if getattr(x,className) != getattr(y,className):
                            classVal = resolveDisagreement(className,x,y)
                            counter["count"] += 1
                        else:
                            classVal = getattr(x,className)
                        setattr(newLabelledReview,className,classVal)
                        print "final class val:" ,classVal
                        print "-----------------------------"
                    newLabelledReview.review_id = x.review_id
                    newLabelledReview.user_id = 100
                    newLabelledReview.project_id = x.project_id
                    # newLabelledReview.save()

def resolveDisagreement(className,reviews1,reviews2):
    disagreedKlass = disagreedClass()
    #check for problematic users
    #if only one of them
    if int(reviews1.user_id) in getattr(disagreedKlass,className) and int(reviews2.user_id) in getattr(disagreedKlass,className):
        user1Mistakes = getattr(disagreedKlass,className)[int(reviews1.user_id)]
        user2Mistakes = getattr(disagreedKlass,className)[int(reviews2.user_id)]
        print " Both of them are problematic"
        if user1Mistakes == user2Mistakes:
            print "get Dominant Class "
            if getDominantClassValue(className) != -1:
                return getDominantClassValue(className)
            else:
                print "ambiguous case"
                return False

        if user1Mistakes > user2Mistakes:
            return getattr(reviews2,className)
        else:
            return getattr(reviews1,className)
    else:
        if int(reviews1.user_id) in getattr(disagreedKlass,className):
            print reviews1.user_id, "only "
            return getattr(reviews2,className)
        if int(reviews2.user_id) in getattr(disagreedKlass,className):
            print reviews2.user_id, " only "
            return getattr(reviews1,className)
        if getDominantClassValue(className) != -1:
            print "get Dominant Class "
            return getDominantClassValue(className)
        else:
            print "ambiguous case"
            return False

def getDominantClassValue(className):
    dominantClasses = {"feature_feedback":False,"feature_shortcoming":False,"complaint":False,"usage_scenario":True,"bug_report":True}
    if className in dominantClasses:
        return  dominantClasses[className]
    else:
        return -1

def printDict(dict):
    z=0
    for x in dict:
        print "---------------------"
        print "user", x
        for y in dict[x]:
            #if y =="noise":
            print y, ":",dict[x][y]
            z += dict[x][y]

        # print z
##What should we do when there is a mismatch
if __name__=="__main__":
    projects = [1,2,3,5,6,7,8]

    for p in projects:
        print "project ",p
        data = preprocessDataPerProject(p)
        dict = createUserClassAggreementDict(data)
        printDict(dict)
        print "----------------------------------------------------------------------------------------------------------------"
    print "disagreement counter", counter['count']
   # print getattr(data[22][0],"feature_request")