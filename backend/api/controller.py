from .db import UsuarioData


class UsuarioController:
    @staticmethod
    def iniciar_sesion(usuario, contrasenia):
        usuario_obj = UsuarioData.obtener_usuario_por_usuario(usuario)
        if usuario_obj and usuario_obj.contrasenia == contrasenia:
            return usuario_obj
        return None

    @staticmethod
    def registrar_usuario(data):
        usuario = UsuarioData.crear_usuario(data)
        tipo_usuario = data.get('tipo_usuario')
        if tipo_usuario == 'Asistente':
            UsuarioData.crear_asistente(usuario.id)
        elif tipo_usuario == 'DT':
            telefono = data.get('telefono')
            UsuarioData.crear_dt(usuario.id, telefono)
        elif tipo_usuario == 'Jugador':
            altura = data.get('altura')
            peso = data.get('peso')
            UsuarioData.crear_jugador(usuario.id, altura, peso)
        return usuario

    @staticmethod
    def autenticar_usuario(usuario, contrasenia):
        return UsuarioData.obtener_usuario_por_usuario_y_contrasenia(usuario, contrasenia)

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        return UsuarioData.obtener_usuario_por_id(usuario_id)

    @staticmethod
    def buscar_usuarios(query):
        return UsuarioData.buscar_usuarios(query)

    @staticmethod
    def obtener_todos_usuarios():
        # Obtén todos los usuarios desde la base de datos
        usuarios = UsuarioData.GetAll()
        return usuarios