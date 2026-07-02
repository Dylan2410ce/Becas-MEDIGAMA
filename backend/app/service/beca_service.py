from app.repository.beca_repository import BecaRepository
from app.repository.solicitante_repository import SolicitanteRepository
from app.schemas.beca_schema import ALLOWED_CATEGORIAS, ALLOWED_ESTADOS


class BecaService:
    PRESUPUESTO_MAXIMO = 2500000.0

    def __init__(self):
        self.repo = BecaRepository()
        self.solicitante_repo = SolicitanteRepository()

    def asignar_beca(self, id_solicitante, categoria, estado="Aprobado", descripcion=""):
        categoria = categoria.strip()
        estado = estado.strip()
        descripcion = descripcion.strip()

        if not descripcion:
            raise ValueError("Debe indicar una descripcion de la decision.")
        if estado not in ALLOWED_ESTADOS:
            raise ValueError("El estado no es permitido.")

        solicitante = self.solicitante_repo.get(id_solicitante)
        if not solicitante:
            raise ValueError("El solicitante no existe.")

        montos = {
            "Beca 1": 45000.0,
            "Beca 2": 70000.0,
            "Beca 3": 90000.0,
            "Beca 4": 120000.0,
            "Beca 5": 150000.0
        }

        if estado == "Aprobado":
            if categoria not in ALLOWED_CATEGORIAS:
                raise ValueError("La categoria no es permitida.")
            monto_total = montos[categoria]
            self._validate_budget(id_solicitante, monto_total)
            nuevo_estado = "Aprobado"
        elif estado == "Rechazado":
            categoria = "Ninguna"
            monto_total = 0.0
            nuevo_estado = "Rechazado"
        else:
            categoria = "Por asignar"
            monto_total = 0.0
            nuevo_estado = "En revision"

        self.solicitante_repo.update(solicitante, {"estado_solicitud": nuevo_estado})
        return self.repo.create_or_update(id_solicitante, categoria, monto_total, estado, descripcion)

    def _validate_budget(self, id_solicitante, nuevo_monto):
        reporte = self.repo.total_aprobado()
        beca_actual = self.repo.get_by_solicitante(id_solicitante)
        monto_actual = beca_actual.monto_total if beca_actual and beca_actual.estado == "Aprobado" else 0
        total_estimado = reporte["monto_total"] - monto_actual + nuevo_monto
        if total_estimado > self.PRESUPUESTO_MAXIMO:
            raise ValueError("No hay presupuesto disponible para aprobar esta beca.")

    def get_beca_by_solicitante(self, id_solicitante):
        return self.repo.get_by_solicitante(id_solicitante)

    def list_becas(self):
        return self.repo.get_all()

    def list_becas_for_user(self, usuario):
        if usuario.rol == "admin":
            return self.list_becas()

        solicitante = self.solicitante_repo.get_by_usuario(usuario.id)
        if not solicitante:
            return []

        beca = self.get_beca_by_solicitante(solicitante.id)
        return [beca] if beca else []

    def resultado_por_correo(self, correo):
        solicitante = self.solicitante_repo.get_by_correo(correo.strip().lower())
        if not solicitante:
            return None

        beca = self.repo.get_by_solicitante(solicitante.id)
        if not beca or beca.estado != "Aprobado":
            return None

        return {
            "id_solicitud": f"SOL-{solicitante.id:05d}",
            "id_solicitante": solicitante.id,
            "estudiante": solicitante.nombre,
            "tipo": "Socioeconomica",
            "categoria": beca.categoria,
            "monto": beca.monto_total,
            "estado": beca.estado,
            "descripcion": beca.descripcion
        }

    def reporte_gasto_total(self):
        reporte = self.repo.total_aprobado()
        reporte["presupuesto_maximo"] = self.PRESUPUESTO_MAXIMO
        reporte["presupuesto_disponible"] = self.PRESUPUESTO_MAXIMO - reporte["monto_total"]
        return reporte

    def reporte_por_categoria(self):
        return self.repo.count_by_categoria()

    def reporte_por_estado(self):
        return self.repo.count_by_estado()
