# generate csv
# Date: 15/08/2014
from models.LabeledReviews import labeledReview
import HTMLParser

if __name__ == '__main__':
    user1Id = 13
    htmlParser = HTMLParser.HTMLParser()
    reviews1 = labeledReview().getAllLabeledReviewsByUserId(user1Id)
    # The TSV header
    #====================================================================#
    # labelled review id, label id, sentiment, project id, ratings, text
    #====================================================================#
    g = open('dataset.tsv', 'w')

    for r in reviews1:
        # {'1':'bug report','2':'feature strength','3':'feature shortcoming','4':'feature request','5':'praise','6':'complaint','7':'noise'}
        # sentiment {'1':'very negative','2':'negative','3':'neutral','4':'positive','5':'very positive'}
        review_comment = htmlParser.unescape(r.review.title + " " + r.review.comment).replace("\n"," ")
        if r.bug_report:
            target = 1
            g.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
                r.id, target, r.sentiment, r.project_id, r.review.stars,
                review_comment))
        if r.feature_feedback:
            target = 2
            g.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
                r.id, target, r.sentiment, r.project_id, r.review.stars,
                review_comment))
        if r.feature_shortcoming:
            target = 3
            g.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
                r.id, target, r.sentiment, r.project_id, r.review.stars,
                review_comment))
        if r.feature_request:
            target = 4
            g.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
                r.id, target, r.sentiment, r.project_id, r.review.stars,
                review_comment))
        if r.praise:
            target = 5
            g.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
                r.id, target, r.sentiment, r.project_id, r.review.stars,
                review_comment))
        if r.complaint:
            target = 6
            g.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
            r.id, target, r.sentiment, r.project_id, r.review.stars, review_comment))
        if r.noise:
            target = 7
            g.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
            r.id, target, r.sentiment, r.project_id, r.review.stars, review_comment))
    g.close()