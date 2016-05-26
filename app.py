from flask import Flask, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
import mongoutils
import json
import random

app = Flask(__name__)


@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        print 'a'
        error = ""
        print request.form
        user = str(request.form['user'])
        password = str(request.form['pass'])
        user_type = str(request.form['rights'])
        if request.form.has_key('login'):
            print '5'
            if user_type == "admin" and mongoutils.authenticateA(user,password):
                session['user'] = user
                return redirect("/admin")
            if user_type == "competitor" and mongoutils.authenticateU(user,password):
                session['user'] = user
                return redirect("/competitor")
            else:
                error = "Incorrect Username or Password. Try Again."
                return render_template("index.html",error=error)            
        if request.form.has_key('register'):
        	all_rows = mongoutils.getAll()
    		for n in range(len(all_rows)):
        		all_rows[n] = all_rows[n]['name']
    		print all_rows
    		print '1'
    		email = str(request.form['email'])
    		print '2'
    		if user in all_rows:
    			print '3'
    			error = "Username already exists. Please try another"
    			return render_template("index.html",regerror=error)
    		else:
    			print '4'
    			message = "Account Created!"
    			session['user'] = user
    			if user_type == "admin":
    				mongoutils.addAdmin(user,password,email)
    				return redirect("/admin")
    			else:
    				mongoutils.addUser(user, password, email)
    				return redirect("/competitor")
    			return redirect("/admin")
    return render_template("index.html") #login failed
    

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
    admins = getAllAdmins()
    if user not in admins:
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
