import os
from datetime import date
from flask import Flask, render_template, request, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from peewee import *
from controller.dateLogic import getTodayDifference

app = Flask(__name__)
currentUser = None
@app.route("/")
def welcomePage():
    return render_template("index.html")

@app.route("/loginPage", methods=['GET', 'POST'])
def logInPage():
    if request.method == 'POST':
        login = request.form
        try:
            Userlogin = User.select().where(User.email == login.get('email'), User.password == login.get('password')).get()
            global currentUser
            currentUser = Userlogin
            print(currentUser.fname)
            return redirect("/home")

        except:
            return "This password and email combination do not exist."
    else:
        return render_template("logInPage.html")

@app.route('/home', methods=['GET', 'POST'])
def landingPage():
    print(currentUser)
    if currentUser:
        print("Passed")
        liveClubs = Club.select().where(Club.active)
        updates = Updates.select().order_by(Updates.date.desc()).get()
        lastUpdated = getTodayDifference(updates.date)
        return render_template("landingPage.html", user=currentUser, liveClubs=liveClubs, updates=updates, lastUpdated = lastUpdated)
    return "Access Denied"

@app.route("/createAccount", methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        print("I can't believe this works!")
        data = request.form
        print(data.get('fname'))
        if User.get_or_none(User.email == data.get('email')):
            return "User already Exists"
        else:
            userRegister = User.create(username=data.get('uname'), fname=data.get('fname'), lname=data.get('lname'), email=data.get('email'), password=data.get('password'))
        if User.get_or_none(User.username == data.get('uname')):
            return render_template("logInPage.html")


    else:
        return render_template("registrationPage.html")

@app.route("/hc/myProfile", methods=['GET', "POST"])
def myAccount():
    if currentUser:
        print("On page")
        return render_template("/userProfile.html", currentUser=currentUser)
    else:
        return "Access Denied"

@app.route("/logout", methods=['GET', 'POST'])
def logOut():
    global currentUser
    currentUser = None
    return redirect("/")


###################DATABASE#########################################
basedir = os.path.abspath(os.path.dirname(__file__))

db = MySQLDatabase('hobbyconnect', host='localhost', port=3306, user='partont', password='Relyteel99!')

class User(Model):
   username=TextField(120)
   fname=TextField(120)
   lname=TextField(120)
   email=TextField(120)
   password=TextField(120)
   class Meta:
      database=db
      db_table='User'

class Club(Model):
   name=TextField(120)
   topic=TextField(120)
   logo=BlobField()
   free=BooleanField(default=True)
   lastActive=DateTimeField()
   active=BooleanField(default=False)
   class Meta:
      database=db
      db_table='Club'

class Updates(Model):
   title=TextField(120)
   version=TextField(120)
   description=TextField()
   date=DateField()
   class Meta:
      database=db
      db_table='Updates'

db.connect()
db.create_tables([User])
db.create_tables([Club])
db.create_tables([Updates])
