from django.forms import *

class MainForm(Form):
	track_id = CharField(label = 'Track ID Query')
	search = CharField(required = False, widget = TextInput(attrs = {'class' : 'form-control', 'label' : 'Search', 'placeholder' : 'Search'}))