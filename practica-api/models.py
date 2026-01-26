from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, unique=True)  # ID de la API
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    second_surname = db.Column(db.String(100))
    shortname = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    image_url = db.Column(db.String(300))
    image_local = db.Column(db.String(300))  # ruta local de la imagen
