import os
import base64
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

def countMembers(club):
    memberGrab = userClub.select(userClub.user).where(userClub.club == club).count()
    return memberGrab


def checkMembership(club, user):
    print(user, club)
    eligible = list(userClub.select().where(userClub.user == user & userClub.club == club))
    if len(eligible) > 1:
        return True
    else:
        return False

@app.route("/loginPage", methods=['GET', 'POST'])
def logInPage():
    if request.method == 'POST':
        login = request.form
        try:
            Userlogin = User.select().where(User.email == login.get('email'), User.password == login.get('password')).get()
            global currentUser
            currentUser = Userlogin
            return redirect("/home")

        except:
            return "This password and email combination do not exist."
    else:
        return render_template("logInPage.html")

@app.route('/joinClub', methods=['GET', 'POST'])
def joinClub():
    try:
        if currentUser:
            joinClub = userClub.create(user=currentUser, club=request.form.get('clubId'))
            return redirect("/home")
    except:
        return("Unable to join club. Who knows why?")

@app.route('/enterClub', methods=['GET', 'POST'])
def enterClub():
    eligible = checkMembership(request.form.get("clubId"), currentUser)
    if eligible:
        return render_template("clubSession.html")

@app.route('/home', methods=['GET', 'POST'])
def landingPage():
    if currentUser:
        liveClubs = Club.select().where(Club.active)
        updates = Updates.select().order_by(Updates.date.desc()).get()
        lastUpdated = getTodayDifference(updates.date)
        clubInfoArr = []
        for club in liveClubs:
            amount = countMembers(club.id)
            groupInfo = [club, amount]
            clubInfoArr.append(groupInfo)
        return render_template("landingPage.html", user=currentUser, updates=updates, lastUpdated = lastUpdated, clubInfoArr=clubInfoArr)
    return "Access Denied"

@app.route("/myClubs", methods=['GET', 'POST'])
def myClubs():
    if currentUser:
        myClubs = userClub.select(userClub.club).where(userClub.user_id == currentUser.id).distinct()
        clubInfoArr = []
        for club in myClubs:
            amount = countMembers(club.club)
            groupInfo = [club.club, amount]
            clubInfoArr.append(groupInfo)
        return render_template("myClubs.html", clubInfoArr=clubInfoArr)
    else:
        return redirect("/")

@app.route("/createClub", methods=['GET', 'POST'])
def createClub():
    clubData = request.form
    if currentUser:
        createClub = Club.create(name=clubData.get('clubName'), topic=clubData.get('clubTopic'))
        return redirect("/myClubs")
    else:
        return "Server error. Club not created."

@app.route("/createAccount", methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        data = request.form
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
   logo=BlobField(null=True)
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

class userClub(Model):
   user = ForeignKeyField(User, backref="users")
   club = ForeignKeyField(Club, backref="clubs")
   class Meta:
      database=db
      db_table='userClub'

db.connect()
db.create_tables([User])
db.create_tables([Club])
db.create_tables([Updates])
db.create_tables([userClub])
