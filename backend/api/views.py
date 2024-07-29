from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .controller import UsuarioController


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            usuario = UsuarioController.registrar_usuario(data)
            return JsonResponse({'message': 'Usuario registrado con éxito', 'id': usuario.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            usuario = data.get('usuario')
            contrasenia = data.get('contrasenia')
            usuario_obj = UsuarioController.autenticar_usuario(usuario, contrasenia)
            if usuario_obj:
                response_data = {
                    'token': 'fake-token',  # Aquí normalmente se devolvería un token real.
                    'user_id': usuario_obj.id
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class UsuarioPerfilView(View):
    def get(self, request, usuario_id):
        usuario = UsuarioController.obtener_usuario_por_id(usuario_id)
        if usuario:
            return JsonResponse({
                'id': usuario.id,
                'usuario': usuario.usuario,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'email': usuario.email,
                'sexo': usuario.sexo,
                'fecha_nacimiento': usuario.fecha_nacimiento,
                'ciudad_nacimiento': usuario.ciudad_nacimiento,
                'provincia_nacimiento': usuario.provincia_nacimiento
            })
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)


class UsuariosView(View):
    def get(self, request):
        usuarios = UsuarioController.obtener_todos_usuarios()
        usuarios_list = [{
            'id': usuario.id,
            'usuario': usuario.usuario,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido
        } for usuario in usuarios]
        return JsonResponse(usuarios_list, safe=False)