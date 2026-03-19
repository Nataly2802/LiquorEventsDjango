from django.urls import path
from . import views
from .views import lista_ventas, detalle_venta, eliminar_venta, exportar_excel, reporte_pdf
urlpatterns = [
    path('venta/', views.crear_venta, name='crear_venta'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket/<int:venta_id>/', views.ticket_pdf, name='ticket_pdf'),
    path('ventas/', lista_ventas, name='lista_ventas'),
    path('ventas/<int:venta_id>/', detalle_venta, name='detalle_venta'),
    path('ventas/eliminar/<int:venta_id>/', eliminar_venta, name='eliminar_venta'),
    path('ventas/excel/', exportar_excel, name='exportar_excel'),
    path('ventas/pdf/', reporte_pdf, name='reporte_pdf'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('compras/', views.registrar_compra, name='registrar_compra'),
    path('compras/lista/', views.lista_compras, name='lista_compras'),
]