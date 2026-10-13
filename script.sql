-- =====================================================
-- Script de creación de la base de datos
-- Ejecutar una sola vez antes de usar la aplicación:
--   mysql -u root -p < script.sql
-- =====================================================

CREATE DATABASE IF NOT EXISTS escuela;
USE escuela;

CREATE TABLE IF NOT EXISTS alumnos (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    dni       VARCHAR(10)  NOT NULL UNIQUE,
    nombre    VARCHAR(50)  NOT NULL,
    apellido  VARCHAR(50)  NOT NULL,
    email     VARCHAR(100),
    telefono  VARCHAR(20)
);

-- Datos de prueba
INSERT INTO alumnos (dni, nombre, apellido, email, telefono) VALUES
('40111222', 'Ana',    'Gómez',    'ana.gomez@mail.com',    '3511234567'),
('41222333', 'Bruno',  'Pérez',    'bruno.perez@mail.com',  '3517654321'),
('42333444', 'Carla',  'Martínez', 'carla.m@mail.com',      '3519876543');
