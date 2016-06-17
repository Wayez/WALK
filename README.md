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


This project required Python 2.7 to run. If that isn't installed, use this helpful [tutorial](http://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/#) to download, install, and configure Python.


This project requires mongoDB to run. if that isn't installed, use this helpful [tutorial](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) to download, install, and configure mongoDB. 


This project requires several python libraries. To install them, run the following commands:

```
$ pip install flask
$ pip install pymongo
$ pip install simplejson
```
The first time you are installing this project, run the following command to set up databases:

```
$ python mongoutils.py
```

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
-  

####Bugs
- Plus/Minus and SE/DE should not appear in update bracket
- Nav bar logo disappears sometimes
- Probably a lot more

####Credits
[JQuery Brackets](https://github.com/teijo/jquery-bracket)
