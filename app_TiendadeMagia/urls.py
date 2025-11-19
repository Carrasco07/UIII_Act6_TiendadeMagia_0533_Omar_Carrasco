from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Clientes
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/actualizar/<int:id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/borrar/<int:id>/', views.borrar_cliente, name='borrar_cliente'),
    
    # Empleados
    path('empleados/', views.ver_empleados, name='ver_empleados'),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/actualizar/<int:id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/borrar/<int:id>/', views.borrar_empleado, name='borrar_empleado'),
    
    # Productos
    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/actualizar/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/borrar/<int:id>/', views.borrar_producto, name='borrar_producto'),
    
    # Proveedores
    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:id>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/borrar/<int:id>/', views.borrar_proveedor, name='borrar_proveedor'),
    
    # Órdenes
    path('ordenes/', views.ver_ordenes, name='ver_ordenes'),
    path('ordenes/agregar/', views.agregar_orden, name='agregar_orden'),
    path('ordenes/actualizar/<int:id>/', views.actualizar_orden, name='actualizar_orden'),
    path('ordenes/borrar/<int:id>/', views.borrar_orden, name='borrar_orden'),

    # Detalles de Orden
path('detalles-orden/', views.ver_detalles_orden, name='ver_detalles_orden'),
path('detalles-orden/agregar/', views.agregar_detalle_orden, name='agregar_detalle_orden'),
path('detalles-orden/actualizar/<int:id>/', views.actualizar_detalle_orden, name='actualizar_detalle_orden'),
path('detalles-orden/borrar/<int:id>/', views.borrar_detalle_orden, name='borrar_detalle_orden'),

]