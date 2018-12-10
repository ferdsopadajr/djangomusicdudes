from django.shortcuts import render
from django.http import HttpResponse
import overallsystem.modules.kmeans as kmc
from .forms import MainForm as mf

# Create your views here.
def login(request):
	# kmc.map_to_mood()
	return render(request, 'overallsystem/login.html')

def main(request):
	# Do clustering if k value exists
	if 'k_value' and 'track_id' in request.GET:
		kmc.cluster_points(int(request.GET['k_value']), request.GET['track_id'])
		# add return statement here
	return render(request, 'overallsystem/main.html', {'form' : mf()})
