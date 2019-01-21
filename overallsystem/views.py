from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from overallsystem.modules.kmeans import plot_points, cluster_points, read_file, preference, determine_mood
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
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
@csrf_exempt
def main(request):
	songs = [read_file(track.track) for track in Tracks.objects.all().order_by('-listens')]
	# Uncomment this to add the tracks to database
	# for track in songs:
	# 	track = Tracks(track=track['id']).save()
	profile = Profiles.objects.get(user=request.user)
	pref = preference(profile, Profiles._meta.fields)
	mood = ''
	rec_songs = []
	if profile.energy:
		mood = determine_mood(pref)['mood']
		rec_songs = cluster_points(preference=pref)
	if request.path == '/main/' or request.path == '/':
		return render(request, 'overallsystem/main.html', {'form': MainForm(), 'songs': songs, 'mood': mood, 'track': Tracks.objects.all(), 'rec_songs': rec_songs, 'profile': profile, 'fave': [obj.track.track for obj in profile.userfaves_set.all()]})
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
def browse(request):
	profile = Profiles.objects.get(user=request.user)
	songs = [read_file(track.track) for track in Tracks.objects.all().order_by('-listens')]
	return render(request, 'overallsystem/browse.html', {'songs': songs, 'track': Tracks.objects.all(), 'fave': [obj.track.track for obj in profile.userfaves_set.all()]})

@csrf_exempt
def gen_rec(request):
	profile = Profiles.objects.get(user=request.user)
	mood = determine_mood(read_file(request.POST['track_id']))['mood']
	rec_songs = cluster_points(track_id=request.POST['track_id'], preference=preference(profile, Profiles._meta.fields))
	return render(request, 'overallsystem/recommendations.html', {'rec_songs': rec_songs, 'mood': mood, 'profile': profile})

@csrf_exempt
def backend_process(request):
	return render(request, 'overallsystem/backend_process.html', {'track_id': request.POST['track_id']})

@csrf_exempt
def duration(request):
	if request.POST['track_id']:
		if request.POST['past_track'] and request.POST['listening_duration']:
			userlistens = UserListens(user=Profiles.objects.get(user=request.user), track=Tracks.objects.get(track=request.POST['past_track']))
		track = read_file(request.POST['track_id'], False)
		return HttpResponse(int(track['duration_ms']))
	else:
		return HttpResponse()

@csrf_exempt
def convert_time(request):
	return HttpResponse(datetime.fromtimestamp(int(request.POST['play_duration'])/1000).strftime('%#M:%S'))

@csrf_exempt
def compute_pref_mean(request):
	# do preference mean computation here
	pass

@csrf_exempt
def upd_cbl(request):
	# listens computation
	# listens = Tracks(track=request.POST['track_id'], listens=Tracks.objects.get(track=request.POST['track_id']).listens+1).save()
	track = read_file(request.POST['track_id'])
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