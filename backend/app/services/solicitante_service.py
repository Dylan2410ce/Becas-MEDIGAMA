from app.repository.solicitante_repository import SolicitanteRepository


class SolicitanteService:
    def __init__(self):
        self.repo = SolicitanteRepository()

    def _validate_options(self, value, allowed, field):
        value = value.strip()
        if value not in allowed:
            raise ValueError(f"{field} no es valido.")
        return value

    def _validate_text(self, value, field_name, min_len=2):
        if value is None or value.strip() == "":
            raise ValueError(f"{field_name} no puede estar vacio.")
        if len(value.strip()) < min_len:
            raise ValueError(f"{field_name} debe tener al menos {min_len} caracteres.")
        return value.strip()

    def _calculate_score(self, ingresos, gastos, dependientes, miembros_hogar, promedio, vivienda, trabaja, transporte, condicion_especial, situacion_especial):
        liquidez = ingresos - gastos
        score = 0

        if liquidez <= 100000:
            score += 45
        elif liquidez <= 200000:
            score += 32
        elif liquidez <= 350000:
            score += 18
        else:
            score += 8

        score += min(dependientes * 7, 28)
        score += min(miembros_hogar * 2, 12)

        if vivienda == "Alquilada":
            score += 12
        elif vivienda == "Prestada":
            score += 16

        if trabaja == "No":
            score += 8

        if transporte in ["Bus", "Beca transporte"]:
            score += 6

        if condicion_especial in ["Discapacidad", "Enfermedad", "Cuido familiar", "Desempleo familiar"]:
            score += 12

        if promedio >= 90:
            score += 10
        elif promedio >= 80:
            score += 6

        if situacion_especial and len(situacion_especial.strip()) >= 8:
            score += 10

        return min(score, 100)

    def _suggest_category(self, score):
        if score >= 85:
            return "Beca 5"
        if score >= 70:
            return "Beca 4"
        if score >= 55:
            return "Beca 3"
        if score >= 40:
            return "Beca 2"
        return "Beca 1"

    def create_or_update_request(self, usuario, data):
        if usuario.rol != "estudiante":
            raise PermissionError("Solo los solicitantes pueden crear su propia solicitud.")

        edad = int(data.edad)
        provincia = self._validate_text(data.provincia, "La provincia")
        canton = self._validate_text(data.canton, "El canton")
        universidad = self._validate_text(data.universidad, "La universidad")
        carrera = self._validate_text(data.carrera, "La carrera")
        nivel = self._validate_options(data.nivel, ["Diplomado", "Bachillerato", "Licenciatura"], "El nivel")
        ingresos = float(data.ingresos)
        gastos = float(data.gastos)
        dependientes = int(data.dependientes)
        miembros_hogar = int(data.miembros_hogar)
        promedio = float(data.promedio)
        vivienda = self._validate_options(data.vivienda, ["Propia", "Alquilada", "Prestada"], "La vivienda")
        trabaja = self._validate_options(data.trabaja, ["Si", "No"], "El campo trabaja")
        transporte = self._validate_options(data.transporte, ["Propio", "Bus", "Beca transporte"], "El transporte")
        condicion_especial = self._validate_options(
            data.condicion_especial,
            ["Ninguna", "Discapacidad", "Enfermedad", "Cuido familiar", "Desempleo familiar"],
            "La condicion especial"
        )
        situacion_especial = (data.situacion_especial or "").strip()

        if edad < 15 or edad > 80:
            raise ValueError("La edad debe estar entre 15 y 80.")
        if ingresos < 0 or gastos < 0:
            raise ValueError("Ingresos y gastos no pueden ser negativos.")
        if gastos > ingresos:
            raise ValueError("Los gastos no pueden ser mayores que los ingresos.")
        if dependientes < 0 or dependientes > 12:
            raise ValueError("La cantidad de dependientes no es valida.")
        if miembros_hogar <= 0 or miembros_hogar > 20:
            raise ValueError("La cantidad de miembros del hogar no es valida.")
        if promedio < 0 or promedio > 100:
            raise ValueError("El promedio debe estar entre 0 y 100.")

        score = self._calculate_score(
            ingresos, gastos, dependientes, miembros_hogar, promedio, vivienda,
            trabaja, transporte, condicion_especial, situacion_especial
        )
        categoria = self._suggest_category(score)

        payload = {
            "usuario_id": usuario.id,
            "nombre": usuario.nombre,
            "telefono": usuario.telefono,
            "correo": usuario.correo,
            "edad": edad,
            "provincia": provincia,
            "canton": canton,
            "universidad": universidad,
            "carrera": carrera,
            "nivel": nivel,
            "ingresos": ingresos,
            "gastos": gastos,
            "dependientes": dependientes,
            "miembros_hogar": miembros_hogar,
            "promedio": promedio,
            "vivienda": vivienda,
            "trabaja": trabaja,
            "transporte": transporte,
            "condicion_especial": condicion_especial,
            "situacion_especial": situacion_especial,
            "indice_vulnerabilidad": score,
            "categoria_sugerida": categoria,
            "estado_solicitud": "En revision"
        }

        solicitante = self.repo.get_by_usuario(usuario.id)
        if solicitante:
            return self.repo.update(solicitante, payload)
        return self.repo.create(payload)

    def update_estado(self, solicitante, estado):
        return self.repo.update(solicitante, {"estado_solicitud": estado})

    def get_my_request(self, usuario):
        if usuario.rol != "estudiante":
            raise PermissionError("Solo los solicitantes pueden consultar este apartado.")
        return self.repo.get_by_usuario(usuario.id)

    def get_solicitante(self, solicitante_id):
        return self.repo.get(solicitante_id)

    def get_by_usuario(self, usuario_id):
        return self.repo.get_by_usuario(usuario_id)

    def get_by_correo(self, correo):
        return self.repo.get_by_correo(correo.strip().lower())

    def list_solicitantes(self):
        return self.repo.get_all()
