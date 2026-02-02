"""
Script para inicializar la base de datos
"""
from app import app, db

def init_database():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✓ Tablas creadas exitosamente en la base de datos 'almacen_db'")
        print("\nTablas creadas:")
        print("  - productos")
        print("  - servicios")
        print("  - producto_servicio (tabla de relación)")

if __name__ == '__main__':
    print("Inicializando base de datos...")
    print("-" * 50)
    try:
        init_database()
        print("-" * 50)
        print("\n✓ Base de datos inicializada correctamente")
        print("\nPuedes iniciar la aplicación con:")
        print("  python app.py")
    except Exception as e:
        print(f"\n✗ Error al inicializar la base de datos: {e}")
        print("\nAsegúrate de que:")
        print("  1. XAMPP está corriendo")
        print("  2. MySQL está activo en puerto 3306")
        print("  3. La base de datos 'almacen_db' existe")
        print("\nPara crear la base de datos, ejecuta en phpMyAdmin o MySQL:")
        print("  CREATE DATABASE almacen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
