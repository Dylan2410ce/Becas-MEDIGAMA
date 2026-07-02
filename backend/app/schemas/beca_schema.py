from pydantic import BaseModel, ConfigDict


ALLOWED_CATEGORIAS = {"Beca 1", "Beca 2", "Beca 3", "Beca 4", "Beca 5"}
ALLOWED_ESTADOS = {"Pendiente", "Aprobado", "Rechazado"}


class BecaSchema(BaseModel):
    id: int
    id_solicitante: int
    categoria: str
    monto_total: float
    estado: str
    descripcion: str

    model_config = ConfigDict(from_attributes=True)


class BecaAsignarSchema(BaseModel):
    id_solicitante: int
    categoria: str
    estado: str = "Aprobado"
    descripcion: str


class ResultadoBecaSchema(BaseModel):
    id_solicitud: str
    id_solicitante: int
    estudiante: str
    tipo: str
    categoria: str
    monto: float
    estado: str
    descripcion: str
