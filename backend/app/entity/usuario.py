from sqlalchemy import Column, Integer, String

from app.config.database import Base


class UsuarioORM(Base):
    __tablename__ = "usuarios_sistema_tb"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False)
    telefono = Column(String(30), nullable=False)
    contrasena = Column(String(80), nullable=False)
    rol = Column(String(20), nullable=False, default="estudiante")

    def __repr__(self):
        return f"UsuarioORM(id={self.id}, correo='{self.correo}', rol='{self.rol}')"
