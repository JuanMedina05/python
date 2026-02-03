from flask import Flask, render_template, flash, request, redirect, url_for, session
from models import db, User, Productos
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bar'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "miclave"

db.init_app(app)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file):
    """Guarda un archivo subido y retorna el nombre del archivo"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Añadir timestamp para evitar duplicados
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None

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
            
            
            return redirect(url_for('login'))

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
def productos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    productos = Productos.query.all()  # traemos todos los productos
    return render_template('index.html', productos=productos)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def productos_nuevo():
    if request.method == 'POST':
        try:
            imagen_filename = None
            if 'imagen' in request.files:
                file = request.files['imagen']
                print("1")
                print(file)
                if file.filename:
                    imagen_filename = save_uploaded_file(file)
                    print("2")

            print("3")
            producto = Productos(
                nombre=request.form['nombre'],
                precio=request.form.get('precio', 0),
                imagen=imagen_filename
            )
            
            db.session.add(producto)
            db.session.commit()

            flash('Producto creado correctamente', 'success')
            return redirect(url_for('ver_productos'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear producto: {str(e)}', 'error')
            return redirect(url_for('productos_nuevo'))

    return render_template('createproduct.html', producto=None)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)