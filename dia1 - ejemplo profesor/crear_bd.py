import pymysql

# Conectar a MySQL sin especificar la base de datos
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        port=3306
    )
    
    cursor = connection.cursor()
    
    # Crear la base de datos si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS pybbdd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("[OK] Base de datos 'pybbdd' creada exitosamente (o ya existia)")
    
    cursor.close()
    connection.close()
    
except pymysql.err.OperationalError as e:
    print(f"[ERROR] Error al conectar a MySQL: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que MySQL/MariaDB este corriendo")
    print("2. Verifica que el usuario 'root' no tenga contrasena")
    print("3. Verifica que MySQL este escuchando en el puerto 3306")
except Exception as e:
    print(f"[ERROR] Error inesperado: {e}")
