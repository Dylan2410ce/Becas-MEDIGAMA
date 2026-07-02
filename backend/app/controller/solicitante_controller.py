from fastapi import APIRouter, HTTPException

from app.schemas.solicitante_schema import SolicitudBecaSchema, SolicitanteSchema
from app.service.solicitante_service import SolicitanteService
from app.service.usuario_service import UsuarioService

router = APIRouter(prefix="/solicitantes", tags=["Solicitantes"])
service = SolicitanteService()
usuario_service = UsuarioService()


@router.post("/mi-solicitud", response_model=SolicitanteSchema)
def solicitar_beca(body: SolicitudBecaSchema, usuario_id: int):
    try:
        usuario = usuario_service.get_user(usuario_id)
        return service.create_or_update_request(usuario, body)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mi-solicitud", response_model=SolicitanteSchema | None)
def obtener_mi_solicitud(usuario_id: int):
    try:
        usuario = usuario_service.get_user(usuario_id)
        return service.get_my_request(usuario)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[SolicitanteSchema])
def listar_solicitantes(admin_id: int):
    try:
        usuario_service.require_admin(admin_id)
        return service.list_solicitantes()
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{solicitante_id}", response_model=SolicitanteSchema)
def buscar_solicitante(solicitante_id: int, admin_id: int):
    try:
        usuario_service.require_admin(admin_id)
        solicitante = service.get_solicitante(solicitante_id)
        if not solicitante:
            raise HTTPException(status_code=404, detail="Solicitante no encontrado.")
        return solicitante
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
