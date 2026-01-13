from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql


pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/login_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "miclave"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def get_username(self):
        return self.username
    def set_username(self, username):
        self.username = username
    def get_password(self):
        return self.password
    def check_password(self, password):
        return self.password == password
