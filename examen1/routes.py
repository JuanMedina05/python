import os
from datetime import datetime
from functools import wraps

from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    send_from_directory,
)

from models import (
    db,
    MenuItem,
    Order,
    OrderItem,
    Payment,
    RestaurantTable,
    User,
    get_open_order,
    order_total,
)


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if session.get("role") not in roles:
                flash("No tienes permiso para acceder a esta sección.", "error")
                return redirect(url_for("dashboard"))
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def register_routes(app):
    @app.route("/")
    def home():
        if "user_id" in session:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    # ---------- AUTH ----------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            user = User.query.filter_by(username=username).first()
            from werkzeug.security import check_password_hash

            if not user or not check_password_hash(user.password_hash, password):
                flash("Credenciales inválidas.", "error")
                return redirect(url_for("login"))
            session["user_id"] = user.id
            session["role"] = user.role
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @role_required("dueno", "camarero", "cocina")
    def dashboard():
        role = session.get("role")
        if role == "dueno":
            return redirect(url_for("owner_dashboard"))
        if role == "camarero":
            return redirect(url_for("waiter_dashboard"))
        return redirect(url_for("kitchen_dashboard"))

    # ---------- DUEÑO ----------
    @app.route("/dueno")
    @role_required("dueno")
    def owner_dashboard():
        menu_items = MenuItem.query.order_by(MenuItem.id.desc()).all()
        tables = RestaurantTable.query.order_by(RestaurantTable.number.asc()).all()
        day_total = db.session.query(db.func.coalesce(db.func.sum(Payment.total), 0.0)).filter(
            db.func.date(Payment.paid_at) == datetime.utcnow().date()
        ).scalar()
        table_income = []
        for table in tables:
            amount = db.session.query(db.func.coalesce(db.func.sum(Payment.total), 0.0)).filter_by(
                table_id=table.id
            ).scalar()
            table_income.append({"table": table, "total": round(float(amount or 0), 2)})
        return render_template(
            "owner_dashboard.html",
            menu_items=menu_items,
            tables=tables,
            day_total=round(float(day_total or 0), 2),
            table_income=table_income,
        )

    @app.route("/dueno/menu/create", methods=["POST"])
    @role_required("dueno")
    def owner_menu_create():
        from werkzeug.utils import secure_filename

        name = request.form.get("name", "").strip()
        kind = request.form.get("kind", "").strip()
        price = request.form.get("price", type=float)
        image_path = None
        image = request.files.get("image")
        if image and image.filename:
            filename = secure_filename(image.filename)
            unique = f"{datetime.utcnow().timestamp()}_{filename}"
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], unique))
            image_path = f"/uploads/{unique}"
        if not name or kind not in {"plato", "bebida"} or price is None:
            flash("Datos de producto inválidos.", "error")
            return redirect(url_for("owner_dashboard"))
        db.session.add(MenuItem(name=name, kind=kind, price=price, image_path=image_path))
        db.session.commit()
        flash("Elemento de carta creado.", "ok")
        return redirect(url_for("owner_dashboard"))

    @app.route("/dueno/menu/<int:item_id>/update", methods=["POST"])
    @role_required("dueno")
    def owner_menu_update(item_id):
        from werkzeug.utils import secure_filename

        item = MenuItem.query.get_or_404(item_id)
        item.name = request.form.get("name", item.name).strip()
        item.kind = request.form.get("kind", item.kind).strip()
        item.price = request.form.get("price", type=float) or item.price
        image = request.files.get("image")
        if image and image.filename:
            filename = secure_filename(image.filename)
            unique = f"{datetime.utcnow().timestamp()}_{filename}"
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], unique))
            item.image_path = f"/uploads/{unique}"
        db.session.commit()
        flash("Elemento actualizado.", "ok")
        return redirect(url_for("owner_dashboard"))

    @app.route("/dueno/menu/<int:item_id>/delete", methods=["POST"])
    @role_required("dueno")
    def owner_menu_delete(item_id):
        item = MenuItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        flash("Elemento eliminado.", "ok")
        return redirect(url_for("owner_dashboard"))

    @app.route("/dueno/mesas/create", methods=["POST"])
    @role_required("dueno")
    def owner_table_create():
        number = request.form.get("number", type=int)
        name = request.form.get("name", "").strip()
        if number is None or not name:
            flash("Datos de mesa inválidos.", "error")
            return redirect(url_for("owner_dashboard"))
        if RestaurantTable.query.filter_by(number=number).first():
            flash("Ya existe una mesa con ese número.", "error")
            return redirect(url_for("owner_dashboard"))
        db.session.add(RestaurantTable(number=number, name=name, is_paid=True))
        db.session.commit()
        flash("Mesa creada correctamente.", "ok")
        return redirect(url_for("owner_dashboard"))

    # ---------- CAMARERO ----------
    @app.route("/camarero")
    @role_required("camarero")
    def waiter_dashboard():
        tables = RestaurantTable.query.order_by(RestaurantTable.number.asc()).all()
        menu_items = MenuItem.query.order_by(MenuItem.kind.asc(), MenuItem.name.asc()).all()
        ready_items = (
            db.session.query(OrderItem, RestaurantTable)
            .join(Order)
            .join(RestaurantTable)
            .filter(
                OrderItem.status == "listo",
                Order.status == "abierta",
            )
            .order_by(OrderItem.created_at.asc())
            .all()
        )
        table_totals = []
        for table in tables:
            open_order = get_open_order(table.id)
            total = order_total(open_order.id) if open_order else 0
            table_totals.append(
                {"table": table, "total": total, "order_id": open_order.id if open_order else None}
            )
        return render_template(
            "waiter_dashboard.html",
            tables=tables,
            menu_items=menu_items,
            ready_items=ready_items,
            table_totals=table_totals,
        )

    @app.route("/camarero/comanda/add", methods=["POST"])
    @role_required("camarero")
    def waiter_add_item():
        table_id = request.form.get("table_id", type=int)
        menu_item_id = request.form.get("menu_item_id", type=int)
        quantity = request.form.get("quantity", type=int, default=1)
        table = RestaurantTable.query.get_or_404(table_id)
        menu_item = MenuItem.query.get_or_404(menu_item_id)
        order = get_open_order(table.id)
        if not order:
            order = Order(table_id=table.id, waiter_id=session["user_id"], status="abierta")
            db.session.add(order)
            db.session.flush()
        db.session.add(
            OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=max(1, quantity),
                unit_price=menu_item.price,
                status="pendiente",
            )
        )
        table.is_paid = False
        db.session.commit()
        flash("Producto añadido a la comanda. Ya está en cola de cocina.", "ok")
        return redirect(url_for("waiter_dashboard"))

    @app.route("/camarero/plato/<int:item_id>/entregado", methods=["POST"])
    @role_required("camarero")
    def waiter_mark_delivered(item_id):
        item = OrderItem.query.get_or_404(item_id)
        item.status = "entregado"
        db.session.commit()
        flash("Plato marcado como entregado.", "ok")
        return redirect(url_for("waiter_dashboard"))

    @app.route("/camarero/mesa/<int:table_id>/pagar", methods=["POST"])
    @role_required("camarero")
    def waiter_pay_table(table_id):
        table = RestaurantTable.query.get_or_404(table_id)
        order = get_open_order(table.id)
        if not order:
            flash("No hay comanda abierta para esa mesa.", "error")
            return redirect(url_for("waiter_dashboard"))
        total = order_total(order.id)
        order.status = "pagada"
        order.paid_at = datetime.utcnow()
        table.is_paid = True
        db.session.add(Payment(order_id=order.id, table_id=table.id, total=total))
        db.session.commit()
        flash(f"Mesa {table.number} pagada. Total: {total:.2f} EUR", "ok")
        return redirect(url_for("waiter_dashboard"))

    # ---------- COCINA ----------
    @app.route("/cocina")
    @role_required("cocina")
    def kitchen_dashboard():
        menu_alias = MenuItem  # sólo para claridad
        queue = (
            db.session.query(OrderItem, RestaurantTable, menu_alias)
            .join(Order)
            .join(RestaurantTable)
            .join(menu_alias)
            .filter(
                Order.status == "abierta",
                OrderItem.status.in_(["pendiente", "en_preparacion"]),
            )
            .order_by(OrderItem.created_at.asc())
            .all()
        )
        return render_template("kitchen_dashboard.html", queue=queue)

    @app.route("/cocina/item/<int:item_id>/estado", methods=["POST"])
    @role_required("cocina")
    def kitchen_change_status(item_id):
        item = OrderItem.query.get_or_404(item_id)
        new_status = request.form.get("status", "").strip()
        if new_status not in {"en_preparacion", "listo"}:
            flash("Estado inválido para cocina.", "error")
            return redirect(url_for("kitchen_dashboard"))
        item.status = new_status
        db.session.commit()
        flash("Estado del plato actualizado.", "ok")
        return redirect(url_for("kitchen_dashboard"))

    # ---------- IMÁGENES ----------
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

