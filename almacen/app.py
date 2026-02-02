import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from config import Config
from models import db, Producto, Servicio

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Inicializar base de datos
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


# ============= RUTAS PRINCIPALES =============

@app.route('/')
def index():
    """Página principal"""
    total_productos = Producto.query.count()
    total_servicios = Servicio.query.count()
    servicios_activos = Servicio.query.filter_by(estado='activo').count()
    productos_bloqueados = Producto.query.join(Producto.servicios).filter(Servicio.estado == 'activo').distinct().count()
    
    return render_template('index.html',
                         total_productos=total_productos,
                         total_servicios=total_servicios,
                         servicios_activos=servicios_activos,
                         productos_bloqueados=productos_bloqueados)


# ============= RUTAS DE PRODUCTOS =============

@app.route('/productos')
def productos_lista():
    """Lista todos los productos"""
    productos = Producto.query.order_by(Producto.created_at.desc()).all()
    return render_template('products/list.html', productos=productos)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def productos_nuevo():
    """Crear nuevo producto"""
    if request.method == 'POST':
        try:
            # Manejar imagen
            imagen_filename = None
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file.filename:
                    imagen_filename = save_uploaded_file(file)
            
            # Crear producto
            producto = Producto(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', ''),
                pasillo=request.form.get('pasillo', ''),
                estante=request.form.get('estante', ''),
                nivel=request.form.get('nivel', ''),
                cantidad=int(request.form.get('cantidad', 0)),
                codigo=request.form['codigo'],
                imagen=imagen_filename
            )
            
            # Manejar fechas opcionales
            if request.form.get('fecha_salida'):
                producto.fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d')
            
            db.session.add(producto)
            db.session.commit()
            
            flash(f'Producto "{producto.nombre}" creado exitosamente.', 'success')
            return redirect(url_for('productos_detalle', id=producto.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear producto: {str(e)}', 'error')
            return redirect(url_for('productos_nuevo'))
    
    return render_template('products/form.html', producto=None)


@app.route('/productos/<int:id>')
def productos_detalle(id):
    """Ver detalles de un producto"""
    producto = Producto.query.get_or_404(id)
    servicios_bloqueados = producto.servicios.all()
    return render_template('products/detail.html', 
                         producto=producto, 
                         servicios_bloqueados=servicios_bloqueados)


@app.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
def productos_editar(id):
    """Editar producto existente"""
    producto = Producto.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Actualizar campos
            producto.nombre = request.form['nombre']
            producto.descripcion = request.form.get('descripcion', '')
            producto.pasillo = request.form.get('pasillo', '')
            producto.estante = request.form.get('estante', '')
            producto.nivel = request.form.get('nivel', '')
            producto.cantidad = int(request.form.get('cantidad', 0))
            producto.codigo = request.form['codigo']
            
            # Manejar nueva imagen
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file.filename:
                    # Eliminar imagen anterior si existe
                    if producto.imagen:
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], producto.imagen)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    producto.imagen = save_uploaded_file(file)
            
            # Manejar fecha de salida
            if request.form.get('fecha_salida'):
                producto.fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d')
            else:
                producto.fecha_salida = None
            
            db.session.commit()
            flash(f'Producto "{producto.nombre}" actualizado exitosamente.', 'success')
            return redirect(url_for('productos_detalle', id=producto.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar producto: {str(e)}', 'error')
    
    return render_template('products/form.html', producto=producto)


@app.route('/productos/<int:id>/eliminar', methods=['POST'])
def productos_eliminar(id):
    """Eliminar producto"""
    producto = Producto.query.get_or_404(id)
    
    try:
        # Eliminar imagen si existe
        if producto.imagen:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], producto.imagen)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        nombre = producto.nombre
        db.session.delete(producto)
        db.session.commit()
        
        flash(f'Producto "{nombre}" eliminado exitosamente.', 'success')
        return redirect(url_for('productos_lista'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar producto: {str(e)}', 'error')
        return redirect(url_for('productos_detalle', id=id))


@app.route('/productos/buscar')
def productos_buscar():
    """Buscar productos por código, nombre, descripción o ubicación"""
    query = request.args.get('q', '').strip()
    
    if not query:
        flash('Por favor ingresa un término de búsqueda.', 'warning')
        return redirect(url_for('productos_lista'))
    
    # Buscar en múltiples campos
    productos = Producto.query.filter(
        db.or_(
            Producto.codigo.ilike(f'%{query}%'),
            Producto.nombre.ilike(f'%{query}%'),
            Producto.descripcion.ilike(f'%{query}%'),
            Producto.pasillo.ilike(f'%{query}%'),
            Producto.estante.ilike(f'%{query}%'),
            Producto.nivel.ilike(f'%{query}%')
        )
    ).all()
    
    return render_template('products/search.html', 
                         productos=productos, 
                         query=query)


# ============= RUTAS DE SERVICIOS =============

@app.route('/servicios')
def servicios_lista():
    """Lista todos los servicios"""
    servicios = Servicio.query.order_by(Servicio.created_at.desc()).all()
    return render_template('services/list.html', servicios=servicios)


@app.route('/servicios/nuevo', methods=['GET', 'POST'])
def servicios_nuevo():
    """Crear nuevo servicio"""
    if request.method == 'POST':
        try:
            # Crear servicio
            servicio = Servicio(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', ''),
                estado=request.form.get('estado', 'activo')
            )
            
            # Manejar fecha de salida
            if request.form.get('fecha_salida'):
                servicio.fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d')
            
            # Asignar productos bloqueados
            productos_ids = request.form.getlist('productos')
            if productos_ids:
                productos = Producto.query.filter(Producto.id.in_(productos_ids)).all()
                for producto in productos:
                    servicio.productos.append(producto)
            
            db.session.add(servicio)
            db.session.commit()
            
            flash(f'Servicio "{servicio.nombre}" creado exitosamente.', 'success')
            return redirect(url_for('servicios_detalle', id=servicio.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear servicio: {str(e)}', 'error')
            return redirect(url_for('servicios_nuevo'))
    
    # Obtener todos los productos para el formulario
    productos_disponibles = Producto.query.order_by(Producto.nombre).all()
    return render_template('services/form.html', 
                         servicio=None, 
                         productos_disponibles=productos_disponibles)


@app.route('/servicios/<int:id>')
def servicios_detalle(id):
    """Ver detalles de un servicio"""
    servicio = Servicio.query.get_or_404(id)
    productos_bloqueados = servicio.productos.all()
    return render_template('services/detail.html', 
                         servicio=servicio, 
                         productos_bloqueados=productos_bloqueados)


@app.route('/servicios/<int:id>/editar', methods=['GET', 'POST'])
def servicios_editar(id):
    """Editar servicio existente"""
    servicio = Servicio.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Actualizar campos
            servicio.nombre = request.form['nombre']
            servicio.descripcion = request.form.get('descripcion', '')
            servicio.estado = request.form.get('estado', 'activo')
            
            # Manejar fecha de salida
            if request.form.get('fecha_salida'):
                servicio.fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d')
            else:
                servicio.fecha_salida = None
            
            # Actualizar productos bloqueados
            servicio.productos = []  # Limpiar relaciones actuales
            productos_ids = request.form.getlist('productos')
            if productos_ids:
                productos = Producto.query.filter(Producto.id.in_(productos_ids)).all()
                for producto in productos:
                    servicio.productos.append(producto)
            
            db.session.commit()
            flash(f'Servicio "{servicio.nombre}" actualizado exitosamente.', 'success')
            return redirect(url_for('servicios_detalle', id=servicio.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar servicio: {str(e)}', 'error')
    
    # Obtener todos los productos para el formulario
    productos_disponibles = Producto.query.order_by(Producto.nombre).all()
    productos_bloqueados_ids = [p.id for p in servicio.productos.all()]
    
    return render_template('services/form.html', 
                         servicio=servicio, 
                         productos_disponibles=productos_disponibles,
                         productos_bloqueados_ids=productos_bloqueados_ids)


@app.route('/servicios/<int:id>/eliminar', methods=['POST'])
def servicios_eliminar(id):
    """Eliminar servicio"""
    servicio = Servicio.query.get_or_404(id)
    
    try:
        nombre = servicio.nombre
        db.session.delete(servicio)
        db.session.commit()
        
        flash(f'Servicio "{nombre}" eliminado exitosamente.', 'success')
        return redirect(url_for('servicios_lista'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar servicio: {str(e)}', 'error')
        return redirect(url_for('servicios_detalle', id=id))


# ============= FILTROS JINJA =============

@app.template_filter('datetime_format')
def datetime_format(value, format='%d/%m/%Y %H:%M'):
    """Formatea fechas para mostrar en templates"""
    if value is None:
        return ''
    return value.strftime(format)


@app.template_filter('date_format')
def date_format(value, format='%d/%m/%Y'):
    """Formatea solo la fecha sin hora"""
    if value is None:
        return ''
    return value.strftime(format)


# ============= MANEJO DE ERRORES =============

@app.errorhandler(404)
def page_not_found(e):
    """Página no encontrada"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Error interno del servidor"""
    db.session.rollback()
    return render_template('500.html'), 500


# ============= COMANDOS DE CLI =============

@app.cli.command()
def init_db():
    """Inicializa la base de datos"""
    db.create_all()
    print('Base de datos inicializada.')


@app.cli.command()
def seed_db():
    """Rellena la base de datos con datos de prueba"""
    # Crear algunos productos de ejemplo
    productos_ejemplo = [
        Producto(nombre='Tornillos M8', codigo='TOR-M8-001', descripcion='Tornillos métricos M8 x 20mm', 
                pasillo='A', estante='1', nivel='2', cantidad=500),
        Producto(nombre='Tuercas M8', codigo='TUE-M8-001', descripcion='Tuercas métricas M8', 
                pasillo='A', estante='1', nivel='3', cantidad=500),
        Producto(nombre='Arandelas', codigo='ARN-001', descripcion='Arandelas planas 8mm', 
                pasillo='A', estante='2', nivel='1', cantidad=1000),
    ]
    
    for producto in productos_ejemplo:
        db.session.add(producto)
    
    db.session.commit()
    print(f'Se han creado {len(productos_ejemplo)} productos de ejemplo.')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
