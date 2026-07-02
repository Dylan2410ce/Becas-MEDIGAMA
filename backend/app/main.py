from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import init_db
from app.controller.auth_controller import router as auth_router
from app.controller.beca_controller import router as beca_router
from app.controller.reporte_controller import router as reporte_router
from app.controller.solicitante_controller import router as solicitante_router
from app.controller.usuario_controller import router as usuario_router
from app.service.usuario_service import UsuarioService

app = FastAPI(title="BECAS MEDIGAMA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def seed_default_admin():
    service = UsuarioService()
    try:
        service.create_admin("Administrador Principal", "admin@medigama.com", "00000000", "12345")
    except ValueError:
        pass


seed_default_admin()
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(solicitante_router)
app.include_router(beca_router)
app.include_router(reporte_router)


@app.get("/")
def home():
    return {"message": "BECAS MEDIGAMA API activa"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
