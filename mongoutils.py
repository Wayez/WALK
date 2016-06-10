from pymongo import MongoClient
import pymongo
import hashlib
import simplejson, urllib2

connection = MongoClient()
db = connection['database']
usersc   = db.users
adminsc  = db.admins
tournsc  = db.tourns
teamsc   = db.teams
coachesc = db.coaches
gamesc = db.games

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
#competitor
def authenticateU(username,password):
    result = list(usersc.find({'name':username}))
    for r in result:
        if(encrypt(password) == r['password']):
            return True
    return False

#admin
def authenticateA(username,password):
    result = list(adminsc.find({'name':username}))
    for r in result:
        if(encrypt(password) == r['password']):
            return True
    return False

#coach
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
#competitor
def getUserId(username):
    result = usersc.find_one({'name':username},{'_id':1})
    return result['_id']

#admin
def getAdminId(username):
    result = adminsc.find_one({'name':username},{'_id':1})
    return result['_id']

#coach
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
#competitor
def getUserName(uid):
    result = usersc.find_one({'_id':uid},{'name':1})
    if result != None:
        return result['name']
    else:
        return {'error':'User Not Found'}

#coach
def getCoachName(cid):
    result = coachesc.find_one({'_id':cid},{'name':1})
    if result != None:
        return result['name']
    else:
        return {'error':'User Not Found'}

#admin
def getAdminName(aid):
    result = adminsc.find_one({'_id':aid},{'name':1})
    if result != None:
        return result['name']
    else:
        return {'error':'User Not Found'}

'''
Gets all users that are registered in the database

Args:
    none

Returns:
    list of dictionaries containing each user's info
'''
#competitors
def getAllUsers():
    return list(usersc.find())

def getAllAdmins():
    return list(adminsc.find())

#coaches
def getAllCoaches():
    return list(coachesc.find())

#all
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
#competitor
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

#admin
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

#coach
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

'''
Checks if a username is in the database

Args:
    user: string username

Returns:
    False if the user is in the database
    True otherwise
'''
#competitor
def isNotUser(name):
    users = usersc.find({'name':name},{'_id':0,'name':1})
    redir = True
    for x in users:
        print x
        if x['name'] == name:
            redir = False
    return redir

#admin
def isNotAdmin(name):
    admins = adminsc.find({'name':name},{'_id':0,'name':1})
    redir = True
    for x in admins:
        print x
        if x['name'] == name:
            redir = False
    return redir

#coach
def isNotCoach(name):
    coaches = coachesc.find({'name':name},{'_id':0,'name':1})
    redir = True
    for x in coaches:
        print x
        if x['name'] == name:
            redir = False
    return redir

'''
-------------------------------------------------------------------------------
--------------------------------Tournaments------------------------------------
-------------------------------------------------------------------------------
'''

'''
Creates a new tournament

Args:
    name: string name
    teams: list of team names
    results: list of results
    ida: id of admin owner

Returns:
    True if it was created
    False otherwise
'''
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

'''
Gets id of tournament by admin id

Args:
    ida: int admin id

Returns:
    list of tournaments
'''
def getTourn(ida):
    result = tournsc.find_one({'aid':ida},{'_id':1})
    return result['_id']

'''
Gets id of tournament by name

Args:
    name: string name

Returns:
    id of tournament
'''
def getTournId(name):
    result = tournsc.find_one({'name':name},{'_id':1})
    return result['_id']

'''
Gets list of tournaments associated with an admin

Args:
    ida: int admin id

Returns:
    list of tournaments
'''
def getAdminTourns(ida):
    result = tournsc.find({'aid':ida},{'name':1})
    ret = []
    for r in result:
        ret.append(r['name'])
    return ret

'''
Gets results of tournaments

Args:
    tid: int tournament id

Returns:
    list of results
'''
def getTournResults(tid):
    result = tournsc.find_one({'_id':tid},{'results':1})
    return result['results']

'''
Gets list of tournaments

Args:
    none

Returns:
    list of tournaments
'''
def getAllTourns():
    return list(tournsc.find())

'''
Gets list of teams participating in the tournament

Args:
    tid: int team id

Returns:
    list of teams
'''
def getTournTeams(tid):
    result = tournsc.find_one({'_id':tid},{'teams':1})
    print result
    return result['teams']

'''
Gets name of tournament

Args:
    tid: team id

Returns:
    string name
'''
def getTournName(tid):
    result = tournsc.find_one({'_id':tid},{'name':1})
    return result['name']

'''
Updates results of tournament

Args:
    tid: int team id
    results: list of results

Returns:
    none
'''
def updateResults(tid,results):
    print tournsc.update({'_id':tid},{'$set':{'results':results}})


'''
-------------------------------------------------------------------------------
-----------------------------------Teams---------------------------------------
-------------------------------------------------------------------------------
'''
def getAllTeams():
    return list(teamsc.find())

def getTeam(ida):
    result = teamsc.find_one({'_id':ida})
    #print result
    return result['name']

#print getTeam(1)

def getTeamId(name):
    print name
    result = teamsc.find_one({'name':name})
    print result
    return result['_id']

def getCoachTeams(coach):
    result = teamsc.find({'coach':coach},{'name':1})
    ret = []
    for r in result:
        ret.append(r['name'])
    return ret

def getCompTeams(competitor):
    result = getAllTeams()
    ret = []
    for team in result:
        for comp in team['idus']:
            id = comp['id']
            name = getUserName(id)
            if name == competitor:
                ret.append(team['name'])
    return ret

#print 3
#print getCompTeams('wayez')

def getTeamMembers(name):
    result =  teamsc.find_one({'name':name}, {'idus':1})
    ret = []
    #print result
    for r in result['idus']:
        if r['approved']:
            #print
            #print getUserName(r['id'])
            ret.append(getUserName(r['id']))
    return ret

def getTeamRequests(name):
    result =  teamsc.find_one({'name':name}, {'idus':1})
    ret = []
    #print result
    for r in result['idus']:
        if not r['approved']:
            #print
            #print getUserName(r['id'])
            ret.append(getUserName(r['id']))
    return ret

#print getTeamMembers('WALK')

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

def getCoach(tid):
    result = teamsc.find_one({'_id':tid},{'coach':1})
    return result['coach']

def joinTeam(tid, uid):
    team = getTeam(tid)
    coach = getCoach(tid)
    idus = getTeamMembers(team)
    idus2 = getTeamRequests(team)
    for x in idus2:
        idus.append(x)
    idus.append({'id':uid, 'approved':False })
    teamsc.update({'name':team}, {'_id':tid, 'name':team, 'coach': coach, 'idus': idus})

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
