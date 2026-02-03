from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Producto

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/almacen2'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "miclave"

db.init_app(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # tu función para comprobar contraseña
            session["user_id"] = user.id  # guardamos el id del usuario en la sesión
            session["username"] = user.username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
    
    return render_template("login.html")
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validar si existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            message = "El nombre de usuario ya existe."
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            # Establecer sesión automáticamente después del registro
            session["user_id"] = new_user.id
            session["username"] = new_user.username
            
            return redirect(url_for('index'))

    return render_template('register.html', message=message)

@app.route('/logout')
def logout():
    # Limpiar toda la sesión
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if "user_id" not in session:
        print("no funciona")
        return redirect(url_for("login"))  # si no hay sesión, va a login
        
    user = User.query.get(session["user_id"])
    return render_template("index.html")

@app.route('/productos')
def ver_productos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    productos = Producto.query.all()  # traemos todos los productos
    return render_template('productos.html', productos=productos)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)