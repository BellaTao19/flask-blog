from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

#create application object
app = Flask(__name__)

app.secret_key = 'secret'

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs): 
	    if 'logged_in' in session:
	    	return f(*args, **kwargs)
	    else:
	        flash('You need to log in first')
	        return redirect(url_for('login'))
	return wrap

#link function to url 	
@app.route('/')
@login_required
def home():
	return render_template('index.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/login', methods = ['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        	error = 'Invalid Credentials. Please Try Again'
         else:
         	 session['logged_in'] = True
         	 flash('You were just logged in!')
        	 return redirect(url_for('home'))

	return render_template('login.html', error = error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out!')
	return redirect(url_for('login'))

if __name__ == '__main__':
     app.run(debug = True)

