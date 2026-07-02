from app.config.database import SessionLocal
from app.entity.solicitante import SolicitanteORM


class SolicitanteRepository:
    def _detach(self, db, obj):
        if obj:
            db.expunge(obj)
        return obj

    def create(self, data):
        db = SessionLocal()
        try:
            solicitante = SolicitanteORM(**data)
            db.add(solicitante)
            db.commit()
            db.refresh(solicitante)
            return self._detach(db, solicitante)
        finally:
            db.close()

    def update(self, solicitante, data):
        db = SessionLocal()
        try:
            current = db.query(SolicitanteORM).filter_by(id=solicitante.id).first()
            if current:
                for key, value in data.items():
                    setattr(current, key, value)
                db.commit()
                db.refresh(current)
            return self._detach(db, current)
        finally:
            db.close()

    def get(self, solicitante_id):
        db = SessionLocal()
        try:
            solicitante = db.query(SolicitanteORM).filter_by(id=solicitante_id).first()
            return self._detach(db, solicitante)
        finally:
            db.close()

    def get_by_usuario(self, usuario_id):
        db = SessionLocal()
        try:
            solicitante = db.query(SolicitanteORM).filter_by(usuario_id=usuario_id).first()
            return self._detach(db, solicitante)
        finally:
            db.close()

    def get_by_correo(self, correo):
        db = SessionLocal()
        try:
            solicitante = db.query(SolicitanteORM).filter_by(correo=correo).first()
            return self._detach(db, solicitante)
        finally:
            db.close()

    def get_all(self):
        db = SessionLocal()
        try:
            solicitantes = db.query(SolicitanteORM).order_by(SolicitanteORM.estado_solicitud, SolicitanteORM.nombre).all()
            for solicitante in solicitantes:
                db.expunge(solicitante)
            return solicitantes
        finally:
            db.close()
