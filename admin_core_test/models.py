# admin_core_test/models.py
from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    mesa = models.CharField(max_length=50)
    mesero = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
