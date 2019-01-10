from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MainForm(Form):
	search = CharField(required=False, widget=TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Search'}))

class CreateUserForm(UserCreationForm):
	username = CharField(required=True, widget=TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}))
	password1 = CharField(required=True, widget=PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password'}))
	password2 = CharField(required=True, widget=PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Confirm Password'}))
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')