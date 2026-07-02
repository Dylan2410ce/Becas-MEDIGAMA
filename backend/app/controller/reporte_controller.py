from fastapi import APIRouter, HTTPException

from app.service.beca_service import BecaService
from app.service.usuario_service import UsuarioService

router = APIRouter(prefix="/reportes", tags=["Reportes"])
service = BecaService()
usuario_service = UsuarioService()


@router.get("/gasto-total")
def gasto_total(admin_id: int):
    try:
        usuario_service.require_admin(admin_id)
        return service.reporte_gasto_total()
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/por-categoria")
def por_categoria(admin_id: int):
    try:
        usuario_service.require_admin(admin_id)
        return service.reporte_por_categoria()
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/por-estado")
def por_estado(admin_id: int):
    try:
        usuario_service.require_admin(admin_id)
        return service.reporte_por_estado()
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
