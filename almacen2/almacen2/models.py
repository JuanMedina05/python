from datetime import date
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

    pasillo = db.Column(db.String(20))
    estante = db.Column(db.String(20))
    nivel = db.Column(db.String(20))

    cantidad = db.Column(db.Integer, nullable=False, default=0)

    fecha_entrada = db.Column(db.Date, default=date.today)
    fecha_salida = db.Column(db.Date, nullable=True)

    imagen = db.Column(db.String(255))

    

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