from sqlalchemy import Column, Float, Integer, String, Text

from app.config.database import Base


class SolicitanteORM(Base):
    __tablename__ = "solicitantes_detalle_tb"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(30), nullable=False)
    correo = Column(String(120), unique=True, nullable=False)
    edad = Column(Integer, nullable=False)
    provincia = Column(String(60), nullable=False)
    canton = Column(String(80), nullable=False)
    universidad = Column(String(120), nullable=False)
    carrera = Column(String(120), nullable=False)
    nivel = Column(String(40), nullable=False)
    ingresos = Column(Float, nullable=False)
    gastos = Column(Float, nullable=False)
    dependientes = Column(Integer, nullable=False)
    miembros_hogar = Column(Integer, nullable=False)
    promedio = Column(Float, nullable=False)
    vivienda = Column(String(40), nullable=False)
    trabaja = Column(String(10), nullable=False)
    transporte = Column(String(40), nullable=False)
    condicion_especial = Column(String(80), nullable=False)
    situacion_especial = Column(Text, nullable=True)
    indice_vulnerabilidad = Column(Float, nullable=False)
    categoria_sugerida = Column(String(30), nullable=False)
    estado_solicitud = Column(String(30), nullable=False, default="En revision")

    def __repr__(self):
        return f"SolicitanteORM(id={self.id}, usuario_id={self.usuario_id})"
