from flask import Flask, request, redirect, jsonify, render_template, url_for, make_response
from controllers.controller import Controller
from models.Users import User
from controllers.Session import Session
from controllers.SessionManager import SessionManager
import HTMLParser

app = Flask(__name__)

sessionManager = SessionManager()
currentSession = Session(0, None, None)
htmlParser = HTMLParser.HTMLParser()


@app.route('/')
def gotoLogin():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def index():
    return render_template('login.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def signIn():
    result = validateUser(request.form.get('username'), request.form.get('password'))
    print "signing in.. ", request.form.get('username'), request.form.get('password'), " is allowed? ", result
    if result:
        resp = make_response(redirect(url_for('view')))
        resp.set_cookie('username', request.form.get('username'))
        return resp
    return render_template('login.html', error="Wrong username or password!")


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    print "Logging out ..", sessionManager.sessions
    return redirect(url_for('index'))


@app.route('/main')
def view():
    currentUser = request.cookies.get('username')
    if not currentUser or not sessionManager.getSessionByUser(currentUser):
        return redirect(url_for('index'))
    currentSession = sessionManager.getSessionByUser(currentUser)
    if currentSession.getSessionUser().getAuthenticate():
        c = currentSession.getSessionController()
        l = c.getReivew()
        r = l.review
        projects = c.getProjects()
        return render_template('main.html', username=currentSession.getSessionUser().username,
                               comment=htmlParser.unescape(r.comment), title=htmlParser.unescape(r.title),
                               stars=r.stars, projects=projects, currentProject=c.getCurrentProject(),
                               bug=l.bug_report, ff=l.feature_feedback, fr=l.feature_request, fs=l.feature_shortcoming,
                               us=l.usage_scenario, pr=l.praise, co=l.complaint, noise=l.noise,
                               other=decodeInput(l.other), sentiment=l.sentiment,
                               numberOfReviewsPerProject=c.getNumberOfReviewsPerProject(), reviewId=c.getReviewId(),
                               totalNumberOfDoneReviews=c.getNumberOfDoneReviews(),
                               totalNumberOfOverallReviews=c.getNumberOfOverallReviews())
    else:
        return redirect(url_for('index'))

@app.route('/save')
def saving():
    isSaved = save(request.args.get('bug'), request.args.get('ff'), request.args.get('fr'), request.args.get('fs'),
                   request.args.get('us'), request.args.get('pr'), request.args.get('co'), request.args.get('other')
                   , convertInput(request.args.get('sentiment')), request.args.get('noise'))
    if isSaved is False:
        return jsonify(error="error")
    controller = getCurrentController()
    return jsonify(totalNumberOfDoneReviews=controller.getNumberOfDoneReviews()
                   , totalNumberOfOverallReviews=controller.getNumberOfOverallReviews())

@app.route('/goTo')
def goTo():
    c = getCurrentController()
    return manageData(c, request, 'goTo')

@app.route('/next')
def next():
    c = getCurrentController()
    return manageData(c, request, 'next')


@app.route('/prev')
def prev():
    c = getCurrentController()
    return manageData(c, request, 'prev')


@app.route('/changeProject')
def changeProject():
    c = getCurrentController()
    return manageData(c, request, "changeProject")


def manageData(controller, request, action):
    isSaved = True
    if action != "prev" and action !="goTo":
        isSaved = save(request.args.get('bug'), request.args.get('ff'), request.args.get('fr'), request.args.get('fs'),
                   request.args.get('us'), request.args.get('pr'), request.args.get('co'), request.args.get('other')
                   , convertInput(request.args.get('sentiment')), request.args.get('noise'))
    if isSaved is False:
        return jsonify(error="error")
    else:

        if action == "changeProject":
            currProject = request.args.get('currProject')
            controller.setCurrentProject(currProject)
            l = controller.getReivew()
            r = l.review
            return jsonify(comment=htmlParser.unescape(r.comment), title=htmlParser.unescape(r.title)
                           , stars=r.stars, currentProject=currProject, bug=l.bug_report,
                           ff=l.feature_feedback, fr=l.feature_request, fs=l.feature_shortcoming, us=l.usage_scenario,
                           pr=l.praise, co=l.complaint, other=decodeInput(l.other),
                           sentiment=l.sentiment, noise=l.noise,
                           numberOfReviewsPerProject=controller.getNumberOfReviewsPerProject(),
                           reviewId=controller.getReviewId(),
                           totalNumberOfDoneReviews=controller.getNumberOfDoneReviews()
                           , totalNumberOfOverallReviews=controller.getNumberOfOverallReviews())
        if action == "next":
            controller.onNext()
        if action == "prev":
            controller.onPrev()
        if action == "goTo":
            review_idx = int(request.args.get('review_idx')) -1
            if not request.args.get('review_idx').isdigit() or review_idx < 0:
                return jsonify(error="alphaerror")
            current_review_idx = controller.getReviewId()
            print "number of done reviews per project " ,controller.getNumberOfDoneReviewsPerProject(), " goto index", review_idx
            if controller.getNumberOfDoneReviewsPerProject() < review_idx:
                return jsonify(error="error")
            controller.goTo(review_idx)
        l = controller.getReivew()
        r = l.review
        return jsonify(comment=htmlParser.unescape(r.comment), title=htmlParser.unescape(r.title), stars=r.stars,
                       bug=l.bug_report, ff=l.feature_feedback,
                       fr=l.feature_request, fs=l.feature_shortcoming, us=l.usage_scenario, pr=l.praise, co=l.complaint,
                       noise=l.noise, other=decodeInput(l.other), sentiment=l.sentiment
                       , numberOfReviewsPerProject=controller.getNumberOfReviewsPerProject()
                       , reviewId=controller.getReviewId(), totalNumberOfDoneReviews=controller.getNumberOfDoneReviews()
                       , totalNumberOfOverallReviews=controller.getNumberOfOverallReviews())


def convertBool(val):
    if (val == 'true'):
        return True
    return False


def convertInput(val):
    if val == 'None' or val == 'none' or val == None or val == "" or val == '-1':
        return -1
    if not val:
        return -1
    else:
        return val


def decodeInput(val):
    if val == -1 or val == 'None' or val == None:
        return ""
    return val


def validateUser(username, password):
    u = User().getUserbyUsername(username)
    if not u:
        return False
    else:
        if (u.password == password):
            u.setAuthenticate()
            # ------------------------------------------------------------------------------
            # Create New Session
            newController = Controller()
            newController.setUserId(u.user_id)
            newController.CreateController()
            sessionManager.createNewSession(u, newController)
            return True
        else:
            return False


def getCurrentController():
    currentSession = sessionManager.getSessionByUser(request.cookies.get('username'))
    print "current session controller user id =", currentSession.getSessionController().getUserId()
    return currentSession.getSessionController()


def save(bug, ff, fr, fs, us, pr, co, other, sentiment, noise):
    print "saving., bug = ", bug, ", ff = ", ff, ", fr = ", fr, ", fs = ", fs, ", pr = ", pr, ", co = ", co, ", other = ", other, ", sentiment = ", sentiment, ", noise = ", noise
    bug = convertBool(bug)
    ff = convertBool(ff)
    fr = convertBool(fr)
    fs = convertBool(fs)
    us = convertBool(us)
    pr = convertBool(pr)
    co = convertBool(co)
    no = convertBool(noise)
    other = convertInput(other)
    sentiment = convertInput(sentiment)
    if not validateInput(bug, ff, fr, fs, pr, us, co, other, sentiment, no):
        return False
    currentController = getCurrentController()
    currentController.setNumberOfDoneReviews()
    currentController.setBugReport(bug)
    currentController.setFeatureFeedback(ff)
    currentController.setFeatureRequest(fr)
    currentController.setFeatureShortcoming(fs)
    currentController.setPraise(pr)
    currentController.setComplaint(co)
    currentController.setNoise(no)
    currentController.setUsageScenario(us)
    currentController.setOther(decodeInput(other))
    currentController.setDone()
    currentController.setSentiment(sentiment)
    currentController.saveLabeledReview()
    return True


def validateInput(bug, ff, fr, fs, pr, us, co, other, sentiment, noise):
    print "validating.. bug ", bug, " ff ", ff, " fr ", fr, " fs ", fs, " pr ", pr, " co ", co, " other ", other, " sentiment ", sentiment, " noise ", noise
    if noise is True:
        return True
    if (((bug is False) and (ff is False) and (fr is False) and (fs is False) and (us is False) and (co is False) and (
        pr is False) and (other == -1))
        or ((sentiment == -1))):
        print "validation is false"
        return False
    return True


if __name__ == '__main__':
    app.run(debug=True)

   