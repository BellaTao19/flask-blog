from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3

#create application object
app = Flask(__name__)

app.secret_key = 'secret'
app.database = "blog.db"

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
	g.db = connect_db()
	cur = g.db.execute('select * from entry')
	entries = [dict(entry_id=row[0], entry_title=row[1], entry_body=row[2],entry_date=row[3]) for row in cur.fetchall()]
	g.db.close()

	return render_template('index.html', entries = entries)

@app.route('/newentry',methods = ['GET','POST'])
@login_required
def newEntry():
	error = None
	if request.method == 'POST':
		g.db = connect_db()
		# cur = g.db.execute('DECLARE @entry_title TEXT')
		title=request.form['entry_title']
		print title
		body=request.form['entry_body']
		print body 
        # cur = g.db.execute('SET @entry_title='+ title)
        # cur = g.db.execute('DECLARE @entry_body TEXT')
        # cur = g.db.execute('SET @entry_body = request.form['entry_body']')
		cur = g.db.execute('INSERT INTO entry VALUES(title, body, CURRENT_TIMESTAMP)')
		return redirect(url_for('home'))
	return render_template('newEntry.html', error = error)
	


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

def connect_db():
	return sqlite3.connect(app.database)


if __name__ == '__main__':
     app.run(debug = True)

