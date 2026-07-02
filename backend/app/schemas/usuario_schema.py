from pydantic import BaseModel, ConfigDict


class UsuarioSchema(BaseModel):
    id: int
    nombre: str
    correo: str
    telefono: str
    rol: str

    model_config = ConfigDict(from_attributes=True)


class UsuarioCreateSchema(BaseModel):
    nombre: str
    correo: str
    telefono: str
    contrasena: str


class UsuarioUpdateSchema(BaseModel):
    nombre: str
    correo: str
    telefono: str


class LoginSchema(BaseModel):
    correo: str
    contrasena: str


class RecoverPasswordSchema(BaseModel):
    correo: str
    nueva_contrasena: str


class LoginResponseSchema(BaseModel):
    usuario: UsuarioSchema
