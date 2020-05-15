from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm, RegistroTarjeta, CrearPerfil
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import shortcuts
from bookflix.models import Billboard, Profile, CreditCards, Account



def register_page(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        formCard = RegistroTarjeta(request.POST)
        formPerfil= CrearPerfil(request.POST)
        # Si el formulario es válido...
        if form.is_valid() and formCard.is_valid() and formPerfil.is_valid:

            # Creamos la nueva cuenta de usuario
            cuenta= form.save()
            id_account= form.cleaned_data.get('id')
            email= form.cleaned_data.get('email')
            raw_password= form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            
            instancia_tarjeta= formCard.save(commit=False)
            instancia_tarjeta.user = cuenta          
            instancia_tarjeta.save()
            
            perfil = formPerfil.save(commit=False)
            perfil.account = cuenta
            perfil.save()
            
            do_login(request, account )
            return redirect('/login')
        else:
            context["user_creation_form"]=form
            context["creacion_tarjeta"]= formCard
            context["profile_creation_form"]=formPerfil
    else:
        form=RegistrationForm()
        formCard=RegistroTarjeta()
        formPerfil= CrearPerfil()
        context["user_creation_form"]=form
        context["creacion_tarjeta"]=formCard
        context["profile_creation_form"]=formPerfil
    return render(request, 'bookflix/register_page.html', context)

def welcome(request):
    
    return render(request, "bookflix/welcome.html",) 

def barra(request):
    return render(request,"bookflix/barra.html", perfil)


def base(request):
    return render(request, "bookflix/base.html")

def perfil(request):
    #Para saber los datos del usuario tenes conectado que usar request.user."atributo"
    #tenes que arreglar todo ahi ese objeto perfil no va a funcionar
    publicacion=Account.objects.filter(username="julian")  #Retocar este parámetro para que agarre la variable del perfil actual y se se puede no de una puta lista
    perfil={"perfil":publicacion[0]}
    return render(request, "bookflix/perfil.html",perfil)

def publicaciones(request):
    publicacion=Billboard.objects.all()
    contexto={"publicaciones":publicacion}
    return render(request, "bookflix/publicaciones.html",contexto)


def publicacion(request):
    return render(request, "bookflix/publicacion.html")

def select_perfil(request):
    perfiles = Profile.objects.all()
    cuentaActualEmail = perfiles[0].account
    perfilActual = Account.objects.filter(email=cuentaActualEmail)[0]
    

    cuentaActual = request.user
    tarjetaActual = CreditCards.objects.filter(user_id=cuentaActual)[0]
    return render(request, "bookflix/select_perfil.html", {'perfiles': perfiles, "tarjetaActual": tarjetaActual, "perfilActual":perfilActual})

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
                return redirect('/select_perfil')

    # Si llegamos al final renderizamos el formulario
    return render(request, "bookflix/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')





# Desde acá van todos los "cambiar algo"

def cambiar_mail(request):

    return render(request, "bookflix/cambiar_mail.html")


def cambiar_tarjeta(request):

    return render(request, "bookflix/cambiar_tarjeta.html")


def cambiar_contraseña(request):

    return render(request, "bookflix/cambiar_contraseña.html")  

