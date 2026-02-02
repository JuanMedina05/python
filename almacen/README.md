# Sistema de Gestión de Almacén

Aplicación web desarrollada con Flask para la gestión de productos en un almacén. Permite crear, leer, actualizar y eliminar productos y servicios, además de buscar productos por diversos criterios y gestionar el bloqueo de productos para servicios.

## Características

### 📦 Gestión de Productos
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Información detallada: nombre, descripción, código, cantidad, ubicación (pasillo/estante/nivel)
- Carga de imágenes para cada producto
- Fechas de entrada y salida
- Búsqueda avanzada por código, nombre, descripción y ubicación

### 🔧 Gestión de Servicios
- CRUD completo para servicios
- Estados: activo/inactivo
- Bloqueo de múltiples productos por servicio
- Relación many-to-many entre productos y servicios

### 🎨 Diseño Moderno
- Interfaz responsive y moderna
- Paleta de colores premium
- Animaciones y transiciones suaves
- Diseño adaptable a dispositivos móviles

## Tecnologías Utilizadas

- **Backend**: Flask 3.0
- **ORM**: SQLAlchemy
- **Base de Datos**: MySQL (con PyMySQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Tipografía**: Inter (Google Fonts)

## Requisitos Previos

- Python 3.8 o superior
- XAMPP con MySQL activo en puerto 3306
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd c:\Users\usuariom\Documents\DWES\python\almacen
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

```bash
# Windows
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Copiar `.env.example` a `.env` y ajustar según sea necesario:

```bash
copy .env.example .env
```

Editar `.env` con tus credenciales de MySQL si es necesario.

### 6. Asegurar que XAMPP está corriendo

- Iniciar XAMPP
- Asegurar que MySQL está activo en puerto 3306

### 7. Crear la base de datos

Desde phpMyAdmin o línea de comandos MySQL:

```sql
CREATE DATABASE almacen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 8. Inicializar las tablas

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 9. (Opcional) Cargar datos de ejemplo

```bash
flask seed-db
```

## Uso

### Iniciar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Rutas Principales

- **Inicio**: `/`
- **Productos**: `/productos`
- **Nuevo Producto**: `/productos/nuevo`
- **Detalle Producto**: `/productos/<id>`
- **Buscar Productos**: `/productos/buscar?q=<termino>`
- **Servicios**: `/servicios`
- **Nuevo Servicio**: `/servicios/nuevo`
- **Detalle Servicio**: `/servicios/<id>`

## Estructura del Proyecto

```
almacen/
├── app.py                    # Aplicación principal Flask
├── models.py                 # Modelos de base de datos
├── config.py                 # Configuración
├── requirements.txt          # Dependencias
├── .env.example             # Ejemplo de variables de entorno
├── static/
│   ├── css/
│   │   └── style.css        # Estilos principales
│   ├── js/
│   │   └── main.js          # JavaScript
│   └── uploads/             # Imágenes de productos
└── templates/
    ├── base.html            # Plantilla base
    ├── index.html           # Página principal
    ├── products/            # Templates de productos
    │   ├── list.html
    │   ├── detail.html
    │   ├── form.html
    │   └── search.html
    └── services/            # Templates de servicios
        ├── list.html
        ├── detail.html
        └── form.html
```

## Funcionalidades Destacadas

### Búsqueda Avanzada
Busca productos por:
- Código
- Nombre
- Descripción
- Ubicación (pasillo, estante, nivel)

### Bloqueo de Productos
- Los servicios pueden bloquear múltiples productos
- Los productos bloqueados se marcan visualmente
- Relación bidireccional: desde producto ver servicios que lo bloquean

### Upload de Imágenes
- Soporte para PNG, JPG, JPEG, GIF, WEBP
- Vista previa antes de subir
- Límite de 16MB por imagen

## Autor

Desarrollado para el curso de DWES

## Licencia

Este proyecto es de uso educativo.
