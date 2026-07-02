from app.repository.solicitante_repository import SolicitanteRepository
from app.repository.usuario_repository import UsuarioRepository


class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()
        self.solicitante_repo = SolicitanteRepository()

    def _validate_text(self, value, field_name, min_len=2):
        if value is None or value.strip() == "":
            raise ValueError(f"{field_name} no puede estar vacio.")
        if len(value.strip()) < min_len:
            raise ValueError(f"{field_name} debe tener al menos {min_len} caracteres.")

    def _validate_correo(self, correo):
        correo = correo.strip().lower()
        if correo == "":
            raise ValueError("El correo no puede estar vacio.")
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise ValueError("El correo no tiene un formato valido.")
        return correo

    def _validate_user(self, nombre, correo, telefono, contrasena, rol):
        self._validate_text(nombre, "El nombre")
        correo = self._validate_correo(correo)
        self._validate_text(telefono, "El telefono", 7)
        self._validate_text(contrasena, "La contrasena", 4)
        if rol not in ["admin", "estudiante"]:
            raise ValueError("El rol no es permitido.")
        return nombre.strip(), correo, telefono.strip(), contrasena.strip()

    def create_student(self, nombre, correo, telefono, contrasena):
        return self._create_user(nombre, correo, telefono, contrasena, "estudiante")

    def create_admin(self, nombre, correo, telefono, contrasena):
        return self._create_user(nombre, correo, telefono, contrasena, "admin")

    def _create_user(self, nombre, correo, telefono, contrasena, rol):
        nombre, correo, telefono, contrasena = self._validate_user(
            nombre, correo, telefono, contrasena, rol
        )

        if self.repo.get_by_correo(correo):
            raise ValueError("El correo ya esta registrado.")

        return self.repo.create(nombre, correo, telefono, contrasena, rol)

    def update_user(self, user_id, nombre, correo, telefono):
        usuario_actual = self.repo.get(user_id)
        if not usuario_actual:
            raise ValueError("Usuario no encontrado.")

        self._validate_text(nombre, "El nombre")
        correo = self._validate_correo(correo)
        self._validate_text(telefono, "El telefono", 7)

        existente = self.repo.get_by_correo(correo)
        if existente and existente.id != user_id:
            raise ValueError("El correo ya esta registrado por otro usuario.")

        usuario = self.repo.update(user_id, nombre.strip(), correo, telefono.strip())
        solicitante = self.solicitante_repo.get_by_usuario(user_id)
        if solicitante:
            self.solicitante_repo.update(solicitante, {
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "telefono": usuario.telefono
            })
        return usuario

    def get_user(self, user_id):
        usuario = self.repo.get(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        return usuario

    def require_admin(self, admin_id):
        usuario = self.get_user(admin_id)
        if usuario.rol != "admin":
            raise PermissionError("Solo administradores pueden realizar esta accion.")
        return usuario

    def recover_password(self, correo, nueva_contrasena):
        correo = self._validate_correo(correo)
        self._validate_text(nueva_contrasena, "La nueva contrasena", 4)

        usuario = self.repo.get_by_correo(correo)
        if not usuario:
            raise ValueError("No existe un usuario con ese correo.")
        if usuario.rol != "estudiante":
            raise ValueError("La recuperacion desde login solo esta disponible para solicitantes.")

        return self.repo.update_password(correo, nueva_contrasena.strip())

    def list_users(self):
        return self.repo.get_all()

    def list_admins(self):
        return self.repo.get_by_rol("admin")
