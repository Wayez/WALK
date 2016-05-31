from pymongo import MongoClient
import pymongo
import hashlib
import simplejson, urllib2

connection = MongoClient()
db = connection['database']
usersc  = db.users
adminsc = db.admins
tournsc = db.tourns
teamsc  = db.teams 

'''
-------------------------------------------------------------------------------
--------------------------------Users------------------------------------------
-------------------------------------------------------------------------------
'''

'''
________________________________Login__________________________________________
'''

'''
Checks whether the username and password match a registered user 
 
Args:
    username: username to be checked
    password: password to be checked    
    
Returns:
    True if both match
    False otherwise
'''
def authenticateU(username,password):
    result = list(usersc.find({'name':username}))
    for r in result:
        if(encrypt(password) == r['password']):
            return True
    return False

def authenticateA(username,password):
    result = list(adminsc.find({'name':username}))
    for r in result:
        if(encrypt(password) == r['password']):
            return True
    return False

def authenticateC(username,password):
    result = list(coachesc.find({'name':username}))
    for r in result:
        if(encrypt(password) == r['password']):
            return True
    return False
    
'''
Gets the id that corresponds to a username

Args:
    username: username
    
Returns:
    corresponding user id
'''
def getUserId(username):
    result = usersc.find_one({'name':username},{'_id':1})
    return result['_id']

def getAdminId(username):
    result = adminsc.find_one({'name':username},{'_id':1})
    return result['_id']

def getCoachId(username):
    result = coachesc.find_one({'name':username},{'_id':1})
    return result['_id']

'''
Gets the username that corresponds to a user id

Args:
    uid: user id 
    
Returns:
    corresponding username
'''
def getUserName(uid):
    result = usersc.find_one({'_id':uid},{'name':1})
    if result != None:
        return result
    else:
        return {'error':'User Not Found'}

'''
Gets all users that are registered in the database

Args:
    none
    
Returns:
    list of dictionaries containing each user's info
''' 
def getAllUsers():
    return list(usersc.find())

def getAllAdmins():
    return list(adminsc.find())

def getAllCoaches():
    return list(coachesc.find())

def getAll():
	return getAllAdmins() + getAllUsers() + getAllCoaches()

'''
Registers a user into the database

Args:
    username: string username
    password: string password
    email: string email
    
Returns:
    True if the registration was successful
    False otherwise
'''
def addUser(username,password,email):
    if usersc.find_one({'name':username}) == None:
        us = getAllUsers()
        if len(us)==0:
            idu = 1
        else:
            n = usersc.find_one(sort=[('_id',-1)])
            idu = int(n['_id'])+1    
        password = encrypt(password)
        r = {'_id':idu, 'name':username, 'password':password, 'email':email}
        usersc.insert(r)
        return True
    return False

def addAdmin(username,password,email):
    if adminsc.find_one({'name':username}) == None:
        us = getAllAdmins()
        if len(us)==0:
            ida = 1
        else:
            n = adminsc.find_one(sort=[('_id',-1)])
            ida = int(n['_id'])+1    
        password = encrypt(password)
        r = {'_id':ida, 'name':username, 'password':password, 'email':email}
        adminsc.insert(r)
        return True
    return False

def addCoach(username, password, email):
    if coachesc.find_one({'name':username}) == None:
        us = getAllCoaches()
        if len(us)==0:
            idc = 1
        else:
            n = coachesc.find_one(sort=[('_id',-1)])
            idc = int(n['_id'])+1    
        password = encrypt(password)
        r = {'_id':idc, 'name':username, 'password':password, 'email':email}
        coachesc.insert(r)
        return True
    return False
    

def isNotAdmin(name):
    #print adminsc.find({'name':name},{'_id':0,'name':1})
    admins = adminsc.find({'name':name},{'_id':0,'name':1})
    redir = True
    for x in admins:
        print x
        if x['name'] == name:
            redir = False
    return redir

def isNotCoach(name):
    #print adminsc.find({'name':name},{'_id':0,'name':1})
    coaches = coachesc.find({'name':name},{'_id':0,'name':1})
    redir = True
    for x in coaches:
        print x
        if x['name'] == name:
            redir = False
    return redir



                
'''
-------------------------------------------------------------------------------
--------------------------------Miscellaneous----------------------------------
-------------------------------------------------------------------------------
'''

'''
Encrypts a password using the hashlib library for python

Args:
    word: string to be encrypted

Returns:
    encrypted string
'''
def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()


'''
-------------------------------------------------------------------------------
--------------------------------Tournaments------------------------------------
-------------------------------------------------------------------------------
'''

def getTourn(ida):
    result = tournsc.find_one({'aid':ida},{'_id':1})
    return result['_id']

def getAllTourns():
    return list(tournsc.find())

def createTourn(name, teams, results, ida):
    print tournsc.find_one({'name':name})
    if tournsc.find_one({'name':name}) == None:
        ts = getAllTourns()
        if len(ts)==0:
            idt = 1
        else:
            n = tournsc.find_one(sort=[('_id',-1)])
            idt = int(n['_id'])+1
        r = {'_id':idt, 'name':name, 'teams':teams,
             'aid':ida, 'results':results}
        tournsc.insert(r)
        return True
    return False

def getTournTeams(tid):
    result = tournsc.find_one({'_id':tid},{'teams':1})
    return result['teams']

def getTournName(tid):
    result = tournsc.find_one({'_id':tid},{'name':1})
    return result['name']

'''
-------------------------------------------------------------------------------
-----------------------------------Teams---------------------------------------
-------------------------------------------------------------------------------
'''

def getAllTeams():
    return list(teamsc.find())

def createTeam(name, coach, idus):
    print teamsc.find_one({'name':name})
    if teamsc.find_one({'name':name}) == None:
        ts = getAllTeams()
        if len(ts)==0:
            idt = 1
        else:
            n = teamsc.find_one(sort=[('_id',-1)])
            idt = int(n['_id'])+1
        r = {'_id':idt, 'name':name, 'coach':coach,
             'idus':idus}
        teamsc.insert(r)
        return True
    return False



