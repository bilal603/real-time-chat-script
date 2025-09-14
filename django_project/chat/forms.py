from django import forms
from django.contrib.auth.models import User

class CustomSignupForm(forms.ModelForm):
    name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('name', 'last_name', 'email')
