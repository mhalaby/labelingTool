from flask import Flask,request, jsonify,render_template
from controllers.controller import Controller

app = Flask(__name__)
@app.route('/')    
def index():
    return render_template('test.html')

c = Controller()
@app.route('/main/')
def view():
    l = c.getReivew()    
    r = l.review
    projects = c.getProjects()
    print l.feature_feedback
    return render_template('main.html', comment=r.comment , title= r.title, stars= r.stars, projects = projects, currentProject = c.getCurrentProject(),
                           bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment)
@app.route('/save') 
def saving():
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))
    return jsonify()
@app.route('/next')
def next():   
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))    
    c.OnNext()    
    print 'next', request.args.get('sentiment'),convertSentiment(request.args.get('sentiment'))
    l = c.getReivew()    
    r = l.review
    print "saved id ", r.review_id,l.feature_feedback,l.sentiment
    return jsonify(comment= r.comment , title= r.title, stars= r.stars,
                    bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment) 

@app.route('/prev')
def prev():
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))
    c.OnPrev()    
    l = c.getReivew()    
    r = l.review
    return jsonify(comment= r.comment , title= r.title, stars= r.stars,
                    bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment)
def convertBool(val):
    if(val == 'true'):
        return True
    return False
def convertSentiment(val):
    if not val:
        return None
    else:
        return val
def save(bug,ff,fr,other,sentiment):   
    c.setBugReport(convertBool(bug))
    c.setFeatureFeedback(convertBool(ff))
    c.setFeatureRequest(convertBool(fr))
    c.setOther(other)
    c.setSentiment(sentiment)
    c.saveLabeledReview()
    
@app.route('/changeProject')
def changeProject():
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))

    currProject = request.args.get('currProject')
    c.setCurrentProject(currProject)
    l = c.getReivew()    
    r = l.review
    return jsonify(comment= r.comment , title= r.title, stars= r.stars,currentProject= currProject,
                    bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment)

if __name__ == '__main__':
    app.run(debug=True)
