from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_torneos, name='lista_torneos'),
    path('inscribirse/<int:torneo_id>/', views.inscribirse, name='inscribirse'),
    path('mis-torneos/', views.mis_torneos, name='mis_torneos'),
]