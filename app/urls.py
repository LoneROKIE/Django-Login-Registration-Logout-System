# aqui van la urls de mi aplicacion
from django.urls import path # importamos la funcion path
from .  import views # importamos el archivo views.py

urlpatterns = [
    path('', views.home, name='home'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('iniciar_sesion/', views.iniciar_sesion, name="iniciar_sesion"),
    path('pagina_privada/', views.pagina_privada, name="pagina_privada"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('activar_cuenta/<uidb64>/<token>', views.activar_cuenta, name="activar_cuenta")
]
