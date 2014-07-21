from flask import Flask,request, redirect,jsonify,render_template,url_for,make_response
from controllers.controller import Controller
from models.Users import User
from controllers.Session import Session
from controllers.SessionManager import SessionManager
app = Flask(__name__)

sessionManager = SessionManager()
currentSession = Session(0,None,None)
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
        resp = make_response(redirect(url_for('view')) )
        resp.set_cookie('username',request.form.get('username'))
        return resp
    return render_template('login.html',error="Wrong username or password!")

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    print sessionManager.sessions
    return redirect(url_for('index'))

@app.route('/main')
def view():
    currentUser = request.cookies.get('username')
    print 'cookie',currentUser
    print 'print Sessions' ,sessionManager.sessions
    print 'curr session', sessionManager.getSessionByUser(currentUser)
    if not currentUser or not sessionManager.getSessionByUser(currentUser):
        return redirect(url_for('index'))
    currentSession = sessionManager.getSessionByUser(currentUser)
    if currentSession.getSessionUser().getAuthenticate():  
        c = currentSession.getSessionController() 
        l = c.getReivew()    
        r = l.review
        projects = c.getProjects()    
        return render_template('main.html', username= currentSession.getSessionUser().username, comment=r.comment , title= r.title, stars= r.stars, projects = projects, currentProject = c.getCurrentProject(),
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
    c = getCurrentController()    
    c.OnNext()    
    l = c.getReivew()    
    r = l.review
    print "saved id ", r.review_id,l.feature_feedback,l.sentiment
    return jsonify(comment= r.comment , title= r.title, stars= r.stars,
                    bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment) 

@app.route('/prev')
def prev():
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))
    c = getCurrentController()
    c.OnPrev()    
    l = c.getReivew()    
    r = l.review
    return jsonify(comment= r.comment , title= r.title, stars= r.stars,
                    bug=l.bug_report, ff = l.feature_feedback, fr = l.feature_request, other = l.other, sentiment = l.sentiment)
@app.route('/changeProject')
def changeProject():
    save(request.args.get('bug'),request.args.get('ff'),request.args.get('fr'),request.args.get('other'),convertSentiment(request.args.get('sentiment')))
    c = getCurrentController()
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
#------------------------------------------------------------------------------ 
# Create New Session     
            newController= Controller()                 
            newController.setUserId(u.user_id)
            newController.init()
            sessionManager.createNewSession(u,newController)            
            return True
        else:
            return False
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def getCurrentController():
    currentSession = sessionManager.getSessionByUser(request.cookies.get('username'))
    return currentSession.getSessionController()
def save(bug,ff,fr,other,sentiment): 
    print sessionManager.sessions
    for s in sessionManager.sessions:
        print s.user.username, " ",s.c.review_id
    
    currentController = getCurrentController()
    print "saving control", currentController.userId, request.cookies.get('username')
    currentController.setBugReport(convertBool(bug))
    currentController.setFeatureFeedback(convertBool(ff))
    currentController.setFeatureRequest(convertBool(fr))
    currentController.setOther(other)
    currentController.setSentiment(convertSentiment(sentiment))
    currentController.saveLabeledReview()


if __name__ == '__main__':
    app.run(debug=True)
