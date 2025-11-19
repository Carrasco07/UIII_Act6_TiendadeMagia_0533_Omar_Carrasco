from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_registro = models.DateField(auto_now_add=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_contratacion = models.DateField(default=timezone.now)
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

class Producto(models.Model):
    CATEGORIAS = [
        ('varitas', 'Varitas Mágicas'),
        ('pociones', 'Pociones'),
        ('libros', 'Libros de Hechizos'),
        ('accesorios', 'Accesorios Mágicos'),
        ('ingredientes', 'Ingredientes Mágicos'),
    ]
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class OrdenDeVenta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('paypal', 'PayPal'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    fecha_orden = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.CharField(max_length=500)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, default='efectivo')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente.nombre}"

class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenDeVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.subtotal = (self.precio_unitario * self.cantidad) - self.descuento
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"