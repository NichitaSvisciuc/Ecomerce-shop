from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm 

from django import forms
from .models import *

class UserRegisterForm(UserCreationForm):

	class Meta:
		model = User

		widgets = {
			'username' : forms.TextInput(attrs={'class': 'input-group'}),
			'password1' : forms.TextInput(attrs={'class': 'input-group'}),
			'password2' : forms.TextInput(attrs={'class': 'input-group'}),
		}

		fields = ['username', 'password1', 'password2'] 