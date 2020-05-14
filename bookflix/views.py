from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm, RegistroTarjeta
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import shortcuts
from bookflix.models import Billboard, Profile



def register_page(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        formCard = RegistroTarjeta(request.POST)
        # Si el formulario es válido...
        if form.is_valid() and formCard.is_valid():

            # Creamos la nueva cuenta de usuario
            cuenta= form.save()
            id_account= form.cleaned_data.get('id')
            email= form.cleaned_data.get('email')
            raw_password= form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            instancia_tarjeta= formCard.save(commit=False)
            instancia_tarjeta.user= cuenta          
            instancia_tarjeta.save()

            do_login(request, account )
            return redirect('/login')
        else:
            context["user_creation_form"]=form
            context["creacion_tarjeta"]= formCard
    else:
        form=RegistrationForm()
        formCard=RegistroTarjeta()
        context["user_creation_form"]=form
        context["creacion_tarjeta"]=formCard
    return render(request, 'bookflix/register_page.html', context)

def welcome(request):
    perrfil=Account.objects.filter(username="julian")  #Retocar este parámetro para que agarre la variable del perfil actual y se se puede no de una puta lista
    perfil={"perfil":perrfil[0]} 
    return render(request, "bookflix/welcome.html", perfil)

def barra(request):
    return render(request,"bookflix/barra.html", perfil)


def base(request):
    return render(request, "bookflix/base.html")

def perfil(request):
    publicacion=Account.objects.filter(username="julian")  #Retocar este parámetro para que agarre la variable del perfil actual y se se puede no de una puta lista
    perfil={"perfil":publicacion[0]}
    return render(request, "bookflix/perfil.html",perfil)

def publicaciones(request):
    publicacion=Billboard.objects.all()
    contexto={"publicaciones":publicacion}
    return render(request, "bookflix/publicaciones.html",contexto)


def publicacion(request):
    return render(request, "bookflix/publicacion.html")






"""def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
    if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            redirect('/')
    else:
        form = RegistrationForm()

        args = {'form': form, }
        return render(request, 'register_page.html', args)"""

def login_propio(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "bookflix/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

