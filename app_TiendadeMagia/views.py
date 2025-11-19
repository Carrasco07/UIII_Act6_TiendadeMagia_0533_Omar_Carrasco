from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Empleado, Producto, Proveedor, OrdenDeVenta, DetalleOrden
from django.contrib.auth.models import User
from django.utils import timezone

def inicio(request):
    return render(request, 'app_TiendadeMagia/inicio.html')

# ==========================================
# VISTAS PARA CLIENTES (FUNCIONAL)
# ==========================================
def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_TiendadeMagia/cliente/ver_clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST['nombre'],
            email=request.POST['email'],
            telefono=request.POST['telefono'],
            direccion=request.POST['direccion'],
            rfc=request.POST.get('rfc', '')
        )
        return redirect('ver_clientes')
    return render(request, 'app_TiendadeMagia/cliente/agregar_cliente.html')

def actualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.email = request.POST['email']
        cliente.telefono = request.POST['telefono']
        cliente.direccion = request.POST['direccion']
        cliente.rfc = request.POST.get('rfc', '')
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'app_TiendadeMagia/cliente/actualizar_cliente.html', {'cliente': cliente})

def borrar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'app_TiendadeMagia/cliente/borrar_cliente.html', {'cliente': cliente})

# ==========================================
# VISTAS PARA EMPLEADOS (FUNCIONALES COMO CLIENTES)
# ==========================================
def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'app_TiendadeMagia/empleado/ver_empleados.html', {'empleados': empleados})

def agregar_empleado(request):
    if request.method == 'POST':
        # Crear usuario primero
        username = request.POST['email'].split('@')[0]
        user = User.objects.create_user(
            username=username,
            email=request.POST['email'],
            password='temp123',
            first_name=request.POST['nombre'].split()[0],
            last_name=' '.join(request.POST['nombre'].split()[1:]) if len(request.POST['nombre'].split()) > 1 else ''
        )
        
        # Crear empleado
        Empleado.objects.create(
            usuario=user,
            puesto=request.POST['puesto'],
            telefono=request.POST['telefono'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario']
        )
        return redirect('ver_empleados')
    return render(request, 'app_TiendadeMagia/empleado/agregar_empleado.html')

def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        # Actualizar usuario
        empleado.usuario.first_name = request.POST['nombre'].split()[0]
        empleado.usuario.last_name = ' '.join(request.POST['nombre'].split()[1:]) if len(request.POST['nombre'].split()) > 1 else ''
        empleado.usuario.email = request.POST['email']
        empleado.usuario.save()
        
        # Actualizar empleado
        empleado.puesto = request.POST['puesto']
        empleado.telefono = request.POST['telefono']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'app_TiendadeMagia/empleado/actualizar_empleado.html', {'empleado': empleado})

def borrar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        usuario = empleado.usuario
        empleado.delete()
        usuario.delete()
        return redirect('ver_empleados')
    return render(request, 'app_TiendadeMagia/empleado/borrar_empleado.html', {'empleado': empleado})

# ==========================================
# VISTAS PARA PRODUCTOS (FUNCIONALES)
# ==========================================
def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'app_TiendadeMagia/producto/ver_productos.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        proveedor = Proveedor.objects.get(id=proveedor_id) if proveedor_id else None
        
        Producto.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST.get('descripcion', ''),
            categoria=request.POST['categoria'],
            precio=request.POST['precio'],
            stock=request.POST['stock'],
            proveedor=proveedor
        )
        return redirect('ver_productos')
    
    proveedores = Proveedor.objects.all()
    return render(request, 'app_TiendadeMagia/producto/agregar_producto.html', {'proveedores': proveedores})

def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        producto.proveedor = Proveedor.objects.get(id=proveedor_id) if proveedor_id else None
        
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST.get('descripcion', '')
        producto.categoria = request.POST['categoria']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.save()
        return redirect('ver_productos')
    
    proveedores = Proveedor.objects.all()
    return render(request, 'app_TiendadeMagia/producto/actualizar_producto.html', {
        'producto': producto,
        'proveedores': proveedores
    })

def borrar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')
    return render(request, 'app_TiendadeMagia/producto/borrar_producto.html', {'producto': producto})

# ==========================================
# VISTAS PARA PROVEEDORES (FUNCIONALES)
# ==========================================
def ver_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'app_TiendadeMagia/proveedor/ver_proveedores.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre=request.POST['nombre'],
            contacto=request.POST['contacto'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            direccion=request.POST['direccion']
        )
        return redirect('ver_proveedores')
    return render(request, 'app_TiendadeMagia/proveedor/agregar_proveedor.html')

def actualizar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.contacto = request.POST['contacto']
        proveedor.telefono = request.POST['telefono']
        proveedor.email = request.POST['email']
        proveedor.direccion = request.POST['direccion']
        proveedor.save()
        return redirect('ver_proveedores')
    return render(request, 'app_TiendadeMagia/proveedor/actualizar_proveedor.html', {'proveedor': proveedor})

def borrar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('ver_proveedores')
    return render(request, 'app_TiendadeMagia/proveedor/borrar_proveedor.html', {'proveedor': proveedor})

# ==========================================
# VISTAS PARA ÓRDENES (BÁSICAS)
# ==========================================
def ver_ordenes(request):
    ordenes = OrdenDeVenta.objects.all()
    return render(request, 'app_TiendadeMagia/orden_venta/ver_ordenes.html', {'ordenes': ordenes})

def agregar_orden(request):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=request.POST['cliente'])
        empleado = get_object_or_404(Empleado, id=request.POST['empleado'])
        
        OrdenDeVenta.objects.create(
            cliente=cliente,
            empleado=empleado,
            direccion_envio=request.POST['direccion_envio'],
            metodo_pago=request.POST['metodo_pago'],
            estado=request.POST['estado'],
            comentarios=request.POST.get('comentarios', '')
        )
        return redirect('ver_ordenes')
    
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    return render(request, 'app_TiendadeMagia/orden_venta/agregar_orden.html', {
        'clientes': clientes,
        'empleados': empleados
    })

def actualizar_orden(request, id):
    orden = get_object_or_404(OrdenDeVenta, id=id)
    if request.method == 'POST':
        orden.direccion_envio = request.POST['direccion_envio']
        orden.metodo_pago = request.POST['metodo_pago']
        orden.estado = request.POST['estado']
        orden.comentarios = request.POST.get('comentarios', '')
        orden.save()
        return redirect('ver_ordenes')
    return render(request, 'app_TiendadeMagia/orden_venta/actualizar_orden.html', {'orden': orden})

def borrar_orden(request, id):
    orden = get_object_or_404(OrdenDeVenta, id=id)
    if request.method == 'POST':
        orden.delete()
        return redirect('ver_ordenes')
    return render(request, 'app_TiendadeMagia/orden_venta/borrar_orden.html', {'orden': orden})

# ==========================================
# VISTAS PARA DETALLES DE ORDEN (FALTANTES)
# ==========================================
def ver_detalles_orden(request):
    detalles = DetalleOrden.objects.all()
    return render(request, 'app_TiendadeMagia/detalle_orden/ver_detalles.html', {'detalles': detalles})

def agregar_detalle_orden(request):
    if request.method == 'POST':
        orden = get_object_or_404(OrdenDeVenta, id=request.POST['orden'])
        producto = get_object_or_404(Producto, id=request.POST['producto'])
        
        # Calcular subtotal automáticamente
        cantidad = int(request.POST['cantidad'])
        precio_unitario = float(request.POST['precio_unitario'])
        descuento = float(request.POST.get('descuento', 0))
        subtotal = (cantidad * precio_unitario) - descuento
        
        DetalleOrden.objects.create(
            orden=orden,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            descuento=descuento,
            subtotal=subtotal,
            observaciones=request.POST.get('observaciones', '')
        )
        return redirect('ver_detalles_orden')
    
    ordenes = OrdenDeVenta.objects.all()
    productos = Producto.objects.all()
    return render(request, 'app_TiendadeMagia/detalle_orden/agregar_detalle.html', {
        'ordenes': ordenes,
        'productos': productos
    })

def actualizar_detalle_orden(request, id):
    detalle = get_object_or_404(DetalleOrden, id=id)
    if request.method == 'POST':
        # Recalcular subtotal
        cantidad = int(request.POST['cantidad'])
        precio_unitario = float(request.POST['precio_unitario'])
        descuento = float(request.POST.get('descuento', 0))
        subtotal = (cantidad * precio_unitario) - descuento
        
        detalle.cantidad = cantidad
        detalle.precio_unitario = precio_unitario
        detalle.descuento = descuento
        detalle.subtotal = subtotal
        detalle.observaciones = request.POST.get('observaciones', '')
        detalle.save()
        return redirect('ver_detalles_orden')
    
    ordenes = OrdenDeVenta.objects.all()
    productos = Producto.objects.all()
    return render(request, 'app_TiendadeMagia/detalle_orden/actualizar_detalle.html', {
        'detalle': detalle,
        'ordenes': ordenes,
        'productos': productos
    })

def borrar_detalle_orden(request, id):
    detalle = get_object_or_404(DetalleOrden, id=id)
    if request.method == 'POST':
        detalle.delete()
        return redirect('ver_detalles_orden')
    return render(request, 'app_TiendadeMagia/detalle_orden/borrar_detalle.html', {'detalle': detalle})