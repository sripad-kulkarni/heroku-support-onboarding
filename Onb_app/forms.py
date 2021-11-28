from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .choices import ROLES
from django.forms.widgets import NumberInput

class UserRegisterForm(UserCreationForm):
	firstname = forms.CharField(max_length=100, required=True)
	lastname = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(required=True)
	role = forms.ChoiceField(choices=ROLES, required=True, widget=forms.Select(attrs={'id':'role'}))
	startdate = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=True)
	enddate = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=True)

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'firstname', 'lastname', 'email', 'role', 'startdate', 'enddate']
