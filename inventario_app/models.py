from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nombre)


class Producto(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=60)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio_compra = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)
    precio_venta = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

    def get_absolute_url(self):
        return reverse('detalle_producto', kwargs={'pk': self.pk})

    @property
    def valor_stock(self):
        return self.cantidad * self.precio_compra


class MovimientoProducto(models.Model):
    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

    @property
    def subtotal_movimiento(self):
        try:
            # Si el precio o la cantidad están vacíos, usamos 0 por defecto
            precio = self.producto.precio_venta or 0
            cantidad = self.cantidad or 0

            return precio * cantidad
        except Exception:
            # Si ocurre CUALQUIER error matemático, devolvemos 0 en lugar de romper la página
            return 0
