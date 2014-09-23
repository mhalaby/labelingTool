__author__ = 'muhammad'
from models.LabeledReviews import labeledReview
from models.Project import projects
import math
from collections import defaultdict
import os
import copy
import  random
userIds = [10,13,21,22,24]
classes = ["feature_request","feature_feedback","feature_shortcoming","praise","complaint","usage_scenario","bug_report","noise"]

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
                if os.path.isfile('user_disagreed_evernote_reviews.txt'):
                    g = open('user_disagreed_evernote_reviews.txt', 'a')
                else:
                    g = open('user_disagreed_evernote_reviews.txt', 'w')

                g.write('user %s - %s \n' %(str(userId),str(idx)))
                for x,y in zip(sortedReviews1,sortedReviews2):
                    if getattr(x,className) != getattr(y,className):
                        disagreedr1.append(x)
                        disagreedr2.append(y)
                    else:
                        count +=1
                g.write("class: %s \n" % className)
                if len(disagreedr1) != 0:
                    rand = random.randint(0,len(disagreedr1)-1)
                    g.write("review %s:%s %s \n" % (disagreedr1[rand].user_id , disagreedr1[rand].review.title.encode('utf-8'),disagreedr1[rand].review.comment.encode('utf-8')))
                    g.write("value %s:  %s \n" % (disagreedr1[rand].user_id,getattr(disagreedr1[rand],className)))
                    g.write("value %s:  %s \n" % (disagreedr2[rand].user_id,getattr(disagreedr2[rand],className)))
                    g.write("\n")
                else:
                    g.write("No disagreement \n")
                g.close()
    #return  math.floor(float(count)*100/len(userReviewsList))
    return count

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
    return  userDict

def resolveMismatch(userId,dataDict):
    userReviewsList = dataDict[userId]
    resultData = []
    for idx in userIds:
         if idx != userId:
             r =  reivewsIntersection(userReviewsList,dataDict[idx])

def getDisagreedReviews(dataDict):
    pass
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
    data = preprocessDataPerProject(3)
    dict = createUserClassAggreementDict(data)
    printDict(dict)
   # print getattr(data[22][0],"feature_request")