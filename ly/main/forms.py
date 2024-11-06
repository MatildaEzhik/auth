from django.contrib.auth.forms import UserCreationForm
from django.forms import forms

from main.models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
