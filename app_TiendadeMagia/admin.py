from django.contrib import admin
from .models import Proveedor, Cliente, Empleado, Producto, OrdenDeVenta, DetalleOrden

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contacto', 'telefono', 'email']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'fecha_registro']

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'puesto', 'telefono', 'salario']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock']

@admin.register(OrdenDeVenta)
class OrdenDeVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'empleado', 'total', 'estado']

@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ['orden', 'producto', 'cantidad', 'subtotal']