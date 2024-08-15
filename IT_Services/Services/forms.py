from django import forms
from django.contrib.auth.models import User
from Services.models import Service

class serviceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name','payment_terms','price','package','tax','image','active']


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput)
