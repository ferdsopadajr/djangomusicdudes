from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from overallsystem.modules.kmeans import cluster_points, read_file
from .forms import MainForm as mf

# Create your views here.
def login(request):
	# kmc.map_to_mood()
	return render(request, 'overallsystem/login.html')

def main(request):
	songs = [track for track in read_file()]
	rec_songs = []
	if request.path == '/main/':
		# if 'track_id' in request.GET:
			# rec_songs = cluster_points(request.GET['track_id'])
		rec_songs = cluster_points('2wYHz0GOHV49Xezd5mWTDP')
		return render(request, 'overallsystem/main.html', {'form': mf(), 'songs': songs, 'rec_songs': rec_songs})
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')