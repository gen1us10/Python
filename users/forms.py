from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
