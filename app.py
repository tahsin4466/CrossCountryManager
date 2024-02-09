from flask import *
import os
from functools import partial
import datetime
import time
import pymysql.cursors
from random import randint
import face_recognition as fr
import cv2
import face_recognition
import numpy as np
from time import sleep
from pygame import mixer
from markupsafe import Markup
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


app = Flask(__name__)
secret = os.urandom(12)
app.config['SECRET_KEY'] = secret
app.config['MAX_CONTENT-PATH'] = 80
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
Acc = {'email': 'admin@slasmail.com', 'password': 'password'}

@app.route("/", methods=["GET", "POST"])
def main():
    if 'user' in session:
        return redirect('/centrescreen')
    else:
        return redirect('login')

@app.route('/login', methods=["GET", "POST"])
def login():

    f = open("theme.txt", "r")
    theme = (f.read())
    if theme == "dark":
        print("Dark Mode Active")
        textcolour = "white"
        button = "light"
        gradient = "linear-gradient(147deg, #000000 0%, #434343 74%);"
        padlock = "https://www.virinchisoftware.com/images/Bulk-Facial-2-white-icon.png"
        btntext = "Light Mode ☀️"
    else:
        print("Light Mode Active")
        textcolour = "black"
        button = "dark"
        padlock = "https://image.flaticon.com/icons/png/512/1231/1231006.png"
        gradient = "linear-gradient(90deg, rgba(250,250,250,1) 0%, rgba(217,217,217,1) 100%)"
        btntext = "Dark Mode 🌃"

    backgroundvar = str(randint(1,5))
    print(backgroundvar)
    bgurl = str("static/running" + backgroundvar + ".mp4")
    print(bgurl)

    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        
        #check to see that both were not empty
        if not email or not password:
            return redirect('login')

        #check to see they match admin account
        if email == Acc['email'] and password == Acc['password']:
            session['logged_in']= True
            admin = Acc['email']
            session['user'] = admin
            return redirect('/centrescreen')
        else:
            return redirect('/')
        
    return render_template('userlogin.html', bgurl=bgurl, textcolour=textcolour, gradient=gradient, button=button, btntext=btntext, padlock=padlock)

@app.route('/faceID')
def faceID():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
    time.sleep(0.1) 
    mixer.init()
    mixer.music.load("audio/shutter.mp3")
    mixer.music.play()
    return_value, image = camera.read()
    time.sleep(0.1)
    cv2.imwrite("compare.png", image)
    del(camera)

    def get_encoded_faces():
        """
        looks through the faces folder and encodes all
        the faces

        :return: dict of (name, image encoded)
        """
        encoded = {}

        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    face = fr.load_image_file("faces/" + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding

        return encoded


    def unknown_image_encoded(img):
        """
        encode a face given the file name
        """
        face = fr.load_image_file("faces/" + img)
        encoding = fr.face_encodings(face)[0]

        return encoding


    def classify_face(im):
        """
        will find all of the faces in a given image and label
        them if it knows what they are

        :param im: str of file path
        :return: list of face names
        """
        faces = get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        img = cv2.imread(im, 1)

        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
    
        os.remove("compare.png")
        return face_names 

    personname = (classify_face("compare.png"))
    namenum = len(personname)

    if namenum != 0:
        if personname[0] == "Tahsin Ahmed":
            print("Matched")
            session['logged_in']= True
            admin = Acc['email']
            session['user'] = admin
            print('FaceID worked')
            return redirect('/centrescreen')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout')
# this removes all session data, whether logged in as customer or admin
def logout():
    session.pop('user', None)
    session.pop('logged_in', None)
    session.pop('admin', None)
    return redirect('/')

@app.route('/centrescreen', methods=["GET", "POST"])
def centrescreen():
    if 'user' in session:

        f = open("theme.txt", "r")
        theme = (f.read())
        if theme == "dark":
            textcolour = "white"
            button = "light"
            gradient = "linear-gradient(147deg, #000000 0%, #434343 74%);"
            btntext = "Light Mode ☀️"
            printtogle = ""
            stickman = "https://img.pngio.com/hd-running-stick-man-png-white-running-stick-man-free-stick-man-png-white-600_575.png"
        else:
            textcolour = "black"
            button = "dark"
            gradient = "linear-gradient(90deg, rgba(250,250,250,1) 0%, rgba(217,217,217,1) 100%)"
            btntext = "Dark Mode 🌃"
            stickman = "https://cdn.pixabay.com/photo/2014/03/24/17/16/stick-man-295293_1280.png"
            printtogle = "<button class = 'btn btn-dark' onclick='window.print()'><b>Print Report 🖨️</b></button>"

        backgroundvar = randint(1,5)
        print(backgroundvar)
        backgroundvar = str(randint(1,5))
        print(backgroundvar)
        bgurl = str("static/running" + backgroundvar + ".mp4")
        print(bgurl)

        f = open("student.txt", "r")
        runnername = [(f.read())]
        f.close()

        if runnername[0] == "":
            runnerfirst = ""
            runnerlast = ""
            runnerage = ""
            runnergender = ""
            runnerhouse = ""
            runnerid = "" 
            imagename = ""
        else:
            f = open("filename.txt", "r")
            imagename = ("static/" + str(f.read()))
            f.close()
            runnername = (runnername[0].split())
            runnersearch1 = runnername[0]
            runnersearch2 = runnername[1]
            #establish the connection to the database 
            db_connection = pymysql.connect(
                host="35.197.171.137",
                user="20214466",
                passwd="tsnaaoLTHz5gYjXd",
                db="20214466db"
            )
            try:
                with db_connection.cursor() as cursor:
                    #construct the sql query using the variables above
                    sql = "SELECT Student.StudentFirstName, Student.StudentLastName, Student.StudentAge, Student.Gender, House.HouseName,  Student.StudentID FROM Student INNER JOIN House ON Student.HouseID = House.HouseID WHERE Student.StudentFirstName = '" + str(runnersearch1) + "' AND Student.StudentLastName = '" + str(runnersearch2) + "';"
                    #execute the query 
                    cursor.execute(sql)
                    runners = cursor.fetchall() 
                    runnerfirst = [lis[0] for lis in runners]
                    runnerfirst = str(runnerfirst[0])
                    runnerlast = [lis[1] for lis in runners]
                    runnerlast = str(runnerlast[0])
                    runnerage = [lis[2] for lis in runners]
                    runnerage = str(runnerage[0])
                    runnergender = [lis[3] for lis in runners]
                    runnergender = str(runnergender[0])
                    runnerhouse = [lis[4] for lis in runners]
                    runnerhouse = str(runnerhouse[0])
                    runnerid = [lis[5] for lis in runners]
                    runnerid = str(runnerid[0])
            finally:
                db_connection.close()

        #establish the connection to the database 
        db_connection = pymysql.connect(
            host="35.197.171.137",
            user="20214466",
            passwd="tsnaaoLTHz5gYjXd",
            db="20214466db"
        )
        try:
            with db_connection.cursor() as cursor:
                #construct the sql query using the variables above
                sql = "SELECT HousePoints FROM House"
                #execute the query 
                cursor.execute(sql)
                housepoints = cursor.fetchall() 
                housepoints = [lis[0] for lis in housepoints]
                sql = "SELECT HouseName FROM House ORDER BY HousePoints DESC;"
                cursor.execute(sql)
                housewinner = cursor.fetchall()
                print(housewinner)
                housewinner = [lis[0] for lis in housewinner]
                print(housewinner)
                housewinner = str(housewinner[0])
                print(housewinner)
                 #construct the sql query using the variables above
                sql = "SELECT HouseName FROM House"
                #execute the query 
                cursor.execute(sql)
                housenames = cursor.fetchall() 
                housenames = [lis[0] for lis in housenames]

                sql = "SELECT * FROM Event ORDER BY EventDistance ASC;"
                cursor.execute(sql)
                eventdb = cursor.fetchall()

                sql = "SELECT Student.StudentFirstName, Student.StudentLastName, Student.StudentAge, Student.Gender, House.HouseName,  Student.StudentID FROM Student INNER JOIN House ON Student.HouseID = House.HouseID ORDER BY Student.StudentLastName ASC;"
                #execute the query 
                cursor.execute(sql)
                runnerdb = cursor.fetchall() 

        finally:
            #close the database connection
            db_connection.close()
            
        return render_template('centre.html', housepoints=housepoints, housenames=housenames, eventdb=eventdb, bgurl=bgurl, textcolour=textcolour, gradient=gradient, btntext=btntext, button=button, printtogle=printtogle, stickman=stickman, runnerdb=runnerdb, runnerfirst=runnerfirst, runnerlast=runnerlast, runnerage=runnerage, runnergender=runnergender, runnerhouse=runnerhouse, runnerid=runnerid, imagename=imagename, housewinner=housewinner)
    else:
        return redirect('/')

@app.route('/PointUpdate', methods=["GET", "POST"]) 
def PointUpdate():

    if request.method == "POST":
        points = str(request.form['points'])
        house = str(request.form['house'])

        db_connection = pymysql.connect(
            host="35.197.171.137",
            user="20214466",
            passwd="tsnaaoLTHz5gYjXd",
            db="20214466db"
        )
        try:
            with db_connection.cursor() as cursor:
                #execute the query
                sql = "UPDATE House SET HousePoints = " + str(points) + " WHERE HouseName = '" + str(house) + "';"
                cursor.execute(sql)
                #save the entries into the database
                db_connection.commit()
       
        finally:
            #close the database connection
            db_connection.close()


    if 'user' in session:
        return redirect('/centrescreen')
    else:
        return redirect('/')

@app.route('/EventUpdate', methods=["GET", "POST"])
def EventUpdate():

    if request.method == "POST":
        eventname = str(request.form['eventname'])
        eventlength = str(request.form['eventlength'])
        eventid = str(request.form['eventid'])

        db_connection = pymysql.connect(
            host="35.197.171.137",
            user="20214466",
            passwd="tsnaaoLTHz5gYjXd",
            db="20214466db"
        )
        try:
            with db_connection.cursor() as cursor:
                #execute the query
                sql = "UPDATE Event SET EventName = '" + str(eventname) + "', EventDistance = " + str(eventlength) + " WHERE EventID = " + str(eventid) + ";"
                cursor.execute(sql)
                #save the entries into the database
                db_connection.commit()

        finally:
            #close the database connection
            db_connection.close()

    if 'user' in session:
        return redirect('/centrescreen')
    else:
        return redirect('/')

@app.route('/NewEvent', methods=["GET", "POST"])
def NewEvent():

    if request.method == "POST":
        neweventname = str(request.form['neweventname'])
        neweventlength = str(request.form['neweventlength'])

        db_connection = pymysql.connect(
            host="35.197.171.137",
            user="20214466",
            passwd="tsnaaoLTHz5gYjXd",
            db="20214466db"
        )
        try:
            with db_connection.cursor() as cursor:
                #execute the query
                sql = "INSERT INTO Event(EventName, EventDistance) VALUES ('" + str(neweventname) + "'," + str(neweventlength) + ");"
                cursor.execute(sql)
                #save the entries into the database
                db_connection.commit()

        finally:
            #close the database connection
            db_connection.close()

    if 'user' in session:
        return redirect('/centrescreen')
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):

    #connects to the database
    db_connection = pymysql.connect(
        host="35.197.171.137",
        user="20214466",
        passwd="tsnaaoLTHz5gYjXd",
        db="20214466db"
    )
    try:
        with db_connection.cursor() as cursor:
            #execute the query
            sql = "DELETE FROM Event WHERE EventID=" + str(id) + ";"
            cursor.execute(sql)
            #save the entries into the database
            db_connection.commit()

    finally:
        #close the database connection
        db_connection.close()

    if 'user' in session:
        return redirect('/centrescreen')
    else:
        return redirect('/')

@app.route('/theme')
def theme():

    f = open("theme.txt", "r")
    theme = (f.read())
    f = open("theme.txt", "w")
    if theme == "dark":
        f.write("light")
        theme = "light"
    else:
        f.write("dark")
        theme = "dark"
    f.close()

    if 'user' in session:
        return redirect('/centrescreen')
    else:
        return redirect('/')

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    
    f = open("filename.txt", "r")
    deletepath = str(f.read())
    f.close()
    if deletepath == "":
        pass
    else:
        os.remove("static/" + deletepath)
    
    if request.method == 'POST':
        f = request.files['File']
        filename = f.filename
        f.save(os.path.join('static', secure_filename(f.filename)))
        

    def get_encoded_faces():
        """
        looks through the faces folder and encodes all
        the faces

        :return: dict of (name, image encoded)
        """
        encoded = {}

        for dirpath, dnames, fnames in os.walk("./students"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    face = fr.load_image_file("students/" + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding
        return encoded


    def unknown_image_encoded(img):
        """
        encode a face given the file name
        """
        face = fr.load_image_file("students/" + img)
        encoding = fr.face_encodings(face)[0]
        return encoding


    def classify_face(im):
        """
        will find all of the faces in a given image and label
        them if it knows what they are

        :param im: str of file path
        :return: list of face names
        """
        faces = get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        img = cv2.imread(im, 1)

        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
        return face_names 
        
    personname = (classify_face("static/" + filename))
    if personname[0] != "Unknown":
        f = open("student.txt", "w")
        f.write(personname[0])
        f.close()
        f = open("filename.txt", "w")
        f.write(filename)
        f.close()
    else:
        f = open("student.txt", "w")
        f.write("")
        f.close()
        f = open("filename.txt", "w")
        f.write("")
        f.close()
        os.remove("static/" + filename)
        
    if 'user' in session:
        return redirect('/centrescreen')
    else:
        return redirect('/')


app.run(host='0.0.0.0', debug=True)