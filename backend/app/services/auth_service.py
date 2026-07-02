from app.repository.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def login(self, correo, contrasena):
        correo = correo.strip().lower()
        contrasena = contrasena.strip()

        if correo == "" or contrasena == "":
            raise ValueError("Correo y contrasena son obligatorios.")

        usuario = self.repo.get_by_correo(correo)
        if not usuario or usuario.contrasena != contrasena:
            raise ValueError("Credenciales incorrectas.")

        return usuario
