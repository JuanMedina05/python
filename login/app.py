from models import db, app, User
from flask import render_template, request, redirect, url_for, session


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # tu función para comprobar contraseña
            session["user_id"] = user.id  # guardamos el id del usuario en la sesión
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
    
    return render_template("login.html")

@app.route('/')
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))  # si no hay sesión, va a login
    
    user = User.query.get(session["user_id"])
    return render_template("index.html", title=user.username)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)