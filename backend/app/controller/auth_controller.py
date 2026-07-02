from fastapi import APIRouter, HTTPException

from app.schemas.usuario_schema import LoginResponseSchema, LoginSchema, RecoverPasswordSchema
from app.service.auth_service import AuthService
from app.service.usuario_service import UsuarioService

router = APIRouter(prefix="/auth", tags=["Autenticacion"])
auth_service = AuthService()
usuario_service = UsuarioService()


@router.post("/login", response_model=LoginResponseSchema)
def login(body: LoginSchema):
    try:
        usuario = auth_service.login(body.correo, body.contrasena)
        return {"usuario": usuario}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.patch("/recuperar-contrasena")
def recuperar_contrasena(body: RecoverPasswordSchema):
    try:
        usuario_service.recover_password(body.correo, body.nueva_contrasena)
        return {"message": "Contrasena actualizada correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
