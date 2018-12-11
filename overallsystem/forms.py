from django import forms

class MainForm(forms.Form):
	k_value = forms.IntegerField(label = 'Number of Clusters', initial = 2, min_value = 2, max_value = 15)
	track_id = forms.CharField(label = 'Track ID')