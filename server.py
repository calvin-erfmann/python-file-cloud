import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
import random
import datetime
from flask import Flask, session
from flask_session import Session
import time
import json
import hashlib


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_url_path='/static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

app.secret_key = 'wdahfuhfjsdhjfhsdhfhsjdhfhdsfhsdhjfhjhfjdhjfhj'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = "spaffel-cloud-cookie"
app.config['SECRET_KEY'] = os.urandom(24)



def adduser(name, password):
    with open("users.json") as fp:
        users = json.load(fp)
    fp.close()
    id = random.randint(0,99999999999)
    if id in users:
        id = random.randint(0,99999999999)
    h = hashlib.md5(password.encode())
    users[id] = str(h.hexdigest())
    with open("idsandnames.json") as fp:
        userids = json.load(fp)
    fp.close()
    if name in userids:
        return "already"
    with open("users.json", "w") as write_file:
        json.dump(users, write_file)
    fp.close()
    setusergroup(name, "default")
    
    userids[str(name)] = id

    with open("idsandnames.json", "w") as write_file:
        json.dump(userids, write_file)
    fp.close()

def checkaccount(name, password):
    with open("idsandnames.json") as fp:
        userids = json.load(fp)
    fp.close()
    id = userids[str(name)]
    with open("users.json") as fp:
        users = json.load(fp)
    fp.close()
    hashedpass = users[str(id)]
    h = hashlib.md5(password.encode())
    if str(hashedpass) == str(h.hexdigest()):
        
        return "yes"
    else:
        print(hashedpass)
        print(hash(password))
        return "no"

def setusergroup(name, groupname):
    with open("groups.json") as fp:
        groups = json.load(fp)
    fp.close()
    groups[str(name)] = str(groupname)
    with open("groups.json", "w") as write_file:
        json.dump(groups, write_file)
    fp.close()

def getusergroup(name):
    with open("groups.json") as fp:
        groups = json.load(fp)
    return group[str(name)]

    



#adduser("david1", "kolinshki")
#print(checkaccount("david1", "kolinshki"))





    
    



