from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_torneos, name='lista_torneos'),
    path('redireccion-rol/', views.redireccion_login, name='redireccion_rol'),
    path('inscribirse/<int:torneo_id>/', views.inscribirse, name='inscribirse'),
    path('cancelar/<int:torneo_id>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    path('mis-torneos/', views.mis_torneos, name='mis_torneos'),
    path('crear/', views.crear_torneo, name='crear_torneo'),
    path('inscritos/<int:torneo_id>/', views.ver_inscritos, name='ver_inscritos'),
    path('editar/<int:torneo_id>/', views.editar_torneo, name='editar_torneo'),
    path('eliminar/<int:torneo_id>/', views.eliminar_torneo, name='eliminar_torneo'),
    path('pago/<int:inscripcion_id>/', views.cambiar_pago, name='cambiar_pago'),
    path('eliminar-participante/<int:inscripcion_id>/', views.eliminar_participante, name='eliminar_participante'),
    path('ganador/<int:torneo_id>/<int:inscripcion_id>/', views.seleccionar_ganador, name='seleccionar_ganador'),
]