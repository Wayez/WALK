from flask import Flask, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
import mongoutils
import json
import random

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
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
        if req.has_key('login'):
            print '5'
            user = str(req['user'])
            password = str(req['pass'])
            user_type = str(req['rights'])

            if user_type == "admin" and mongoutils.authenticateA(user,password):
                session['user'] = user
                return redirect("/admin")
            if user_type == "competitor" and mongoutils.authenticateU(user,password):
                session['user'] = user
                return redirect("/competitor")
            if user_type == "coach" and mongoutils.authenticateC(user,password):
                session['user'] = user
                return redirect("/coach")
            else:
                error = "Incorrect Username or Password. Try Again."
                return render_template("index.html",error=error)
        if req.has_key('register'):
            user = str(req['reguser'])
            password = str(req['regpass'])
            user_type = str(req['rights'])

            print '6ducks'
            all_rows = mongoutils.getAll()
            for n in range(len(all_rows)):
                all_rows[n] = all_rows[n]['name']
            print all_rows
            print '1'
            email = str(req['email'])
            print '2'
            if user in all_rows:
                print '3'
                error = "Username already exists. Please try another"
                return render_template("index.html",regerror=error)
            else:
                print '4'
                message = "Account Created!"
                session['user'] = user
                print user_type
                print user_type == "admin"
                if user_type == "admin":
                    mongoutils.addAdmin(user,password,email)
                    return redirect("/admin")
                if user_type == "coach":
                    mongoutils.addCoach(user, password, email)
                    return redirect("/coach")
                else:
                    mongoutils.addUser(user, password, email)
                    return redirect("/competitor")
    return render_template("index.html") #login failed


@app.route("/competitor", methods = ['GET', 'POST'])
def home_user():
    if 'user' not in session:
        return redirect ("/login")
    return render_template("comp.html")

@app.route("/admin", methods = ['GET','POST'])
def admin():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    print user
    if mongoutils.isNotAdmin(user):
    	return redirect("/competitor")
    if request.method == 'POST':
        print request.form
        if request.form.has_key('new'):
            return redirect("/newtourn")
        if request.form.has_key('old'):
            tid = mongoutils.getTournId(request.form['old'])
            return redirect("/bracket/"+str(tid))
        if request.form.has_key('logout'):
            return redirect('/logout')
    tornus = mongoutils.getAdminTourns(mongoutils.getAdminId(session['user']))
    return render_template("admin.html",tourns=tornus)

@app.route("/coach", methods = ['GET','POST'])
def coach():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    print user
    if mongoutils.isNotCoach(user):
        if mongoutils.isNotAdmin(user):
            return redirect("/competitor")
        return rediect("/admin")
    if request.method == 'POST':
        print request.form
        if request.form.has_key('new'):
            return redirect("/newteam")
        if request.form.has_key('old'):
            tid = mongoutils.getTeamId(request.form['old'])
            #return redirect("/bracket/"+str(tid))
            return redirect("/coach")
        if request.form.has_key('logout'):
            return redirect('/logout')
    teams = mongoutils.getCoachTeams(session['user'])
    print teams
    print  session['user']
    return render_template("coach.html",teams=teams)

@app.route("/newtourn", methods = ['GET','POST'])
def new_tourn():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    print user
    if mongoutils.isNotAdmin(user):
        if mongoutils.isNotCoach(user):
            return redirect("/competitor")
        return redirect("/coach")
    if request.method == 'POST':
        print request.form
        if request.form.has_key('logout'):
            return redirect('/logout')
        if request.form.has_key('create'):
            name = str(request.form['name'])
            teams = []
            numTeam = 0
            win =  [[[], [], [], [], [], [], [], []],
                    [[], [], [], []],
                    [[], []],
                    [[]]]
            lose = [[[], [], [], []],
                    [[], [], [], []],
                    [[], []],
                    [[], []],
                    [[]],
                    [[]]]
            finals=[[[], []],
                    [[]]]
            ida = mongoutils.getAdminId(session['user'])
            req = {}
            # transfer it otherwise theres a bad request error
            for x in request.form:
                req[x]=request.form[x]
            # getting all the teams out
            while req.has_key('name' + str(numTeam)):
                teams.append(req['name' + str(numTeam)])
                numTeam += 1
            if mongoutils.createTourn(name, teams, win, lose, final, ida):
                tid = mongoutils.getTournId(name)
                return redirect("/bracket/"+str(tid))
            else:
                return render_template("newtourn.html")
    return render_template("newtourn.html")

@app.route("/newteam", methods = ['GET','POST'])
def new_team():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    print user
    if mongoutils.isNotCoach(user):
        if mongoutils.isNotAdmin(user):
            return redirect("/competitor")
        return redirect("/admin")
    if request.method == 'POST':
        print request.form
        if request.form.has_key('logout'):
            return redirect('/logout')
        if request.form.has_key('create'):
            name = str(request.form['name'])
            competitors = []
            numComps = 0
            #results = []
            coach = user
            req = {}
            # transfer it otherwise theres a bad request error
            for x in request.form:
                req[x]=request.form[x]
            # getting all the teams out
            while req.has_key('name' + str(numComps)):
                competitors.append(mongoutils.getUserId(req['name' + str(numComps)]))
                numComps += 1
            if mongoutils.createTeam(name, coach, competitors):
                tid = mongoutils.getTeamId(name)
                #return redirect("/bracket/"+str(tid))
                #return redirect("/team" + str(tid))
                return redirect("/coach")
            else:
                return render_template("newteam.html")
    return render_template("newteam.html")

@app.route("/bracket/<int:tid>")
def bracket(tid):
    if 'user' not in session:
        return redirect ("/login")
    if request.method == 'POST':
        if request.form.has_key('logout'):
            return redirect('/logout')
    #if not mongoutils.isNotAdmin(session['user']):
        #aid = mongoutils.getAdminId(session['user'])
        #tid = mongoutils.getTourn(aid)
    tjason = {"teams":mongoutils.getTournTeams(tid)}
    wjason = {"results":mongoutils.getTournWinners(tid)}
    ljason = {"results":mongoutils.getTournLosers(tid)}
    fjason = {"results":mongoutils.getTournFinals(tid)}
    nom = mongoutils.getTournName(tid)
    print "\n\n",jason,"\n\n"
    return render_template("bracket.html",name=nom,teams=tjason,
                           losers=ljason,winners=wjason,finals=fjason)
    
@app.route("/logout")
def logout():
    del session['user']
    return redirect("/login")

@app.route("/update")
def update():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    print user
    if mongoutils.isNotAdmin(user):
    	return redirect("/competitor")
    if request.method == 'POST':
        pass
    return render_template("update.html")


if __name__ == '__main__':
    app.secret_key = "hello"
    app.debug = True
    app.threaded = True
    app.run(host='0.0.0.0', port=8000)
else:
    app.secret_key = "hello"
    app.debug = True
