from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from  .models import *

class AccountAdmin(UserAdmin): 
    list_display= ('email', 'username', 'date_joined', 'plan')
    search_fields= ('email', 'username')
    readonly_fields= ('last_login', 'date_joined')

    filter_horizontal= ()
    list_filter=()
    fieldsets=()

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

admin.site.register(Account, AccountAdmin)

admin.site.register(Author)
admin.site.register(Gender)
admin.site.register(Editorial)


admin.site.register(CreditCards)
admin.site.register(Profile)

admin.site.register(UserSolicitud)

admin.site.register(StateOfBook)

admin.site.register(ExpirationDatesBillboard)
admin.site.register(UpDatesBillboard)
admin.site.register(Book)
admin.site.register(BookByChapter)
admin.site.register(Chapter)
admin.site.register(Billboard)

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(LikeComment)

admin.site.register(CounterStates)

admin.site.register(UpDates)
admin.site.register(ExpirationDates)