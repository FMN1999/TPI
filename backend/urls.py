from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),  # Rutas de la API de Django
    path('', TemplateView.as_view(template_name='static/dist/voley-app/browser/index.html')),  # Frontend Angular
]