import os
import flask
from flask import Flask, flash, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
import random
import datetime
from flask import Flask, session
from flask_session import Session
import time
import json
import hashlib
from os import listdir
from os.path import isfile, join
import pathlib
import shutil


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


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    
    print(filename)
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    path = f'{uploads}{filename}'
    return send_from_directory(directory=uploads, filename=filename, path = path)

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        
        form_data = request.form
        

        wert = adduser(form_data['username'], form_data['passwort'])
        
        if wert == "already":
            return '''
    <!doctype html>
    <title>New User</title>
    <h1>Create New User</h1>
    <a>Username already in use</a>
    <form method=post enctype=multipart/form-data>
     <p>Username: <input type = "text" name = "username" />
    <p>Password: <input type = "text" name = "passwort" />      
        <p>Group :<input type="text" value="default" name = "group">
        |   <input type=submit value=Create></p>
    '''
        else:
            setusergroup(form_data['username'], form_data['group'])
            uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
            newpath = f"{uploads}/private/{form_data['username']}/{form_data['username']}"
            if not os.path.exists(newpath):
              os.makedirs(newpath)

        return redirect('/')
            

    return '''
    <!doctype html>
    <title>New User</title>
    <h1>Create New User</h1>
    <form method=post enctype=multipart/form-data>
    <p>Username: <input type = "text" name = "username" />
    
        <p>Password: <input type = "text" name = "passwort" />      
        <p>Group: <input type="text" value="default" name = "group">
        |   <input type=submit value=Create></p>
    

    </form>
    '''

@app.route('/', methods=['GET', 'POST'])
def startpage():
    if request.method == 'POST':
        
        form_data = request.form
        
        
        wert = checkaccount(form_data['username'], form_data['passwort'])
        
        if wert == "no":
            return '''
    <!doctype html>
    <title>Login</title>
    <h1>Login</h1>
    <a>Password is Wrong</a>
    <form method=post enctype=multipart/form-data>
     <p>Username: <input type = "text" name = "username" />
    <p>Password: <input type = "text" name = "passwort" />      

        |   <input type=submit value=Create></p>
    '''
        else:
            
            session['username'] = form_data['username']
            session['user'] = form_data['username']
            session['log'] = "yes"
        
            return redirect('/startpage')
            

    return '''
    <!doctype html>
    <title>Login</title>
    <h1>Login</h1>
    <form method=post enctype=multipart/form-data>
    <p>Username: <input type = "text" name = "username" />
    
        <p>Password: <input type = "text" name = "passwort" />
        |   <input type=submit value=Create></p>
    

    </form>
    '''


def listdirs(folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

def get_filepaths(mypath):
    return([f for f in listdir(mypath) if isfile(join(mypath, f))])

@app.route('/priv/<path:path1>', methods=['GET', 'POST'])
def newprivate(path1):
    if not 'log' in session:
      return redirect('/')
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    path = f"{uploads}/private/{session['user']}/{path1}"
    path2 = f"uploads/private/{session['user']}/{path1}"
    print(path)

    ordner = listdirs(path)
    datein = get_filepaths(path)

    seite = """
    <style>
    *{box-sizing:border-box;}

body{
  font-family:source sans pro;
}
h3{
  font-weight:400;
  font-size:16px;
}
p{
  font-size:12px;
  color:#888;
}
a.fill-div {
    display: block;
    height: 100%;
    width: 100%;
    text-decoration: none;
}
.stage{
  max-width:80%;margin:60px 10%;
  position:relative;  
}
.folder-wrap{
  display: flex;
  flex-wrap:wrap;
}
.folder-wrap::before{
  
  display: block;
  position: absolute;
  top:-40px;
}
.folder-wrap:first-child::before{
  display: block;
  position: absolute;
  top:-40px;
}
.tile{
    border-radius: 3px;
    width: calc(20% - 17px);
    margin-bottom: 23px;
    text-align: center;
    border: 1px solid #eeeeee;
    transition: 0.2s all cubic-bezier(0.4, 0.0, 0.2, 1);
    position: relative;
    padding: 35px 16px 25px;
    margin-right: 17px;
    cursor: pointer;
}
.tile:hover{
  box-shadow: 0px 7px 5px -6px rgba(0, 0, 0, 0.12);
}
.tile i{
    color: #00A8FF;
    height: 55px;
    margin-bottom: 20px;
    font-size: 55px;
    display: block;
    line-height: 54px;
    cursor: pointer;
}
.tile i.mdi-file-document{
  color:#8fd9ff;
}

.back{
  font-size: 26px;
  border-radius: 50px;
  background: #00a8ff;
  border: 0;
  color: white;
  width: 60px;
  height: 60px;
  margin: 20px 20px 0;
  outline:none;
  cursor:pointer;
}

/* Transitioning */
.folder-wrap{
  position: absolute;
  width: 100%;
  transition: .365s all cubic-bezier(.4,0,.2,1);
  pointer-events: none;
  opacity: 0;
  top: 0;
}
.folder-wrap.level-up{
  transform: scale(1.2);
    
}
.folder-wrap.level-current{
  transform: scale(1);
  pointer-events:all;
  opacity:1;
  position:relative;
  height: auto;
  overflow: visible;
}
.folder-wrap.level-down{
  transform: scale(0.8);  
}

.button7 {


     
                    display: inline-block;
                    outline: none;
                    cursor: pointer;
                    border-radius: 3px;
                    font-size: 14px;
                    font-weight: 500;
                    line-height: 16px;
                    padding: 2px 16px;
                    height: 38px;
                    min-width: 96px;
                    min-height: 38px;
                    border: none;
                    color: #fff;
                    position:absolute;
                    top:1;
                    right:30px;
                    vertical-align: middle;
                    background-color: rgb(88, 101, 242);
                    transition: background-color .17s ease,color .17s ease;
                    :hover {
                        background-color: rgb(71, 82, 196);
                    }
                    
    
                
   }

.button8 {


     
                    display: inline-block;
                    outline: none;
                    cursor: pointer;
                    border-radius: 3px;
                    font-size: 14px;
                    font-weight: 500;
                    line-height: 16px;
                    padding: 2px 16px;
                    height: 38px;
                    min-width: 96px;
                    min-height: 38px;
                    border: none;
                    color: #fff;
                    position:absolute;
                    top:1;
                    right:190px;
                    vertical-align: middle;
                    background-color: rgb(88, 101, 242);
                    transition: background-color .17s ease,color .17s ease;
                    :hover {
                        background-color: rgb(71, 82, 196);
                    }
                    
    
                
   }


.button9 {


     
                    display: inline-block;
                    outline: none;
                    cursor: pointer;
                    border-radius: 3px;
                    font-size: 14px;
                    font-weight: 500;
                    line-height: 16px;
                    padding: 2px 16px;
                    height: 38px;
                    min-width: 96px;
                    min-height: 38px;
                    border: none;
                    color: #fff;
                    position:absolute;
                    top:2;
                    left:40px;
                    vertical-align: middle;
                    background-color: rgb(88, 101, 242);
                    transition: background-color .17s ease,color .17s ease;
                    :hover {
                        background-color: rgb(71, 82, 196);
                    }
                    
    
                
   }



</style>

  
  
 


    """


    seite += '<input type="button" class="button7" onclick="window.location.href = '
    seite += f"'http://{flask.request.host}/newuploadprivat/{path2}'"
    seite += f';" value="Upload File" />'


    seite += '<input type="button" class="button8" onclick="window.location.href = '
    seite += f"'http://{flask.request.host}/neuerordner/{path2}'"
    seite += f';" value="New Folder" />'


    path = pathlib.Path(path1)
    ober = path.parent


    

    seite += '<input type="button" class="button9" onclick="window.location.href = '
    if path1 == session['user'] or path1 == f"{session['user']}/":
      seite += f"'http://{flask.request.host}/startpage'"
    else:
      seite += f"'http://{flask.request.host}/priv/{ober}'"
    seite += f';" value="<--Back" />'


    path = f"{uploads}/private/{session['user']}/{path1}"

    seite += """

     <div class="stage">
    
    <div class="folder-wrap level-current scrolling">

    """

    for ordner in ordner:
      seite += f'<div class="tile folder" onclick="location.href='
      seite += f"'http://{flask.request.host}/priv/{path1}/{ordner}';"
      seite += f'">'
      seite += f'<i class="mdi mdi-folder"></i><img src="http://spaffel.de/uploads/Sonstiges/9457267491658betterfolder.png" height="70">'
      seite += f'<h3>{ordner}</h3>'
      seite += '<p>    </p></div><!-- .tile.folder -->'

    for datei in datein:
      seite += f'<div class="tile form" onclick="location.href='
      seite += f"'http://{flask.request.host}/{path2}/{datei}';"
      seite += f'">'
      if '.docx' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/2714680531560Google_Docs_logo_2014-2020.svg.png" height="70">'
      elif '.doc' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/2714680531560Google_Docs_logo_2014-2020.svg.png" height="70">'
      elif '.odt' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/2714680531560Google_Docs_logo_2014-2020.svg.png" height="70">'
      elif '.odf' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/2714680531560Google_Docs_logo_2014-2020.svg.png" height="70">'
      elif '.pdf' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/4054768518186pdf.png" height="75">'
      elif '.zip' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/9068193777637zip.png" height="75">'
      elif '.7z' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/9068193777637zip.png" height="75">'
      elif '.7z' in datei:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/9068193777637zip.png" height="75">'
      else:
        imagehtml = '<img src="http://spaffel.de/uploads/Sonstiges/508972341814file.png" height="80">'

      seite += imagehtml
      seite += f'<h3>{datei}</h3>'
      seite += '<p>    </p></div><!-- .tile.folder -->'
      
    
    
    return seite

@app.route('/newuploadprivat/<path:path1>', methods=['GET', 'POST'])
def newupload_privatfile(path1):
    
    if not 'log' in session:
        return redirect('/')
    if session['log'] == 'yes':
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                form_data = request.form
                filename = secure_filename(file.filename)
                dateipfad = f"{path1}/{filename}"
                file.save(os.path.join(dateipfad))
            print(path1)
            remove = f'uploads/private/{session["user"]}/' 
            path1 = path1.replace(remove, '')
                        
                
            return redirect(f'/priv/{path1}/')
                

        bilder = ['http://cloud.spaffel.de/s/61648','http://cloud.spaffel.de/s/70961','http://cloud.spaffel.de/s/43823','http://cloud.spaffel.de/s/54910','http://cloud.spaffel.de/s/15743','http://cloud.spaffel.de/s/86145','http://cloud.spaffel.de/s/57242','http://cloud.spaffel.de/s/95847','http://cloud.spaffel.de/s/54606','http://cloud.spaffel.de/s/49015','http://cloud.spaffel.de/uploads/Sonstiges/8303446944419ybl7h8xjdsl81.webp','http://cloud.spaffel.de/uploads/Datenbanken/6415563826150rqkw9hupklm81.webp','http://cloud.spaffel.de/uploads/Datenbanken/508764086821p5krx8s4ybl81.webp','http://cloud.spaffel.de/uploads/Datenbanken/5722891565723j3zyas6hwdn81.webp','http://cloud.spaffel.de/uploads/Datenbanken/9809891929942dmy1bxggn8m81.webp','http://cloud.spaffel.de/uploads/Datenbanken/1043666397135b17mancuhpn81.webp','http://cloud.spaffel.de/uploads/Datenbanken/2140991528796459omspyhlm81.webp',
    'http://cloud.spaffel.de/uploads/Datenbanken/32484574417671j8lpkau3xl81.webp','http://cloud.spaffel.de/uploads/Datenbanken/9286426486532spaexu6y98l81.webp','http://cloud.spaffel.de/uploads/Datenbanken/6373717700644w9l0ul7y98l81.webp','http://cloud.spaffel.de/uploads/Datenbanken/1423269031125ve2a3c7y98l81.webp',
    'http://cloud.spaffel.de/uploads/Datenbanken/40949221654976grt1ew82jk81.webp','http://cloud.spaffel.de/uploads/Datenbanken/188095855317wb6aimw48pk81.webp']
        hintergrundurl = random.choice(bilder)
        
        return1 = '''
        <!doctype html>

        <title>Upload</title>
        
        <form method=post enctype=multipart/form-data>
<center>
<h1>Upload</h1>
<style>
body {
'''
        return2 = f"background-image: url('{hintergrundurl}');"

  




        return3 = """
}

.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
.button {
  min-width: 300px;
  min-height: 60px;
  font-family: 'Nunito', sans-serif;
  font-size: 22px;
  text-transform: uppercase;
  letter-spacing: 1.3px;
  font-weight: 700;
  color: #313133;
  background: #4FD1C5;
background: linear-gradient(90deg, rgba(129,230,217,1) 0%, rgba(79,209,197,1) 100%);
  border: none;
  border-radius: 1000px;
  box-shadow: 12px 12px 24px rgba(79,209,197,.64);
  transition: all 0.3s ease-in-out 0s;
  cursor: pointer;
  outline: none;
  position: relative;
  padding: 10px;
  }

button::before {
content: '';
  border-radius: 1000px;
  min-width: calc(300px + 12px);
  min-height: calc(60px + 12px);
  border: 6px solid #00FFCB;
  box-shadow: 0 0 60px rgba(0,255,203,.64);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: all .3s ease-in-out 0s;
}

.button:hover, .button:focus {
  color: #313133;
  transform: translateY(-6px);
}

button:hover::before, button:focus::before {
  opacity: 1;
}

button::after {
  content: '';
  width: 30px; height: 30px;
  border-radius: 100%;
  border: 6px solid #00FFCB;
  position: absolute;
  z-index: -1;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: ring 1.5s infinite;
}

button:hover::after, button:focus::after {
  animation: none;
  display: none;
}

@keyframes ring {
  0% {
    width: 30px;
    height: 30px;
    opacity: 1;
  }
  100% {
    width: 300px;
    height: 300px;
    opacity: 0;
  }
}


.upload-container {
    position: relative;
}




.upload-container input {
    border: 1px solid #92b0b3;
    background-color: rgba(255, 255, 255, 0.5);
    outline: 2px dashed #92b0b3;
    outline-offset: -10px;
    padding: 100px 150px 100px 150px;
    text-align: center !important;
    width: 500px;
}
 
.upload-container input:hover {
    background: #ddd;
}
 
.upload-container:before {
    text-align: center;
    position: absolute;
    bottom: 50px;
    left: 245px;
    color: #3f8188;
    font-weight: 900;
}
 
.upload-btn {
    margin-left: 300px;
    padding: 20px 20px;
}

input[type=text] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}
input[type=text]:focus {
  border: 3px solid #555;
}
.upload-sel  {
    border: 1px solid #92b0b3;
    background-color: rgba(0, 0, 0, 0.5);
    outline:  #92b0b3;
    outline-offset: -10px;
    padding: 10px 25px 10px 25px;
    text-align: center !important;
    width: 500px;
    padding: 100px 150px 100px 150px;
    text-align: center;
    
}
select {
  width: 100%;
  padding: 16px 20px;
  border: none;
  border-radius: 4px;
  background-color: #f1f1f1;
}
input[type=button], input[type=submit], input[type=reset] {
  background-color: #04AA6D;
  border: none;
  color: white;
  padding: 16px 32px;
  text-decoration: none;
  margin: 4px 2px;
  cursor: pointer;
}



input[type=text]{
    width:100%;
    border:2px solid #aaa;
    border-radius:5px;
    margin:3px 0;
    outline:none;
    padding:8px;
    box-sizing:border-box;
    transition:.3s;
  }

input[type=time]{
    font-size:18px;
    color:hsla(207, 100%, 50%, 1);
    width:50%;
    border:2px solid #ccc;
    border-radius:5px;
    margin:3px 0;
    outline:none;
    padding:8px;
    box-sizing:border-box;
    transition:.3s;
  }
  
  input[type=text]:focus,input[type=time]:focus{
    border-color:dodgerBlue;
    box-shadow:0 0 3px 0 dodgerBlue;
  }

body{
  background-color:#f1f1f1;
  font-family: Arial, Helvetica, sans-serif;
}

.conteudo{
  background-color:#e1e1e1;
  margin: 0 auto;
  padding: 1.5em;
  max-width:400px;
  height: auto;
  border: none;
  border-radius: 5px;
  -webkit-box-shadow: 2px 1px 1px #757575;
  -moz-box-shadow: 2px 1px 1px #757575;
  box-shadow: 0px 1px 1px #757575;
}



.navbar {
  overflow: hidden;
  background-color: #333;
}

.navbar a {
  float: left;
  font-size: 16px;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

.dropdown {
  float: left;
  overflow: hidden;
}

.dropdown .dropbtn {
  font-size: 16px;
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.navbar a:hover, .dropdown:hover .dropbtn {
  background-color: red;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.dropdown:hover .dropdown-content {
  display: block;
}


</style>
<script>
function myFunction() {
  var x = document.getElementById("mySelect").value;
  document.getElementById("demo").innerHTML = "You selected: " + x;
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}
</script>
<script>
             
    function uploadFiles() {
        var files = document.getElementById('file_upload').files;
        if(files.length==0){
            alert("Please select a file...");
            return;
        }
        var filenames="";
        for(var i=0;i<files.length;i++){
            filenames+=files[i].name+"\n";
        }
        alert("Selected file(s) :\n____________________\n"+filenames);
    }
            
</script>

<div class="border">
    <div class="upload-container">

        <div id="div1" ondrop="drop(event)" ondragover="allowDrop(event)"></div>

  	<center>
      
        <input type=file name=file draggable="true" ondragstart="drag(event)" >
        
        
	</center>
        </div>

    </div>
	       <div class="wrap"></p><p><input type=submit class="button" value=Upload></p></div>
    </div>

        </form>
</div>
</center>
"""

    return f'{return1}{return2}{return3}'



@app.route('/neuerordner/<path:path1>', methods=['GET', 'POST'])
def newfolder(path1):
  if not 'log' in session:
        return redirect('/')
  
  if session['log'] == 'yes':
      if request.method == 'POST':
          
          form_data = request.form
          
          
                  
          newpath = f"{path1}/{form_data['Name']}"
          if not os.path.exists(newpath):
            os.makedirs(newpath) 
          
          remove = f'uploads/private/{session["user"]}/' 
          path1 = path1.replace(remove, '')
                      
              
          return redirect(f'http://{flask.request.host}/priv/{path1}/{form_data["Name"]}/')
              

      return '''
      <!doctype html>
      <title>New Folder</title>
      <h1>New Folder</h1>
      <form method=post enctype=multipart/form-data>
      <p>Ordner Name: <input type = "text" name = "Name" />
      
              |   <input type=submit value=Create></p>
      

      </form>
      '''
    



    
    



app.run(host='0.0.0.0', port='25578')