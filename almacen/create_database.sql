-- Script SQL para crear la base de datos del almacén
-- Ejecutar en phpMyAdmin o línea de comandos MySQL

CREATE DATABASE IF NOT EXISTS almacen_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos
USE almacen_db;

-- Las tablas se crearán automáticamente ejecutando el script Python init_db.py
