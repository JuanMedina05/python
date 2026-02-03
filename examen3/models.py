from datetime import date
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")


    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = ""
    def get_username(self):
        return self.username
    def set_username(self, username):
        self.username = username
    def get_password(self):
        return self.password
    def check_password(self, password):
        return self.password == password
    def is_admin(self):
        return self.role == "admin"

class Productos(db.Model):
    __tablename__='productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    precio = db.Column(db.Integer, default=0)
    imagen = db.Column(db.String(255))

    def __init__(self,nombre,precio,imagen):
        self.nombre=nombre
        self.precio=precio
        self.imagen=imagen


class Mesas(db.Model):
    __tablename__='mesas'

    num_mesa=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50), unique=True, nullable=False)
    def get_nombre(self):
        return self.nombre
    def set_nombre(self, nombre):
        self.nombre = nombre

