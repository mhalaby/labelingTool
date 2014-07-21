from flask import Flask,request, redirect,jsonify,render_template,url_for
from controllers.controller import Controller
from models.Users import User

app = Flask(__name__)
c = Controller()
user = User()
Session = {}

@app.route('/')
def gotoLogin():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])    
def index():
    return render_template('login.html')

@app.route('/sign_in', methods=['POST', 'GET'])
def signIn():     
    result =  validate_user(request.form.get('username'), request.form.get('password'))
    if result:
        return redirect(url_for('view'))        
    return render_template('login.html',error="Wrong username or password!")

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    Session.clear()
    print Session
    return redirect(url_for('index'))

@app.route('/main')
def view():
    if not Session:
        return redirect(url_for('index'))
    if Session['user'].getAuthenticate():
        c.setUserId(Session['user'].user_id)
        c.init()
        l = c.getReivew()    
        r = l.review
        projects = c.getProjects()    
        return render_template('main.html', username=Session['user'].username, comment=r.comment , title= r.title, stars= r.stars, projects = projects, currentProject = c.getCurrentProject(),
                           bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment)
    else:
        return redirect(url_for('index'))
    
     
@app.route('/save') 
def saving():
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))
    return jsonify()

@app.route('/next')
def next():   
    print 'next', request.args.get('sentiment'),convertSentiment(request.args.get('sentiment'))

    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))    
    c.OnNext()    
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
@app.route('/changeProject')
def changeProject():
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))

    currProject = request.args.get('currProject')
    c.setCurrentProject(currProject)
    l = c.getReivew()    
    r = l.review
    return jsonify(comment= r.comment , title= r.title, stars= r.stars,currentProject= currProject,
                    bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment)

def convertBool(val):
    if(val == 'true'):
        return True
    return False

def convertSentiment(val):
    if val is 'None':
        return -1
    if not val:
        return -1
    else:
        return val
def decodeSentiment(val):
    if val == -1:
        return None
def validate_user(username,password):  
    u = User().getUserbyUsername(username)
    if not u:
        return False
    else:
        if(u.password == password):
            u.setAuthenticate()  
            Session['user']=u
            return True
        else:
            return False

def save(bug,ff,fr,other,sentiment):  
    c.setBugReport(convertBool(bug))
    c.setFeatureFeedback(convertBool(ff))
    c.setFeatureRequest(convertBool(fr))
    c.setOther(other)
    c.setSentiment(convertSentiment(sentiment))
    c.saveLabeledReview()
    

if __name__ == '__main__':
    app.run(debug=True)
