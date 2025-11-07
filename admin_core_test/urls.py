from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('comandas/', home, name='comandas'),
    path('home/', home, name='home'),
]