# Date: 15/08/2014
from models.LabeledReviews import labeledReview
import math
from collections import defaultdict
import copy

def strictAggreement(reviews1,reviews2,ids):
    count = 0
    re1= copy.deepcopy(reviews1)
    re2= copy.deepcopy(reviews2)
    for i in ids:
        re1[i].user_id = 0         
        re2[i].user_id = 0
        re1[i].id = 0
        re2[i].id = 0

        if re1[i].noise:
            re1[i].sentiment = -1
        if re2[i].noise:
            re2[i].sentiment = -1
        if len(re1[i].other) > 1:
            re1[i].other = 1
        if len(re2[i].other) > 1:
            re2[i].other = 1
        if re1[i] == re2[i]:
            count += 1
    print "Total number of reviews ", len(re1)
    print "number of agreement ", count
    print "percentage ", round((float(count) / float(len(re1))) * 100, 2)
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

def checkMultiLabel(reviews1,reviews2,idx):
    r1= copy.deepcopy(reviews1)
    r2= copy.deepcopy(reviews2)
    count = 0
    mcount = 0
    bugCount = 0
    strengthCount = 0
    shortcomingCount = 0
    requestCount = 0
    praiseCount = 0
    complaintCount = 0
    usageCount = 0
    noiseCount = 0
    otherCount = 0
    g = open('Results_user_'+str(user2Id)+".txt", 'w')
    for i in idx:
        r2[i].user_id = 0
        r1[i].user_id = 0
        r1[i].id = 0
        r2[i].id = 0
        # ignore sentiment
        r1[i].sentiment = 1
        r2[i].sentiment = 1

        if r1[i].noise:
            r1[i].sentiment = -1
        if r2[i].noise:
            r2[i].sentiment = -1
        if len(str(r1[i].other)) > 1:
            r1[i].other = 1
        if len(str(r2[i].other)) > 1:
            r2[i].other = 1
        if r1[i] == r2[i]:
            count += 1
            if r1[i].bug_report:
                bugCount +=1
            if r1[i].feature_feedback:
                strengthCount +=1
            if r1[i].feature_shortcoming:
                shortcomingCount +=1
            if r1[i].feature_request:
                requestCount +=1
            if r1[i].praise:
                praiseCount +=1
            if r1[i].complaint:
                complaintCount +=1
            if r1[i].noise:
                noiseCount +=1
            if r1[i].other == 1:
                otherCount +=1
        else:
            if r1[i].equals(r2[i]):
                mcount += 1
            if r1[i].bug_report or r2[i].bug_report :
                bugCount +=1
            if r1[i].feature_feedback or r2[i].feature_feedback:
                strengthCount +=1
            if r1[i].feature_shortcoming or r2[i].feature_shortcoming:
                shortcomingCount +=1
            if r1[i].feature_request or r2[i].feature_request:
                requestCount +=1
            if r1[i].praise or r2[i].praise:
                praiseCount +=1
            if r1[i].complaint or r2[i].complaint:
                complaintCount +=1
            if r1[i].usage_scenario or r2[i].usage_scenario:
                usageCount +=1
            if r1[i].noise or r2[i].noise:
                noiseCount +=1
            if r1[i].other == 1 or r2[i].other == 1:
                otherCount +=1
        
        g.write("%s \n" %r2[i].review.comment)
        g.write( "complaint\t%s \n" % ( r2[i].complaint))
        g.write( "fshort \t%s \n" % (  r2[i].feature_shortcoming))
        g.write( "bug report \t%s \n" %( r2[i].bug_report))
        g.write( "frequest \t%s \n"%(r2[i].feature_request))
        g.write( "fstrength\t%s \n"%(   r2[i].feature_feedback))
        g.write( "usage \t%s \n"%( r2[i].usage_scenario))
        g.write( "praise \t%s \n"%( r2[i].praise))
        g.write( "noise \t%s \n" %(r2[i].noise))
        g.write( "-----------------------------------------------------\n")
    g.write( "bugCount %s \n" %(bugCount))
    g.write( "strengthCount %s \n"%(strengthCount))
    g.write( "shortcomingCount %s \n" %(shortcomingCount))
    g.write( "requestCount %s \n" %(requestCount))
    g.write( "praiseCount %s \n" %(praiseCount))
    g.write( "complaintCount %s \n" %(complaintCount))
    g.write( "usageCount %s \n"%(usageCount))
    g.write( "otherCount %s \n" %(otherCount))
    g.close()
    print "number of agreement without sentiment", count
    print "number of partial agreement without sentiment", mcount
    print "percentage ", round((float(count) / float(len(reviews1))) * 100, 2)
    print "percentage with partial agreement", round((float(count + mcount) / float(len(reviews1))) * 100, 2)

def checkSentimentAgreement(reviews1,reviews2,idx):
    count = 0
    mcount = 0
    r1= copy.deepcopy(reviews1)
    r2= copy.deepcopy(reviews2)
    for i in idx:
        if r1[i].noise:
            r1[i].sentiment = -1
        if r2[i].noise:
            r2[i].sentiment = -1
        if r1[i].sentiment == r2[i].sentiment:
            count += 1
        else:
            if (r1[i].sentiment == 1 and r2[i].sentiment == 2) or (r2[i].sentiment == 1 and r1[i].sentiment == 2):
                mcount += 1
            if (r1[i].sentiment == 4 and r2[i].sentiment == 5) or (r2[i].sentiment == 4 and r1[i].sentiment == 5):
                mcount += 1
    print "number of sentiment agreement ", count
    print "number of sentiment partial agreement ", mcount
    print "percentage ", round((float(count) / float(len(r1))) * 100, 2)
    print "percentage with partial agreement", round((float(count + mcount) / float(len(r1))) * 100, 2)


def convertToDict(reviews):
    rdict = defaultdict()
    ids = set()
    for r in reviews:
        rdict[r.review_id]= r
        ids.add(r.review_id)
    return rdict,ids


def aggreementTest():
    l1 = list(l.review_id for l in labeledReview().getLabeledReviewsByUserId(10,2) if l.review.stars == 1)
    l2 = list(l.review_id for l in labeledReview().getLabeledReviewsByUserId(13,2) if l.review.stars == 1)
    l3 = list(l.review_id for l in labeledReview().getLabeledReviewsByUserId(21,2) if l.review.stars == 1)
    l4 = list(l.review_id for l in labeledReview().getLabeledReviewsByUserId(22,2) if l.review.stars == 1)
    l5 = list(l.review_id for l in labeledReview().getLabeledReviewsByUserId(24,2) if l.review.stars == 1)
    print len(l2)
    print len(set(l1+l2+l3))
    print list(set(l3).intersection(set(l5)))
    print "---------------"
    print list(set(l3).intersection(set(l4)))
    print l3

if __name__ == "__main__":
    user1Id = 11
    user2Id = 30
    # reviews1 = labeledReview()
    reviews1,ids1 = convertToDict(labeledReview().getAllLabeledReviewsByUserId(user1Id))
    reviews2,ids2 = convertToDict(labeledReview().getAllLabeledReviewsByUserId(user2Id))
    #
    idx = ids1.intersection(ids2)
    strictAggreement(reviews1,reviews2,idx)
    checkMultiLabel(reviews1,reviews2,idx)
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    checkSentimentAgreement(reviews1,reviews2,idx)
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

