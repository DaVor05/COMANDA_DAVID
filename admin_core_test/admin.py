# admin_core_test/admin.py
from django.contrib import admin
from .models import Categoria, Producto, Pedido, PedidoItem

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
