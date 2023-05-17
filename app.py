from flask import Flask, render_template, request, session, redirect, url_for
#we must import flask to use it, render_template  allows connection to HTML, request allows data to be fetched from any database.
#session allows users data and activity on the website to be stored, redirect just returns user back to a specifc page.
# url_for provides another connection function.
import os
# imports a python module.
import sqlite3
# imports sqlite as the database.
from markupsafe import escape
from datetime import timedelta
#allows the implementation and connection to the date and time.

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
#random key used to send and save data in the browser and is used for sessions.
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1)
#This is necessary for the timeout function to be implemented for each session.

@app.route('/')
def home():
        return render_template('homepage.html')

@app.route('/user')
#labels the login html page as "user"
def user():
    # def creates a function
    return render_template('login.html')
    #outputs the html page in the brackets (login.html)

@app.route('/register')
#This code creates a route for the '/register' endpoint to handle user registration.
def register():
    #creates a function for register
    return render_template('signup.html')
    #outputs the html page in the brackets (signup.html)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tetra')
def tetra():
    return render_template('tetra.html')

@app.route('/signup',methods=['POST'])
def signup():
    #creates a function called signup
    with sqlite3.connect('fish.db') as db:
    #connects to the SQLite database named 'fish.db'
        cursor = db.cursor()
        # creates a cursor connection
        cursor.execute("INSERT INTO USER (Username, Email, Password) VALUES (?,?,?)",
			       		(request.form['username'],request.form['email'], request.form['password']))
                        # INSERT statement inserts the values 'username', 'email' and 'password' from the request.form into the 'USER' table.
        db.commit()
        session.permanent = True
        #creates a session lifetime == permanent, so data be saved
        session['username'] = request.form['username']
        # code sets request.form['username'] (value) to the 'username' key for the session
        return render_template('homepage.html') + "Welcome " + request.form['username']
        # Redirect the user back to the homepage and provides a welcome message.


@app.route('/create')
#creates a table in the Database, in this case using sqlite
def create():
            with sqlite3.connect('fish.db') as db:
                # assigning fish.db as the name of the Database
                cursor = db.cursor()
                # creates a cursor connection
                cursor.execute(	"""	CREATE TABLE IF NOT EXISTS USER(
						Username text VARCHAR(20) NOT NULL,
                        Email text VARCHAR(20) NOT NULL,
						Password text VARCHAR(20) NOT NULL,
						Primary Key(Username))""")
                db.commit()
                return 'created'
                # cursor.execute is used to create the table.
                # the operations are inputted within the brackets (Username,Email etc...)
                # NOT NULL meaning each operation requirement must be filled.
                # return created will me be shown once the table is created.





@app.route('/select')
def select():
    con = sqlite3.connect('fish.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM USER")
    rows = cur.fetchall()
    return render_template('table.html', rows=rows)


def insert():
  with sqlite3.connect('fish.db') as db:
    cursor = db.cursor()

    # Check if the email is NULL
    if request.form['email'] is None:
      # The email is NULL, do not insert the new row
      print('Email cannot be NULL')
    else:
      cursor.execute("""
        INSERT INTO USER (Username, Password, Email)
        VALUES (?, ?, ?)
      """, (request.form['username'], request.form['email'], request.form['password']))
      db.commit()
  return request.form['username'] + ' added'

		#cursor.execute("""	INSERT INTO Users (email, Password)



@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect('fish.db')
    #'connect' is used to create a connection with the 'fish.db' database
    cur = con.cursor()
    cur.execute("SELECT * FROM USER WHERE Username=?  AND Password=?",
    #searches for the username and password in the USER table
    (request.form['username'], request.form['password']))
    #requests these two form values the username and the password
    match = len(cur.fetchall())
    #checks if their is a match by comparing the inputted data to the data in the table
    if match == 0:
        #if match is equal to 0 then the user has entered the incorrect password. So one that isn't found in the db
        return "Wrong email and password"
        #return this message
    else:
        session.permanent = True
        #if the entered credentials are correct, so match the values in the db, A session is started for the user.
        session['unam'] = request.form['username']
        #session is labelled 'unam', and is stored under the users username
        return render_template('homepage.html') + "Welcome " + request.form['username']
        #directs the user to the homepage, and presents this message welcome + for e.g Bob


    #else:
        #request.form["password"]= 2005
        #request.form["Username"]= "MrTom"
        #return render_template('homepage.html') + "Welcome " + request.form['username']


@app.route('/un')
def un():
    if 'unam' in session:
        return 'Logged in as %s' % escape(session['unam'])
    return render_template('homepage.html') +  'You are not logged in'

@app.route('/logout')
def logout():
    session.pop('unam', None)
    return redirect(url_for('un'))

@app.route('/tetra')
def fish():
  connection = sqlite3.connect("ourfish.db")
  cursor = connection.cursor()

  sqlcommand = """


      CREATE TABLE IF NOT EXISTS tblfish
      (
          fishID       TEXT,
          fishName     TEXT,
          price        INTEGER,
          size         TEXT,
          tempRange    TEXT,
          pHRange      TEXT,
          rating       TEXT,
          primary key   (fishID)
      )"""

  cursor.execute(sqlcommand)
  print("tblfish table has been created in ourfish.db")
  tblTemps = [('001','Neon Tetra',1.45,'3cm','21–27°C','6.0–6.5',"***"),
              ('002','Serpae Tetra',2.50,'3cm','22-27°C','6.0–8.0',"****"),

              ]
  #cursor.executemany("INSERT INTO tblFISH1 VALUES (?,?,?,?,?,?,?)", (request.form['fishID'], request.form['fishName'], (request.form['price'], request.form['size'], request.form['tempRange'], request.form['pHRange'], (request.form['rating'])
  cursor.executemany("INSERT or REPLACE into tblfish VALUES (?,?,?,?,?,?,?)",tblTemps)
  print("\n To select and display only records whichs are of 'Action' and 'Animation category")
  for row1 in cursor.execute('SELECT * FROM tblfish WHERE rating = "***" '):
    print(row1)
  connection.commit()
  connection.close()
fish()

#@app.route('/createfishtable')
#def create():
            #with sqlite3.connect('fish.db') as db:
                #cursor = db.cursor()
                #cursor.execute(	"""	CREATE TABLE IF NOT EXISTS tblFISH(
				#		Username text,
				#		Password text,
				#		Primary Key(Username))""")
                #db.commit()
                #return 'created'


