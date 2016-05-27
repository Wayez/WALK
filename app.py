from flask import Flask, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
import mongoutils
import loginutils
import json
import random

app = Flask(__name__)


@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        print 'a'
        error = ""
        print request.form
        req = {}
        # transfer it otherwise theres a bad request error
        for x in request.form:
            req[x]=request.form[x]
        return loginutils.loginHelper(req)
        
    

@app.route("/competitor", methods = ['GET', 'POST'])
def home_user():
	if 'user' not in session:
		return redirect ("/login")
	return render_template("comp.html")

@app.route("/admin", methods = ['GET','POST'])
def create_tourn():
    if 'user' not in session:
        return redirect ("/login")
    user = session['user']
    print user
    admins = mongoutils.findAdmin(user)
    print admins
    if admins!=user:
    	return redirect("/competitor")
    if request.method == 'POST':
        print request.form
        if request.form.has_key('create'):
            name = str(request.form['name'])
            teams = []
            numTeam = 0
            results = []
            ida = mongoutils.getAdminId(session['user'])
            req = {}
            # transfer it otherwise theres a bad request error
            for x in request.form:
                req[x]=request.form[x]
            # getting all the teams out
            while req.has_key('name' + str(numTeam)):
                teams.append(req['name' + str(numTeam)])
                numTeam += 1
            if mongoutils.createTourn(name, teams, results, ida):
                return redirect("/bracket")
            else:
                return render_template("newtourn.html")
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
