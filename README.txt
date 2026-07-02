BECAS MEDIGAMA WEB
Este proyecto permite registrar estudiantes, recibir solicitudes de beca,
revisarlas desde un panel administrativo y consultar resultados aprobados.

USUARIOS
Estudiante solicitante:
- Crea cuenta, inicia sesion, actualiza sus datos y recupera contrasena.
- Llena la solicitud socioeconomica y consulta si tiene beca aprobada.

Administrador:
- Usa credenciales ya creadas en MySQL.
- Revisa solicitantes, aprueba o rechaza becas y crea otros admins.
- Consulta reportes, estadisticas, categorias, estados y presupuesto.

TECNOLOGIAS USADAS
- Python con FastAPI para la API.
- SQLAlchemy para trabajar con MySQL usando ORM.
- PyMySQL para conectar Python con MySQL.
- HTML, CSS y JavaScript para el frontend.
- Draw.io para el diagrama UML.

COMO SE CONECTA TODO
El frontend envia peticiones HTTP a la API.
La API recibe los datos en los controllers.
Los services revisan reglas, validaciones, calculos y permisos.
Los repositories guardan y consultan informacion en MySQL.
Las entities representan las tablas de la base de datos.

CARPETAS
backend/
Contiene la API del proyecto.

backend/app/controller/
Recibe peticiones del frontend.

backend/app/service/
Tiene validaciones, calculos, permisos y reglas.

backend/app/repository/
Hace consultas y registros en la base de datos.

backend/app/entity/
Define las tablas usadas por SQLAlchemy.

backend/app/schemas/
Define los datos que entran y salen de la API.

backend/app/config/
Contiene la conexion con MySQL.

frontend/
Contiene la pagina web hecha con HTML, CSS y JavaScript.

docs/
Contiene el UML del proyecto en formato draw.io.

LOGICA PRINCIPAL
- El ID de usuarios, solicitantes y becas es autoincrementable.
- Las validaciones de campos vacios se hacen en service.
- El calculo de vulnerabilidad se hace en service.
- La categoria sugerida de beca se calcula automaticamente.
- El administrador decide la aprobacion final.
- El sistema controla presupuesto disponible para becas aprobadas.
- Los reportes muestran montos, categorias y estados.
- Solo administradores pueden crear otros administradores.

COMO EJECUTAR
1. Crear la base de datos en MySQL:
CREATE DATABASE becas_medigama;

2. Revisar la conexion en:
backend/app/config/database.py

3. Entrar a la carpeta backend:
cd backend

4. Instalar dependencias:
py -m pip install -r requirements.txt

5. Iniciar la API:
py -m uvicorn app.main:app --reload

6. Abrir el frontend:
frontend/index.html

CREDENCIALES ADMIN INICIALES
Correo: admin@medigama.com
Contrasena: 12345

