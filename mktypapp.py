"""
    Brandeis Friender
	Developers:


    The authentication comes from an app by Bruno Rocha
    GitHub: https://github.com/rochacbruno
"""
from functools import wraps
from flask import Flask, redirect, url_for, session, request, jsonify, render_template, request
from flask_oauthlib.client import OAuth
from datetime import datetime


app = Flask(__name__)
app.config['GOOGLE_ID'] = '246096591118-ti33uv184e4m1bib9grgn8alm45btadb.apps.googleusercontent.com'
app.config['GOOGLE_SECRET'] = 'iqgLqu6pXgLuHsZFq6nvxDX3'


app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not('google_token' in session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/main')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        print("logged in")
        print(jsonify(me.data))
        return render_template("main.html")
        #return jsonify({"data": me.data})
    print('redirecting')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    #
    return redirect(url_for('main'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    print(session['google_token'])
    me = google.get('userinfo')
    session['userinfo'] = me.data
    print(me.data)
    return render_template("main.html")
    #return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')



@app.route('/')
def main():
	return render_template("main.html")

@app.route('/team')
def team():
	return render_template('team.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/arnell')
def arnell():
	return render_template('arnell.html')
@app.route('/jasmine')
def jasmine():
	return render_template('jasmine.html')
@app.route('/dario')
def dario():
	return render_template('dario.html')

@app.route('/pitch')
def pitch():
	return render_template('pitch.html')

@app.route('/survey')
@require_login
def survey():
	return render_template('survey.html')


surveys = []
surveyCounter=0


@app.route('/processSurvey',methods=['GET','POST'])
def processSurvey():
	global surveys
	global surveyCounter
	print("entering processSurvey")
	if request.method == 'POST':
		print("Entering POST branch")
		userinfo = session['userinfo']

		who = userinfo['email']

		b = request.form['birthplace']
		i = request.form['interests']
		y = request.form['year']
		print("A")
		t = request.form['TVshow']
		print("B")
		m = request.form['music']
		print("C")
		p = request.form['magicalpower']
		print("D")
		f = request.form['favoritefood']
		print("E")
		h = request.form['favoriteholiday']
		print("F")
		n = datetime.now()
		print("G")
		print(surveyCounter)
		print("H")
		survey = {
			'id':surveyCounter,
			'birthplace':b,
			'interests':i,
			'year':y,
			'TVshow':t,
			'music':m,
			'magicalpower':p,
			'favoritefood':f,
			'favoriteholiday':h,
			'time':n,
			'who':who
			}
		print("I")
		surveyCounter = surveyCounter + 1
		surveys.insert(0,survey) # add msg to the front of the list
		print(surveys)
		return render_template("processSurvey.html",surveys=surveys)
	else:
		return render_template("processSurvey.html",surveys=surveys)


friendRequests = []

@app.route('/requestConnection',methods=['GET','POST'])
def requestConnection():
	global surveys
	global friendRequests
	global friendCounter
	print(request.form['surveyNumber'])
	if request.method == 'POST':
		return render_template("friends.html",surveys=surveys)
	else:
		return render_template("friends.html",surveys=surveys)


@app.route('/formdemo')
def formdemo():
	return render_template('formdemo.html')

@app.route('/chat',methods=['GET','POST'])
def chat():
	if request.method == 'POST':
 		msg = request.form['msg']
 		who = request.form['who']
 		now = datetime.now()
 		x = {'msg':msg,'now':now,'who':who}
 		messages.insert(0,x) # add msg to the front of the list
 		return render_template("chat.html",messages=messages)
	else:
		return render_template("chat.html",messages=[])


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)
