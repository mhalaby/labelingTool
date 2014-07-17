from flask import Flask,request, jsonify,render_template
from controllers.controller import Controller

app = Flask(__name__)
@app.route('/')    
def index():
    return render_template('test.html')

c = Controller()
@app.route('/main/')
def view():    
    r = c.loadReviews()[0]
    return render_template('main.html', comment=r.comment , title= r.title, stars= r.stars)
 
@app.route('/next')
def next():
    c.OnNext()    
    r = c.getReivew()
    return jsonify(comment= r.comment , title= r.title, stars= r.stars) 

@app.route('/prev')
def prev():
    c.OnPrev()    
    r = c.getReivew()
    return jsonify(comment= r.comment , title= r.title, stars= r.stars) 
 
if __name__ == '__main__':
    app.run(debug=True)
