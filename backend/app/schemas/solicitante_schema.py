from pydantic import BaseModel, ConfigDict


class SolicitanteSchema(BaseModel):
    id: int
    usuario_id: int
    nombre: str
    telefono: str
    correo: str
    edad: int
    provincia: str
    canton: str
    universidad: str
    carrera: str
    nivel: str
    ingresos: float
    gastos: float
    dependientes: int
    miembros_hogar: int
    promedio: float
    vivienda: str
    trabaja: str
    transporte: str
    condicion_especial: str
    situacion_especial: str | None = ""
    indice_vulnerabilidad: float
    categoria_sugerida: str
    estado_solicitud: str

    model_config = ConfigDict(from_attributes=True)


class SolicitudBecaSchema(BaseModel):
    edad: int
    provincia: str
    canton: str
    universidad: str
    carrera: str
    nivel: str
    ingresos: float
    gastos: float
    dependientes: int
    miembros_hogar: int
    promedio: float
    vivienda: str
    trabaja: str
    transporte: str
    condicion_especial: str
    situacion_especial: str | None = ""
