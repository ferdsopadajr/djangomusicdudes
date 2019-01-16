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
	profile = Profiles.objects.get(user=request.user)
	if profile.pref_mean_energy:
		rec_songs = cluster_points(query=preference(profile, Profiles._meta.fields))
		print(rec_songs)	
	if request.path == '/main/' or request.path == '/':
		return render(request, 'overallsystem/main.html', {'form': MainForm(), 'songs': songs, 'profile': Profiles.objects.get(user=request.user), 'fave': [obj.track.track for obj in Profiles.objects.get(user=request.user).userfaves_set.all()]})
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
def gen_rec(request):
	profile = Profiles.objects.get(user=request.user)
	rec_songs = cluster_points(request.POST['track_id'], profile.pref_mean_x, profile.pref_mean_y)
	return render(request, 'overallsystem/recommendations.html', {'rec_songs': rec_songs, 'profile': Profiles.objects.get(user=request.user)})

@csrf_exempt
def upd_cbl(request):
	track = read_file(request.POST['track_id'])
	if request.POST['past_track']:
		past_track = read_file(request.POST['past_track'])
		print(past_track['valence'], past_track['energy'])
	profile = Profiles(user=request.user, pref_mean_x=track['valence'], pref_mean_y=track['energy'])
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
	for track in favorites:
		track['duration_ms'] = datetime.fromtimestamp(int(track['duration_ms'])/1000).strftime('%#M:%S')
	print(favorites)
	return render(request, 'overallsystem/favorites.html', {'fave': favorites})