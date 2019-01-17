from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from overallsystem.modules.kmeans import cluster_points, read_file, preference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .forms import MainForm, CreateUserForm
from .models import *

@csrf_exempt
def account(request):
	return render(request, 'overallsystem/account.html')

def signup(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			profile = Profiles(user=user.username)
			profile.save()
			messages.success(request, 'Account created successfully!')
			return redirect('/login/')
	else:
		form = CreateUserForm()
	return render(request, 'overallsystem/login.html', {'form': form})

# def login(request):
# 	# kmc.map_to_mood()
# 	return render(request, 'overallsystem/login.html')

@login_required(redirect_field_name=None)
def main(request):
	songs = [track for track in read_file()]
	for track in songs:
		track = Tracks(track=track['id']).save()
	profile = Profiles.objects.get(user=request.user)
	rec_songs = []
	if profile.energy:
		rec_songs = cluster_points(preference=preference(profile, Profiles._meta.fields))
	if request.path == '/main/' or request.path == '/':
		return render(request, 'overallsystem/main.html', {'form': MainForm(), 'songs': songs, 'rec_songs': rec_songs, 'profile': Profiles.objects.get(user=request.user), 'fave': [obj.track.track for obj in Profiles.objects.get(user=request.user).userfaves_set.all()]})
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
def gen_rec(request):
	profile = Profiles.objects.get(user=request.user)
	rec_songs = cluster_points(track_id=request.POST['track_id'], preference=preference(profile, Profiles._meta.fields))
	print(rec_songs)
	return render(request, 'overallsystem/recommendations.html', {'rec_songs': rec_songs, 'profile': Profiles.objects.get(user=request.user)})

@csrf_exempt
def upd_cbl(request):
	track = read_file(request.POST['track_id'])
	if request.POST['past_track']:
		past_track = read_file(request.POST['past_track'])
		print(track['acousticness'], track['danceability'], track['energy'], track['instrumentalness'], track['key'], track['liveness'], track['loudness'], track['speechiness'], track['tempo'], track['valence'])
		# do preference mean computation here
	profile = Profiles(user=request.user, acousticness=track['acousticness'], danceability=track['danceability'], energy=track['energy'], instrumentalness=track['instrumentalness'], key=track['key'], liveness=track['liveness'], loudness=track['loudness'], speechiness=track['speechiness'], tempo=track['tempo'], valence=track['valence'])
	profile.save()
	return render(request, 'overallsystem/now-playing.html', {'track': track, 'fave': [obj.track.track for obj in Profiles.objects.get(user=request.user).userfaves_set.all()]})

@csrf_exempt
def add_to_fav(request):
	fave = UserFaves(user=Profiles.objects.get(user=request.user), track=Tracks.objects.get(track=request.POST['track_id']))
	fave.save()
	return HttpResponse()

@csrf_exempt
def del_to_fav(request):
	UserFaves.objects.filter(user=Profiles.objects.get(user=request.user), track=Tracks.objects.get(track=request.POST['track_id'])).delete()
	return HttpResponse()

@csrf_exempt
def favorites(request):
	fave = Profiles.objects.get(user=request.user).userfaves_set.all()
	songs = [obj.track.track for obj in fave]
	favorites = [read_file(track) for track in songs]
	return render(request, 'overallsystem/favorites.html', {'fave': favorites})