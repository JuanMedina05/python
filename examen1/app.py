import os

from flask import Flask

from models import db, seed_initial_data
from routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@localhost:3306/examen1_restaurante",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    upload_folder = os.path.join(os.path.dirname(__file__), "static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_folder

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_initial_data()

    register_routes(app)
    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True, host="0.0.0.0", port=5001)
