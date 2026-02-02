from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabla de asociación para la relación many-to-many entre productos y servicios
producto_servicio = db.Table('producto_servicio',
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True),
    db.Column('servicio_id', db.Integer, db.ForeignKey('servicios.id'), primary_key=True),
    db.Column('fecha_bloqueo', db.DateTime, default=datetime.utcnow)
)


class Producto(db.Model):
    """Modelo para productos del almacén"""
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Ubicación del producto
    pasillo = db.Column(db.String(50))
    estante = db.Column(db.String(50))
    nivel = db.Column(db.String(50))
    
    # Inventario
    cantidad = db.Column(db.Integer, default=0)
    codigo = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Fechas
    fecha_entrada = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_salida = db.Column(db.DateTime)
    
    # Imagen
    imagen = db.Column(db.String(255))
    
    # Relación con servicios (productos bloqueados para servicios)
    servicios = db.relationship('Servicio', secondary=producto_servicio, 
                               back_populates='productos',
                               lazy='dynamic')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Producto {self.codigo}: {self.nombre}>'
    
    def to_dict(self):
        """Convertir el producto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'pasillo': self.pasillo,
            'estante': self.estante,
            'nivel': self.nivel,
            'cantidad': self.cantidad,
            'codigo': self.codigo,
            'fecha_entrada': self.fecha_entrada.isoformat() if self.fecha_entrada else None,
            'fecha_salida': self.fecha_salida.isoformat() if self.fecha_salida else None,
            'imagen': self.imagen,
            'servicios_count': self.servicios.count()
        }
    
    @property
    def ubicacion_completa(self):
        """Retorna la ubicación completa del producto"""
        partes = []
        if self.pasillo:
            partes.append(f"Pasillo {self.pasillo}")
        if self.estante:
            partes.append(f"Estante {self.estante}")
        if self.nivel:
            partes.append(f"Nivel {self.nivel}")
        return " - ".join(partes) if partes else "Sin ubicación"
    
    @property
    def esta_bloqueado(self):
        """Verifica si el producto está bloqueado por algún servicio activo"""
        return self.servicios.filter_by(estado='activo').count() > 0


class Servicio(db.Model):
    """Modelo para servicios que bloquean productos"""
    __tablename__ = 'servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Fechas
    fecha_entrada = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_salida = db.Column(db.DateTime)
    
    # Estado
    estado = db.Column(db.String(20), default='activo', nullable=False)  # activo, inactivo
    
    # Relación con productos bloqueados
    productos = db.relationship('Producto', secondary=producto_servicio,
                               back_populates='servicios',
                               lazy='dynamic')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Servicio {self.id}: {self.nombre} ({self.estado})>'
    
    def to_dict(self):
        """Convertir el servicio a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_entrada': self.fecha_entrada.isoformat() if self.fecha_entrada else None,
            'fecha_salida': self.fecha_salida.isoformat() if self.fecha_salida else None,
            'estado': self.estado,
            'productos_count': self.productos.count()
        }
