# Date: 15/08/2014
from models.LabeledReviews import labeledReview
import math

user1Id = 12
user2Id = 10
reviews1 = labeledReview().getAllLabeledReviewsByUserId(user1Id)
reviews2 = labeledReview().getAllLabeledReviewsByUserId(user2Id)
count = 0
for r1, r2 in zip(reviews1, reviews2):
    r2.user_id = 0
    r1.user_id = 0
    r1.id = 0
    r2.id = 0
    if r1.noise:
        r1.sentiment = -1
    if r2.noise:
        r2.sentiment = -1
    if len(r1.other) > 1:
        r1.other = 1
    if len(r2.other) > 1:
        r2.other = 1
    if r1 == r2:
        count += 1

print "Total number of reviews ", len(reviews1)
print "number of agreement ", count
print "percentage ", round((float(count) / float(len(reviews1))) * 100, 2)
print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"


def checkMultiLabel():
    count = 0
    mcount = 0
    bugCount = 0
    strengthCount = 0
    shortcomingCount = 0
    requestCount = 0
    praiseCount = 0
    complaintCount = 0
    noiseCount = 0
    otherCount = 0
    re1 = labeledReview().getAllLabeledReviewsByUserId(user1Id)
    re2 = labeledReview().getAllLabeledReviewsByUserId(user2Id)
    for r1, r2 in zip(re1, re2):
        r2.user_id = 0
        r1.user_id = 0
        r1.id = 0
        r2.id = 0
        # ignore sentiment
        r1.sentiment = 1
        r2.sentiment = 1
        if r2.usage_scenario:
            print r2.review.comment
        if r1.noise:
            r1.sentiment = -1
        if r2.noise:
            r2.sentiment = -1
        if len(r1.other) > 1:
            r1.other = 1
        if len(str(r2.other)) > 1:
            r2.other = 1
        if r1 == r2:
            count += 1
            if r1.bug_report:
                bugCount +=1
            if r1.feature_feedback:
                strengthCount +=1
            if r1.feature_shortcoming:
                shortcomingCount +=1
            if r1.feature_request:
                requestCount +=1
            if r1.praise:
                praiseCount +=1
            if r1.complaint:
                complaintCount +=1
            if r1.noise:
                noiseCount +=1
            if r1.other == 1:
                otherCount +=1
        else:
            if r1.equals(r2):
                mcount += 1
            if r1.bug_report or r2.bug_report :
                bugCount +=1
            if r1.feature_feedback or r2.feature_feedback:
                strengthCount +=1
            if r1.feature_shortcoming or r2.feature_shortcoming:
                shortcomingCount +=1
            if r1.feature_request or r2.feature_request:
                requestCount +=1
            if r1.praise or r2.praise:
                praiseCount +=1
            if r1.complaint or r2.complaint:
                complaintCount +=1
            if r1.noise or r2.noise:
                noiseCount +=1
            if r1.other == 1 or r2.other == 1:
                otherCount +=1

                #--------------------------------------- print r2.review.comment
                #---------- print "complaint", r1.complaint, " # ", r2.complaint
                # print "fshort ", r1.feature_shortcoming, " # ", r2.feature_shortcoming
                #------ print "bug report ", r1.bug_report, " # ", r2.bug_report
                # print "frequest ", r1.feature_request, " # ", r2.feature_request
                # print "fstrength ", r1.feature_feedback, " # ", r2.feature_feedback
                #------------------ print "praise ", r1.praise, " # ", r2.praisemm
                #--------------------- print "noise ", r1.noise, " # ", r2.noise
                # print "-----------------------------------------------------"
    print "bugCount " ,bugCount
    print "strengthCount " ,strengthCount
    print "shortcomingCount " ,shortcomingCount
    print "requestCount " ,requestCount
    print "praiseCount " ,praiseCount
    print "complaintCount " ,complaintCount
    print "otherCount " ,otherCount
    print "number of agreement without sentiment", count
    print "number of partial agreement without sentiment", mcount
    print "percentage ", round((float(count) / float(len(re1))) * 100, 2)
    print "percentage with partial agreement", round((float(count + mcount) / float(len(re1))) * 100, 2)


def checkSentimentAgreement():
    count = 0
    mcount = 0
    re1 = labeledReview().getAllLabeledReviewsByUserId(user1Id)
    re2 = labeledReview().getAllLabeledReviewsByUserId(user2Id)
    for r1, r2 in zip(re1, re2):
        if r1.noise:
            r1.sentiment = -1
        if r2.noise:
            r2.sentiment = -1
        if r1.sentiment == r2.sentiment:
            count += 1
        else:
            if (r1.sentiment == 1 and r2.sentiment == 2) or (r2.sentiment == 1 and r1.sentiment == 2):
                mcount += 1
            if (r1.sentiment == 4 and r2.sentiment == 5) or (r2.sentiment == 4 and r1.sentiment == 5):
                mcount += 1
    print "number of sentiment agreement ", count
    print "number of sentiment partial agreement ", mcount
    print "percentage ", round((float(count) / float(len(re1))) * 100, 2)
    print "percentage with partial agreement", round((float(count + mcount) / float(len(re1))) * 100, 2)


checkMultiLabel()
print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
checkSentimentAgreement()
print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"




# ----------------------------------------------------------- def convertVals(x):
#----------------------------------------------------- if isinstance(x,int):
#--------------------------------------------------------- return int(x)
#---------------------------------------- if x =="" or x== " " or x is None:
#-------------------------------------------------------------- return 0
#----------------------------------------------------------- if x.isalpha():
#-------------------------------------------------------------- return 1
#------------------------------------------------------------- return int(x)
# mat1 = [[convertVals(x) for x in r.__dict__["_data"].values()] for r in reviews1]
# mat2 = [[convertVals(x) for x in r.__dict__["_data"].values()] for r in reviews2]
#---------------------------------------------- print "array of values 1 ", mat1
#---------------------------------------------- print "array of values 2 ", mat2

#print "kappa == ", computeKapp

DEBUG = True


def computeKappa(mat):
    """ Computes the Kappa value
        @param n Number of rating per subjects (number of human raters)
        @param mat Matrix[subjects][categories]
        @return The Kappa value """
    n = checkEachLineCount(mat)  # PRE : every line count must be equal to n
    N = len(mat)
    k = len(mat[0])

    if DEBUG:
        print n, "raters."
        print N, "subjects."
        print k, "categories."

    # Computing p[]
    p = [0.0] * k
    for j in xrange(k):
        p[j] = 0.0
        for i in xrange(N):
            p[j] += mat[i][j]
        p[j] /= N * n
    if DEBUG: print "p =", p

    # Computing P[]    
    P = [0.0] * N
    for i in xrange(N):
        P[i] = 0.0
        for j in xrange(k):
            P[i] += mat[i][j] * mat[i][j]
        P[i] = (P[i] - n) / (n * (n - 1))
    if DEBUG: print "P =", P

    # Computing Pbar
    Pbar = sum(P) / N
    if DEBUG: print "Pbar =", Pbar

    # Computing PbarE
    PbarE = 0.0
    for pj in p:
        PbarE += pj * pj
    if DEBUG: print "PbarE =", PbarE

    kappa = (Pbar - PbarE) / (1 - PbarE)
    if DEBUG: print "kappa =", kappa

    return kappa


def checkEachLineCount(mat):
    """ Assert that each line has a constant number of ratings
        @param mat The matrix checked
        @return The number of ratings
        @throws AssertionError If lines contain different number of ratings """
    n = sum(mat[0])

    assert all(sum(line) == n for line in mat[1:]), "Line count != %d (n value)." % n
    return n

