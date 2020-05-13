from django.urls import path
from .views import *

urlpatterns = [
    path('', welcome, name='welcome'),
    path('login', login_propio, name='login'),
    path('logout/', logout, name='logout'),#no se para que son los names pero por las duda los dejo
    path('register_page/', register_page, name='registrar'),
]

