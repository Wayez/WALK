from flask import Flask, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
import mongoutils
import json
import random

app = Flask(__name__)


@app.route("/login", methods = ['GET','POST'])
def login():
    all_rows = mongoutils.getAllAdmins()
    for n in range(len(all_rows)):
        all_rows[n] = all_rows[n]['name']
    print all_rows
    if request.method == 'POST':
        print 'a'
        error = ""
        print request.form
        if request.form.has_key('login'):
            user = str(request.form['user'])
            password = str(request.form['pass'])
            print '5'
            if mongoutils.authenticateA(user,password):
                session['user'] = user
                return redirect("/home")
            else:
                error = "Incorrect Username or Password. Try Again."
                return render_template("index.html",error=error)            
        if request.form.has_key('register'):
            print '1'
            user = str(request.form['reguser'])
            password = str(request.form['regpass'])
            email = str(request.form['email'])
            print '2'
            if user in all_rows:
                print '3'
                error = "Username already exists. Please try another"
                return render_template("index.html",regerror=error)
            else:
                print '4'
                message = "Account Created!"
                mongoutils.addAdmin(user,password,email)
                session['user'] = user
                return redirect("/admin")
    return render_template("index.html") #login failed

@app.route("/admin", methods = ['GET','POST'])
def home():
    if 'user' not in session:
        return redirect ("/login")
    if request.method == 'POST':
        print request.form
        if request.form.has_key('submit'):
        	name = str(request.form['name'])
        	teams = []
        	numTeam = 0
        	while not str(request.form['name' + numTeam]) is None:
        		teams.append(request.form['name' + numTeam])
        		numTeam = numTeam + 1
        	results = 0
        	ida = random.randint(0, 10000)
        	while not mongoutils.getTourn(ida) is None:
        		ida = random.randint(0, 10000)
        	if mongoutils.createTourn(name, teams, results, ida):
        		return redirect("/bracket")
        	else: #tournament name taken
        		return render_template("newtourn.html")
        #mongoutils.createTourn(stuff)
    return render_template("newtourn.html")

@app.route("/bracket")
def bracket():
    if 'user' not in session:
        return redirect ("/login")
    return render_template("bracket.html")
    
@app.route("/logout")
def logout():
    del session['user']
    return redirect("/login")


if __name__ == '__main__':
    app.secret_key = "hello"
    app.debug = True
    app.threaded = True
    app.run(host='0.0.0.0', port=8000)
else:
    app.secret_key = "hello"
    app.debug = True
