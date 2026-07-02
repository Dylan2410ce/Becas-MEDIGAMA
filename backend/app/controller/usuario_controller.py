from fastapi import APIRouter, HTTPException

from app.schemas.usuario_schema import UsuarioCreateSchema, UsuarioSchema, UsuarioUpdateSchema
from app.service.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
service = UsuarioService()


@router.post("/estudiantes", response_model=UsuarioSchema)
def registrar_estudiante(body: UsuarioCreateSchema):
    try:
        return service.create_student(
            body.nombre,
            body.correo,
            body.telefono,
            body.contrasena
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admins", response_model=UsuarioSchema)
def registrar_admin(body: UsuarioCreateSchema, admin_id: int):
    try:
        service.require_admin(admin_id)
        return service.create_admin(
            body.nombre,
            body.correo,
            body.telefono,
            body.contrasena
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UsuarioSchema)
def obtener_mi_usuario(usuario_id: int):
    try:
        return service.get_user(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/me", response_model=UsuarioSchema)
def actualizar_mi_usuario(body: UsuarioUpdateSchema, usuario_id: int):
    try:
        return service.update_user(usuario_id, body.nombre, body.correo, body.telefono)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[UsuarioSchema])
def listar_usuarios(admin_id: int):
    try:
        service.require_admin(admin_id)
        return service.list_users()
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/admins", response_model=list[UsuarioSchema])
def listar_admins(admin_id: int):
    try:
        service.require_admin(admin_id)
        return service.list_admins()
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
