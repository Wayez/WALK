from flask import Flask, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
import mongoutils
import json
import random

def loginHelper(req):
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
            else:
                mongoutils.addUser(user, password, email)
                return redirect("/competitor")
    return render_template("index.html") #login failed