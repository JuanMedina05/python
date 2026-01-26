from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from models import db, Character
from services.character_service import obtener_characters

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/api1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "miclave"

# Inicializar db con la app
db.init_app(app)

with app.app_context():
    db.create_all()

# Ruta principal para mostrar los personajes
@app.route("/")
def index():
    characters = Character.query.all()
    return render_template("index.html", characters=characters)

# Ruta para importar characters desde la API
@app.route("/characters/import")
def importar_characters():
    data = obtener_characters()
    
    for char in data:
        existe = Character.query.filter_by(character_id=char["id"]).first()
        if not existe:
            nuevo = Character(
                character_id=char["id"],
                name=char.get("name"),
                surname=char.get("surname"),
                second_surname=char.get("second_surname"),
                shortname=char.get("shortname"),
                nickname=char.get("nickname"),
                image_url=char.get("image_url")
            )
            db.session.add(nuevo)
    
    db.session.commit()
    return jsonify({"message": "Characters importados correctamente", "total": len(data)})

if __name__ == "__main__":
    app.run(debug=True)
