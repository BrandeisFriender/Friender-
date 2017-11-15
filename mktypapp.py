from flask import Flask, render_template, request
app = Flask(__name__)


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

@app.route('/pitch')
def pitch():
	return render_template('pitch.html')

@app.route('/survey')
def survey():
	return render_template('survey.html')

@app.route('/formdemo')
def formdemo():
	return render_template('formdemo.html')


if __name__ == '__main__':
    app.run('0.0.0.0',port=3000)
