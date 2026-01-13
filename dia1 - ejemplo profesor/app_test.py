from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

# Configurar PyMySQL como MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/pybbdd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'  # Cambia esto por una clave segura

db = SQLAlchemy(app)

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    ruedas = db.Column(db.Integer)

    def __init__(self, tipo):
        self.tipo = tipo
    
    def get_tipo(self):
        return self.tipo
    
    def set_tipo(self, tipo):
        self.tipo=tipo
    
    def get_ruedas(self):
        return self.ruedas
    
    def set_ruedas(self, ruedas):
        self.ruedas=ruedas
    def volar(self):
        return "no estoy volando"

class Avion(db.Model):
    __tablename__ = 'avion'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), default='avion')
    ruedas = db.Column(db.Integer, default=2)
    
    def __init__(self):
        self.tipo = 'avion'
        self.ruedas = 2
    
    def get_tipo(self):
        return self.tipo
    
    def get_ruedas(self):
        return self.ruedas
    
    def volar(self):
        return "estoy volando"

class Coche(db.Model):
    __tablename__ = 'coche'
    
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    tipo = db.Column(db.String(50), default='coche')
    ruedas = db.Column(db.Integer, default=4)
    usuarios = db.relationship('Usuario', backref='coche', lazy=True)

    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.tipo = 'coche'
        self.ruedas = 4
    def set_marca(self, marca):
        self.marca = marca
    def get_marca(self):
        return self.marca
    def get_tipo(self):
        return self.tipo 
    def get_ruedas(self):
        return self.ruedas
    def volar(self):
        return "no estoy volando"

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    coches = db.relationship('Coche', backref='usuario', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def set_username(self, username):
        self.username = username
    
    def get_username(self):
        return self.username
    
    def set_password(self, password):
        self.password = password
    
    def get_password(self):
        return self.password

    def get_coches(self):
        return self.coches

    def set_coches(self, coches):
        self.coches = coches

# Código de prueba - solo se ejecuta si corres este archivo directamente
if __name__ == '__main__':
    car1 = Coche("Toyota", "Corolla")
    avion = Avion()
    print(avion.volar())
    print(car1.volar())
    print(vars(car1))