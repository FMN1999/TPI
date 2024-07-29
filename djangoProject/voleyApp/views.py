from django.http import HttpResponse
from django.template import loader
from controllers.controllers import UsuarioController


def usuarios(request):
    usuario_controller = UsuarioController()  # Instanciar la clase
    misusuarios = usuario_controller.GetUsuarios()  # Llamar al método de instancia
    template = loader.get_template('Todos los usuarios.html')
    context = {
        'misusuarios': misusuarios,
    }
    return HttpResponse(template.render(context, request))


def usuario(request, id: int):
    usuario_controller = UsuarioController()
    miusuario = usuario_controller.GetUsuario(id)
    template = loader.get_template('Usuarios detalles.html')
    context = {
        'miusuario': miusuario,
    }
    return HttpResponse(template.render(context, request))


def lista_usuarios(request):
    template = loader.get_template('ListaUsuarios.html')
    return HttpResponse(template.render())


def testing(request):
    template = loader.get_template('Template.html')
    context = {
        'firstname': 'Linus',
    }
    return HttpResponse(template.render(context, request))
