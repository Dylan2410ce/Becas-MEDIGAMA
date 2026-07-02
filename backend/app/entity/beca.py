from sqlalchemy import Column, Float, Integer, String, Text

from app.config.database import Base


class BecaORM(Base):
    __tablename__ = "becas_decisiones_tb"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitante = Column(Integer, unique=True, nullable=False)
    categoria = Column(String(30), nullable=False)
    monto_total = Column(Float, nullable=False)
    estado = Column(String(20), nullable=False, default="Pendiente")
    descripcion = Column(Text, nullable=False)

    def __repr__(self):
        return f"BecaORM(id={self.id}, id_solicitante={self.id_solicitante})"
