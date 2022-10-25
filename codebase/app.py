import os
from datetime import date
from dateutil import parser
from flask import Flask, render_template, request, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from peewee import *

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
            print("trying")
            Userlogin = User.select().where(User.email == login.get('email'), User.password == login.get('password')).get()
            print("Found user")
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
    liveClubs = Club.select().where(Club.active)
    updates = Updates.select().order_by(Updates.date.desc()).get()
    print(updates.date)
    currentDate = parser.parse(date.today())
    updateDate = parser.parse(updates.date)

    if currentDate - updateDate > 1:
        lastUpdated = currentDate - updateDate
    else:
        lastUpdated = None
    return render_template("landingPage.html", user=currentUser, liveClubs=liveClubs, updates=updates, lastUpdated = lastUpdated)

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
