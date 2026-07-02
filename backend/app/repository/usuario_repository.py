from app.config.database import SessionLocal
from app.entity.usuario import UsuarioORM


class UsuarioRepository:
    def _detach(self, db, obj):
        if obj:
            db.expunge(obj)
        return obj

    def create(self, nombre, correo, telefono, contrasena, rol):
        db = SessionLocal()
        try:
            usuario = UsuarioORM(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                contrasena=contrasena,
                rol=rol
            )
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            return self._detach(db, usuario)
        finally:
            db.close()

    def get(self, user_id):
        db = SessionLocal()
        try:
            usuario = db.query(UsuarioORM).filter_by(id=user_id).first()
            return self._detach(db, usuario)
        finally:
            db.close()

    def get_by_correo(self, correo):
        db = SessionLocal()
        try:
            usuario = db.query(UsuarioORM).filter_by(correo=correo).first()
            return self._detach(db, usuario)
        finally:
            db.close()

    def get_all(self):
        db = SessionLocal()
        try:
            usuarios = db.query(UsuarioORM).order_by(UsuarioORM.rol, UsuarioORM.nombre).all()
            for usuario in usuarios:
                db.expunge(usuario)
            return usuarios
        finally:
            db.close()

    def get_by_rol(self, rol):
        db = SessionLocal()
        try:
            usuarios = db.query(UsuarioORM).filter_by(rol=rol).order_by(UsuarioORM.nombre).all()
            for usuario in usuarios:
                db.expunge(usuario)
            return usuarios
        finally:
            db.close()

    def update(self, user_id, nombre, correo, telefono):
        db = SessionLocal()
        try:
            usuario = db.query(UsuarioORM).filter_by(id=user_id).first()
            if usuario:
                usuario.nombre = nombre
                usuario.correo = correo
                usuario.telefono = telefono
                db.commit()
                db.refresh(usuario)
            return self._detach(db, usuario)
        finally:
            db.close()

    def update_password(self, correo, nueva_contrasena):
        db = SessionLocal()
        try:
            usuario = db.query(UsuarioORM).filter_by(correo=correo).first()
            if usuario:
                usuario.contrasena = nueva_contrasena
                db.commit()
                db.refresh(usuario)
            return self._detach(db, usuario)
        finally:
            db.close()
