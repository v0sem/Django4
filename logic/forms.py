from django import forms
from datamodel.models import Move, Game
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator
from django.contrib.auth import password_validation, authenticate

from logic import tests_services

class SignupForm(forms.ModelForm):

    password = forms.CharField(label='Enter password', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Enter password again', required=True, widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password, 
                        password_validators=(MinimumLengthValidator(min_length=6), 
                                            NumericPasswordValidator(), 
                                            CommonPasswordValidator()))
        return password
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise ValidationError("Password and Repeat password are not the same|La clave y su repetición no coinciden")

        return password2

    def save(self):
        user = super(SignupForm, self).save()
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

class loginForm(AuthenticationForm):


    def is_valid(self):

        name = self.data['username']
        passw = self.data['password']

        if not User.objects.filter(username=name).exists():
            self.add_error(None, tests_services.SERVICE_DEF[tests_services.LOGIN_ERROR]['pattern'])
            return False
        
        if not authenticate(username=name, password=passw):
            self.add_error(None, tests_services.SERVICE_DEF[tests_services.LOGIN_ERROR]['pattern'])
            return False
        
        return super(loginForm, self).is_valid()
    

    class Meta:
        model = User
        fields = ('username', 'password')