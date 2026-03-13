from django.urls import path
from . import views

urlpatterns = [
    path('venta/', views.crear_venta, name='crear_venta'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket/<int:venta_id>/', views.ticket_pdf, name='ticket_pdf'),
]