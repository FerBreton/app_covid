from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('registro', Entrada.as_view(), name='registro'),
    path('historial', Historial.as_view(), name='historial'),
    path('resultados', Resultados.as_view(), name='resultados'),
]