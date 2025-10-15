from django.urls import path
from . import views # Importa el módulo de vistas

urlpatterns = [
    # Asocia la ruta base ('') con la función clima_vista
    path('', views.clima_vista, name='clima'), 
]