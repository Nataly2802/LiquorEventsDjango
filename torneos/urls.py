from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_torneos, name='lista_torneos'),
]
