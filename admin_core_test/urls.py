from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('comandas/', comandas, name='comandas'),
    path('home/', home, name='home'),
]