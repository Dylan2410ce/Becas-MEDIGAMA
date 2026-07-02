from sqlalchemy import func

from app.config.database import SessionLocal
from app.entity.beca import BecaORM


class BecaRepository:
    def _detach(self, db, obj):
        if obj:
            db.expunge(obj)
        return obj

    def create_or_update(self, id_solicitante, categoria, monto_total, estado, descripcion):
        db = SessionLocal()
        try:
            beca = db.query(BecaORM).filter_by(id_solicitante=id_solicitante).first()
            if beca:
                beca.categoria = categoria
                beca.monto_total = monto_total
                beca.estado = estado
                beca.descripcion = descripcion
            else:
                beca = BecaORM(
                    id_solicitante=id_solicitante,
                    categoria=categoria,
                    monto_total=monto_total,
                    estado=estado,
                    descripcion=descripcion
                )
                db.add(beca)
            db.commit()
            db.refresh(beca)
            return self._detach(db, beca)
        finally:
            db.close()

    def get_by_solicitante(self, id_solicitante):
        db = SessionLocal()
        try:
            beca = db.query(BecaORM).filter_by(id_solicitante=id_solicitante).first()
            return self._detach(db, beca)
        finally:
            db.close()

    def get_all(self):
        db = SessionLocal()
        try:
            becas = db.query(BecaORM).order_by(BecaORM.estado, BecaORM.id_solicitante).all()
            for beca in becas:
                db.expunge(beca)
            return becas
        finally:
            db.close()

    def total_aprobado(self):
        db = SessionLocal()
        try:
            total = db.query(func.sum(BecaORM.monto_total)).filter_by(estado="Aprobado").scalar()
            cantidad = db.query(BecaORM).filter_by(estado="Aprobado").count()
            return {"cantidad_aprobadas": cantidad, "monto_total": float(total or 0)}
        finally:
            db.close()

    def count_by_categoria(self):
        db = SessionLocal()
        try:
            rows = (
                db.query(BecaORM.categoria, func.count(BecaORM.categoria))
                .filter_by(estado="Aprobado")
                .group_by(BecaORM.categoria)
                .all()
            )
            result = {"Beca 1": 0, "Beca 2": 0, "Beca 3": 0, "Beca 4": 0, "Beca 5": 0}
            for categoria, cantidad in rows:
                if categoria in result:
                    result[categoria] = cantidad
            return result
        finally:
            db.close()

    def count_by_estado(self):
        db = SessionLocal()
        try:
            rows = db.query(BecaORM.estado, func.count(BecaORM.estado)).group_by(BecaORM.estado).all()
            result = {"Pendiente": 0, "Aprobado": 0, "Rechazado": 0}
            for estado, cantidad in rows:
                if estado in result:
                    result[estado] = cantidad
            return result
        finally:
            db.close()
