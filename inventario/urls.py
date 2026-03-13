from django.urls import path
from . import views

urlpatterns = [
    path('venta/', views.crear_venta, name='crear_venta'),
]