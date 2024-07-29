from .models import Usuario, Asistente, DT, Jugador


class UsuarioData:
    @staticmethod
    def obtener_usuario_por_usuario(usuario):
        try:
            return Usuario.objects.get(usuario=usuario)
        except Usuario.DoesNotExist:
            return None

    def crear_usuario(data):
        usuario = Usuario(
            fecha_nacimiento=data.get('fecha_nacimiento'),
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            ciudad_nacimiento=data.get('ciudad_nacimiento'),
            provincia_nacimiento=data.get('provincia_nacimiento'),
            email=data.get('email'),
            usuario=data.get('usuario'),
            contrasenia=data.get('contrasenia'),
            sexo=data.get('sexo')
        )
        usuario.save()
        return usuario

    @staticmethod
    def crear_asistente(id_usuario):
        asistente = Asistente(id_usuario=id_usuario)
        asistente.save()
        return asistente

    @staticmethod
    def crear_dt(id_usuario, telefono):
        dt = DT(id_usuario=id_usuario, telefono=telefono)
        dt.save()
        return dt

    @staticmethod
    def crear_jugador(id_usuario, altura, peso):
        jugador = Jugador(id_usuario=id_usuario, altura=altura, peso=peso)
        jugador.save()
        return jugador

    @staticmethod
    def obtener_usuario_por_usuario_y_contrasenia(usuario, contrasenia):
        try:
            return Usuario.objects.get(usuario=usuario, contrasenia=contrasenia)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def buscar_usuarios(query):
        return Usuario.objects.filter(nombre__icontains=query) | Usuario.objects.filter(apellido__icontains=query)

    @classmethod
    def GetAll(cls):
        usuarios = Usuario.objects.all()
        return usuarios