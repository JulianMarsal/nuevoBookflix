from django.urls import path
from .views import *

urlpatterns = [
    path('', welcome, name='welcome'),
    path('login', login, name='login'),
    path('logout/', logout, name='logout'),#no se para que son los names pero por las duda los dejo
    path('register/', register),
]

