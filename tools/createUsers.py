__author__ = 'muhammad'
from models.LabeledReviews import labeledReview
from models.Users import User
import random



def createUser():
    u = User()
    u.user_id = 20
    u.username = "hallawa"
    u.password = "hallawa"
   # u.save(force_insert=True)
    return u



if __name__ == '__main__':
    u = createUser()
    reviews = labeledReview().getAllLabeledReviewsByUserId(11)
    random.shuffle(reviews)
    for r in reviews:
        print r.review.stars
        l = labeledReview()
        l.review_id = r.review_id
        l.project_id = r.project_id
        l.done = 0
        l.bug_report = 0
        l.feature_feedback = 0
        l.feature_request = 0
        l.feature_shortcoming = 0
        l.praise= 0
        l.complaint= 0
        l.usage_scenario = 0
        l.sentiment = -1
        l.other = ""
        l.noise= 0
        l.user_id = u.user_id
       # l.save()
