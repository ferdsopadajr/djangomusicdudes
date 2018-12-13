from django import forms

class MainForm(forms.Form):
	track_id = forms.CharField(label = 'Track ID Query')