from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register_page', views.register_page, name="register_page"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
