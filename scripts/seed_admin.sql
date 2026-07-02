CREATE DATABASE IF NOT EXISTS becas_medigama;
USE becas_medigama;

CREATE TABLE IF NOT EXISTS usuarios_sistema_tb (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(120) NOT NULL UNIQUE,
  telefono VARCHAR(30) NOT NULL,
  contrasena VARCHAR(80) NOT NULL,
  rol VARCHAR(20) NOT NULL DEFAULT 'estudiante'
);

INSERT INTO usuarios_sistema_tb (nombre, correo, telefono, contrasena, rol)
VALUES ('Administrador Principal', 'admin@medigama.com', '00000000', '12345', 'admin')
ON DUPLICATE KEY UPDATE
  nombre = VALUES(nombre),
  telefono = VALUES(telefono),
  contrasena = VALUES(contrasena),
  rol = VALUES(rol);
