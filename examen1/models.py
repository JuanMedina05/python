from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # dueno, camarero, cocina


class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    kind = db.Column(db.String(20), nullable=False)  # plato, bebida
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)


class RestaurantTable(db.Model):
    __tablename__ = "restaurant_tables"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    is_paid = db.Column(db.Boolean, default=True, nullable=False)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey("restaurant_tables.id"), nullable=False)
    waiter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="abierta", nullable=False)  # abierta, pagada
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    paid_at = db.Column(db.DateTime, nullable=True)
    table = db.relationship("RestaurantTable")


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.String(30),
        default="pendiente",
        nullable=False
    )  # pendiente, en_preparacion, listo, entregado
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    order = db.relationship("Order")
    menu_item = db.relationship("MenuItem")


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("restaurant_tables.id"), nullable=False)
    total = db.Column(db.Float, nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


def seed_initial_data():
    """Crear usuarios iniciales de ejemplo si no existen."""
    if not User.query.filter_by(username="dueno").first():
        db.session.add(User(
            username="dueno",
            password_hash=generate_password_hash("dueno123"),
            role="dueno"
        ))
    if not User.query.filter_by(username="camarero").first():
        db.session.add(User(
            username="camarero",
            password_hash=generate_password_hash("camarero123"),
            role="camarero"
        ))
    if not User.query.filter_by(username="cocina").first():
        db.session.add(User(
            username="cocina",
            password_hash=generate_password_hash("cocina123"),
            role="cocina"
        ))
    db.session.commit()


def get_open_order(table_id: int):
    """Obtener la comanda abierta de una mesa (si existe)."""
    return Order.query.filter_by(table_id=table_id, status="abierta").first()


def order_total(order_id: int) -> float:
    """Calcular el total de una comanda."""
    rows = OrderItem.query.filter_by(order_id=order_id).all()
    return round(sum(r.quantity * r.unit_price for r in rows), 2)

