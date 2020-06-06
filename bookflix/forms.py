from django import forms
from .models import Account, CreditCards, Profile, ConfirmationMail
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms import ValidationError

class MailConfirmacion(forms.Form):
    codigoV = forms.CharField(label='codigo Validacion')


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

class MailChange(ModelForm):

    class Meta: 
        model = Account
        fields = ('email',)

    def clean_email(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            try:
                account= Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("el mail se encuentra en uso" )