# admin_core_test/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('comandas/', views.comandas, name='comandas'),
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),

    
    path('pedido/<int:pedido_id>/pdf/', views.pedido_pdf, name='pedido_pdf'),
]
    