from pymongo import MongoClient
import pymongo
import hashlib
import simplejson, urllib2

connection = MongoClient()
db = connection['database']
usersc  = db.users
adminsc = db.admins
tournsc = db.tourns

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
def authenticate(username,password):
    result = list(usersc.find({'name':username}))
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

'''
________________________________Changing_______________________________________
'''

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

def getTourn():
    pass

def createTourn():
