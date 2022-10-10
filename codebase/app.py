import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from peewee import *
app = Flask(__name__)

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
            print("looking for user", Userlogin.fname)
            return ("Welcome back " + Userlogin.fname + " " + Userlogin.lname)

        except:
            return "This password and email combination do not exist."

    else:
        return render_template("logInPage.html")

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
db.connect()
db.create_tables([User])
