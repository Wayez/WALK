# WALK
Softdev 2 Final Project

###About
Science Bowl tournament management system

####Collaborators
|      **Member**     |               **Github**                    |
|---------------------|---------------------------------------------|
|Wayez Chowdhury      | [`Wayez`](https://github.com/wayez)         |
|Liam Daly            | [`ldalynyc`](https://github.com/ldalynyc)   |
|Katherine Gershfeld  | [`kagers`](https://github.com/kagers)       | 
|Alexander Sosnovsky  | [`atrp--`](https://github.com/atrp--)       |

####Installing / Running


First, clone the repository using the following command:

```
$ git clone https://github.com/Wayez/WALK.git
```
<br>

This project required Python 2.7 to run. If that isn't installed, use this helpful [tutorial](http://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/#) to download, install, and configure Python.
<br>

This project requires mongoDB to run. if that isn't installed, use this helpful [tutorial](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) to download, install, and configure mongoDB. 
<br>

This project requires several python libraries. To install them, run the following commands:

```
$ pip install flask
$ pip install pymongo
$ pip install simplejson
```
<br>

The first time you are installing this project, run the following command to set up databases:

```
$ python mongoutils.py
```
<br>

To run this site:
```
$ python app.py
```

####Development Log
This is only a log of key goals, click this [link](https://github.com/Wayez/WALK/blob/master/devlog.txt) for a full development log.

05-17-2016
  Implemented Bracket View of Tournaments
  
05-22-2016
  Completed login system for administrators and competitors
  
05-25-2016
  Admins able to create tournaments
  
05-31-2016
  Implemented coaches
  
06-07-2016
  Tournaments can now be updated.
  



####Features
Three user types with varying privelages 
Admins:
- Create double-elimination tournaments of up to 16 teams that do not have to be registered.
- Update the teams that are participating as well as the scores in each of their tournaments.
- Remove flags on tournament (To be implemented).

Coaches:
- Create teams of registered competitors.
- Approve or deny requests by competitors to join their teams.
- Update scores of tournaments that their team is participating in.
- Flag the scores of tournaments that their team is participating in (To be implemented).

Competitor:
- Request to join teams.
- Get alerts on where a game they will be participating in is being held (To be implemented).

Non-Users:
- Spectate tournament brackets.


####Bugs
- Plus/Minus and SE/DE should not appear in update bracket
- Nav bar logo disappears sometimes
- Admins cannot change team names on update bracket page.

####Credits
[JQuery Brackets](https://github.com/teijo/jquery-bracket)
