from fastapi import APIRouter, HTTPException

from app.schemas.beca_schema import BecaAsignarSchema, BecaSchema, ResultadoBecaSchema
from app.service.beca_service import BecaService
from app.service.usuario_service import UsuarioService

router = APIRouter(prefix="/becas", tags=["Becas"])
service = BecaService()
usuario_service = UsuarioService()


@router.get("/", response_model=list[BecaSchema])
def listar_becas(usuario_id: int):
    try:
        usuario = usuario_service.get_user(usuario_id)
        return service.list_becas_for_user(usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/asignar", response_model=BecaSchema)
def asignar_beca(body: BecaAsignarSchema, admin_id: int):
    try:
        usuario_service.require_admin(admin_id)
        return service.asignar_beca(
            body.id_solicitante,
            body.categoria,
            body.estado,
            body.descripcion
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/resultado/{correo}", response_model=ResultadoBecaSchema)
def consultar_resultado(correo: str):
    resultado = service.resultado_por_correo(correo)
    if not resultado:
        raise HTTPException(status_code=404, detail="No hay una beca aprobada asociada a ese correo.")
    return resultado
