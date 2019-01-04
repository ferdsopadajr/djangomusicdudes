from django.forms import *

class MainForm(Form):
	search = CharField(required = False, widget = TextInput(attrs = {'class' : 'form-control', 'label' : 'Search', 'placeholder' : 'Search'}))