from django import forms
from .models import Account, CreditCards, Profile
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class RegistroTarjeta(ModelForm):

    class Meta:
        model = CreditCards

        fields = ('number','cod','card_name','date_expiration','bank',)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Account
        fields = (  
            'username',
            'email',
            'password1',
            'password2',            
        )

class CrearPerfil(ModelForm):
    class Meta: 
        model = Profile
        fields = ('name',)