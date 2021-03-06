from flask import Flask, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
import mongoutils
import emailutils
import json
import random
import os

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def homepage():
    t = mongoutils.getAllTourns()
    allTourns = {}
    for tr in t:
        print tr
        allTourns[tr['name']] = tr['_id']
    rights = ""
    if 'user' not in session:
        rights = "public"
    else:
        user = session['user']
        print user
        print mongoutils.isNotAdmin(user)
        print mongoutils.isNotCoach(user)
        print mongoutils.isNotUser(user)
        if  mongoutils.isNotAdmin(user) and mongoutils.isNotCoach(user):
            rights = "competitor"
        elif mongoutils.isNotAdmin(user):
            rights = "coach"
        else:
            rights = "admin"
    return render_template("alltourns.html",allTourns=allTourns,rights=rights)

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        #print 'a'
        error = ""
        print request.form
        req = {}
        # transfer it otherwise theres a bad request error
        for x in request.form:
            req[x]=request.form[x]
        if req.has_key('login'):
            #print '5'
            user = str(req['user'])
            password = str(req['pass'])
            user_type = str(req['rights'])
            
            if user_type == "admin" and mongoutils.authenticateA(user,password):
                session['user'] = user
                if mongoutils.isValidAdmin(user):
                    return redirect("/admin")
                return redirect("/validate")
            if user_type == "competitor" and mongoutils.authenticateU(user,password):
                session['user'] = user
                if mongoutils.isValidUser(user):
                    return redirect("/competitor")
                return redirect("/validate")
            if user_type == "coach" and mongoutils.authenticateC(user,password):
                session['user'] = user
                if mongoutils.isValidCoach(user):
                    return redirect("/coach")
                return redirect("/validate")
            else:
                error = "Incorrect Username or Password. Try Again."
                return render_template("index.html",error=error)
        if req.has_key('register'):
            user = str(req['reguser'])
            password = str(req['regpass'])
            user_type = str(req['rights'])

            #print '6ducks'
            all_rows = mongoutils.getAll()
            #print all_rows
            for n in range(len(all_rows)):
                all_rows[n] = all_rows[n]['name']
            #print all_rows
            #print '1'
            email = str(req['email'])
            #print '2'
            if user in all_rows:
                #print '3'
                error = "Username already exists. Please try another"
                return render_template("index.html",regerror=error)
            else:
                #print '4'
                message = "Account Created!"
                session['user'] = user
                #print user_type
                #print user_type == "admin"
                emailutils.send_confirmation(user, email)
                if user_type == "admin":
                    mongoutils.addAdmin(user,password,email)
                    return redirect("/validate")
                if user_type == "coach":
                    mongoutils.addCoach(user, password, email)
                    return redirect("/validate")
                else:
                    mongoutils.addUser(user, password, email)
                    return redirect("/validate")
    return render_template("index.html") #login failed

#print mongoutils.getCompTeams('wayez')

@app.route("/competitor", methods = ['GET', 'POST'])
def home_user():
    if 'user' not in session:
        return redirect ("/login")

    user = session['user']
    
    if mongoutils.isNotUser(user):
        if mongoutils.isNotCoach(user):
            return redirect("/admin")
        return redirect("/coach")

    if request.method == 'POST':
        print request.form
        if request.form.has_key('new'):
            #print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            #print request.form
            #print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            tid = mongoutils.getTeamId(request.form['joinTeam'])
            return redirect("/team/" + str(tid))
        if request.form.has_key('old'):
            tid = mongoutils.getTeamId(request.form['old'])
            return redirect("/team/" + str(tid))
        if request.form.has_key('logout'):
            return redirect('/logout')
    teams = mongoutils.getAllTeams()
    allTeams = []
    t = []
    #print teams
    for x in teams:
        #print x
        if user not in mongoutils.getTeamMembers(x['name']):
            allTeams.append(x['name'])
        else:
            t.append(x['name'])
    return render_template("competitor.html", t = t, allTeams = allTeams)

@app.route("/admin", methods = ['GET','POST'])
def admin():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']

    if mongoutils.isNotAdmin(user):
        if mongoutils.isNotCoach(user):
            return redirect("/competitor")
        return redirect("/coach")

    if request.method == 'POST':
        if request.form.has_key('old'):
            #print request.form
            tid = mongoutils.getTournId(request.form['old'])
            return redirect("/bracket/"+str(tid))

    tornus = mongoutils.getAdminTourns(mongoutils.getAdminId(session['user']))

    return render_template("admin.html",tourns=tornus)

@app.route("/validate", methods = ['GET','POST'])
def valid():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    if request.method == "POST":
        if request.form.has_key("validate"):
            code = str(request.form['validate'])
            if mongoutils.is_valid(user, code):
                if not mongoutils.isNotAdmin(user):
                    return redirect("/admin")
                if not mongoutils.isNotCoach(user):
                    return redirect("/coach")
                return redirect("/user")
            else:
                return render_template('validate.html')
    return render_template("validate.html")

@app.route("/coach", methods = ['GET','POST'])
def coach():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']

    if mongoutils.isNotCoach(user):
        if mongoutils.isNotAdmin(user):
            return redirect("/competitor")
        return redirect("/admin")

    if request.method == 'POST':
        #print request.form
        if request.form.has_key('new'):
            return redirect("/newteam")
        if request.form.has_key('old'):
            tid = mongoutils.getTeamId(request.form['old'])
            return redirect("/team/" + str(tid))
        if request.form.has_key('logout'):
            return redirect('/logout')
    teams = mongoutils.getCoachTeams(session['user'])

    return render_template("coach.html",teams=teams)

@app.route("/newtourn", methods = ['GET','POST'])
def new_tourn():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']

    if mongoutils.isNotAdmin(user):
        if mongoutils.isNotCoach(user):
            return redirect("/competitor")
        return redirect("/coach")

    if request.method == 'POST':
        #print request.form
        if request.form.has_key('logout'):
            return redirect('/logout')
        if request.form.has_key('create'):
            name = str(request.form['name'])
            teams = []
            numTeam = 0
            results = [ [[[]]], [], [] ]
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

    if mongoutils.isNotCoach(user):
        if mongoutils.isNotAdmin(user):
            return redirect("/competitor")
        return redirect("/admin")
    
    #print user
    comps = mongoutils.getAllUsers()
    for c in range(len(comps)):
        comps[c] = comps[c]['name']
    if mongoutils.isNotCoach(user):
        if mongoutils.isNotAdmin(user):
            return redirect("/competitor")
        return redirect("/admin")
    if request.method == 'POST':
        #print request.form
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
                if not req['name' + str(numComps)] == 'N/A': 
                    competitors.append(mongoutils.getUserId(req['name' + str(numComps)]))
                numComps += 1
            if mongoutils.createTeam(name, coach, competitors):
                tid = mongoutils.getTeamId(name)
                #return redirect("/bracket/"+str(tid))
                return redirect("/team/" + str(tid))
            else:
                return render_template("newteam.html", comps = comps)
    return render_template("newteam.html", comps = comps)

@app.route("/team/<int:tid>", methods = ['GET','POST'])
def team(tid):
    if 'user' not in session:
        return redirect ("/login")
    
    user = session['user']

    if request.method == 'POST':
        #print request.form
        if request.form.has_key('logout'):
            return redirect('/logout')
        if request.form.has_key('join'):
            mongoutils.joinTeam(tid, mongoutils.getUserId(user))
            return redirect('/competitor')
        if request.form.has_key('accept'):
            req = request.form.copy()
            comps = req.getlist('comps')
            #print "wwwwwwwwwwwwwwwwwwwwwwww"
            for competitor in comps:
                print competitor
                mongoutils.approve(tid, competitor)
            return redirect('/team/' + str(tid) )
        if request.form.has_key('decline'):
            req = request.form.copy()
            comps = req.getlist('comps')
            for competitor in comps:
                #print "reject"
                mongoutils.reject(tid, competitor)
            return redirect('/team/'+ str(tid))
    rights = ""
    if  mongoutils.isNotAdmin(user) and mongoutils.isNotCoach(user):
        rights = "competitor"
    elif not mongoutils.isNotCoach(user) and mongoutils.getCoach(tid) == user:
        rights = "coach"
    name = mongoutils.getTeam(tid)
    members = mongoutils.getTeamMembers(name)
    requests = mongoutils.getTeamRequests(name)
    return render_template("team.html", name = name, members = members, requests = requests, rights = rights)

@app.route("/bracket/<int:tid>", methods = ['GET','POST'])
def bracket(tid):
    #if 'user' not in session:
    #    return redirect ("/login")
    
    if request.method == 'POST':
        if request.form.has_key('logout'):
            return redirect('/logout')

    tjason = {"teams":mongoutils.getTournTeams(tid)}
    rjason = {"results":mongoutils.getTournResults(tid)}
    nom = mongoutils.getTournName(tid)
    
    rights = ""
    if 'user' not in session:
        rights = "public"
    else:
        user = session['user']
        print user
        print mongoutils.isNotAdmin(user)
        print mongoutils.isNotCoach(user)
        print mongoutils.isNotUser(user)
        if  mongoutils.isNotAdmin(user) and mongoutils.isNotCoach(user):
            rights = "competitor"
        elif mongoutils.isNotAdmin(user):
            rights = "coach"
        else:
            rights = "admin"

    return render_template("bracket.html",name=nom,teams=tjason,
                           results=rjason,tid=tid,rights=rights)

@app.route("/logout")
def logout():
    del session['user']
    return redirect("/login")

@app.route("/update", methods = ['GET','POST'])
def updata():
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    #print user

    if mongoutils.isNotAdmin(user):
        if mongoutils.isNotCoach(user):
            return redirect("/competitor")
        return redirect("/coach")
    
    if request.method == 'POST':
        #print request.form
        req = []
        for x in request.form:
            req.append(x)
        #print req
        jason = json.loads(req[0])
        temz = jason['teams']
        results = jason['results']
        tid = jason['tid']
        #print results
        mongoutils.update(tid, results, temz)
        return render_template("index.html")
    return redirect("/admin")

@app.route("/update/<int:tid>", methods = ['GET','POST'])
def update(tid):
    if 'user' not in session:
        return redirect("/login")
    user = session['user']
    #print user

    if mongoutils.isNotAdmin(user):
        if mongoutils.isNotCoach(user):
            return redirect("/competitor")
        return redirect("/coach")
    
    if request.method == 'POST':
        if request.form.has_key('logout'):
            return redirect('/logout')
    tjason = {"teams":mongoutils.getTournTeams(tid)}
    rjason = {"results":mongoutils.getTournResults(tid)}
    nom = mongoutils.getTournName(tid)
    #print "\n\n",rjason,"\n\n"
    return render_template("update.html",name=nom,teams=tjason,
                           results=rjason,tid=tid)

if __name__ == '__main__':
    app.secret_key = "hello"
    app.threaded = True
    #app.debug = True
    app.run(host='0.0.0.0', port=8000)
else:
    app.secret_key = "hello"
    #app.debug = True
