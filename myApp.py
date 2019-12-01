from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
# import BL.User
myApp = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "myDatabase.db"))
myApp.config["SQLALCHEMY_DATABASE_URI"] = database_file
myApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

mydb = SQLAlchemy(myApp)

class user(mydb.Model):
    user_ID = mydb.Column(mydb.Integer , unique=True , nullable=False, primary_key=True , autoincrement=True)
    user_Name = mydb.Column(mydb.String(40), unique=False, nullable=False)
    user_Email = mydb.Column(mydb.String(40), unique=False, nullable=False)
    user_Address = mydb.Column(mydb.String(100), unique=False, nullable=False)
    user_City = mydb.Column(mydb.String(40), unique=False, nullable=False)
    user_MobileNo = mydb.Column(mydb.String(30), unique=False, nullable=False)

# mydb.create_all()
print(myApp)


# this is a main page of my website
@myApp.route("/")
def index():
    AllUser=user.query.all()
    print(AllUser)
    return render_template('index.html', myAlluser=AllUser)
@myApp.route("/user_registration",methods=['POST','GET'] )
def user_registration():
    if request.method=='POST':
        myUser=user()
        myUser.user_Name=request.form["name"]
        myUser.user_Email=request.form['email']
        myUser.user_City=request.form['city']
        myUser.user_Address=request.form['address']
        myUser.user_MobileNo=request.form['MobileNo']
        mydb.session.add(myUser)
        mydb.session.commit()
    AllUser = user.query.all()
    return render_template('index.html',myAlluser=AllUser)


@myApp.route("/delete",methods=['POST'])
def target_User():
    # if request.method=="POST":
    user_name=request.form['target_user']

    user_find = user.query.filter_by(user_Name=user_name).first()
    print(user_find)
    mydb.session.delete(user_find)
    mydb.session.commit()

    AllUser = user.query.all()
    return render_template('index.html', myAlluser=AllUser)
@myApp.route("/update", methods=['POST'])
def update():
    ID=request.form['ID']
    name=request.form['name']
    user_find=user.query.filter_by(user_ID=ID).first()
    user_find.user_Name=name
    mydb.session.add(user_find)
    mydb.session.commit()
    AllUser = user.query.all()
    return render_template('index.html', myAlluser=AllUser)


myApp.run(debug=True)
