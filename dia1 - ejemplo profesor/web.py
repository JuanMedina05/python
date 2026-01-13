from flask.globals import request
from flask.templating import render_template
from app_test import Coche, Avion, db, app

@app.route('/', methods=['GET', 'POST'])
def index():

    # $var = $_GET['user']
    var = request.args.get('user')
    
    # $var = $_POST['user']
    usuario = request.form.get('user')

    # $_SESSION['user'] = $usuario
    session['user'] = usuario

    # $var = $_SESSION['user']
    usuario = session.get('user')

    session.pop('user')

    # $var = $_COOKIE['user']
    cookie = request.cookies.get('user')

    # $imagen = $_FILES['imagen']
    imagen = request.files.get('imagen')

    # $imagen.save('uploads/' . $imagen['name'])
    imagen.save('uploads/' + imagen['name'])


    coche = Coche(usuario, "model")
    db.session.add(coche)
    db.session.commit() 

    return render_template('test.html', usuario = usuario)

@app.route('/search', methods=['POST'])
def search():
    search = request.form.get('search')
    coches = Coche.query.filter_by(marca=search)
    return render_template('search.html', coches = coches)

@app.route('/coches/<int:id>')
@roles_required('manager', 'admin')
def coche(id):
    coche = Coche.query.get_or_404(id)
    coche2 = Coche.query.find("c")
    coche.set_marca("audi")
    db.session.add(coche)
    db.session.commit()

    return render_template('coches.html', coche2 = coche2)

@app.route('/coches')
def coches():
    lista_coches = Coche.query.all()
    return render_template('coches.html', coches=lista_coches)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
