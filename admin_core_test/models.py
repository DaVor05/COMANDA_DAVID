from django.db import models
from django.contrib.auth.models import User



class Comanda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.IntegerField()
    comanda = models.TextField()
    detalle = models.CharField(max_length=50)

class Mesa(models.Model):
    mesa = models.IntegerField()
    cliente = models.CharField(max_length=100)
    capacidad = models.IntegerField()

class Pago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.IntegerField()
    cliente = models.CharField(max_length=100)
    pago = models.FloatField()

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100)
    pago = models.FloatField()
    nombre = models.CharField(max_length=100)
    

