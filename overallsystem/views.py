from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from overallsystem.modules.kmeans import plot_points, compute_ratings, compute_cols_mean, cluster_points, read_file, preference, determine_mood
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from statistics import mean
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
			Profiles(user=user.username).save()
			messages.success(request, 'Account created successfully!')
			return redirect('/login/')
	else:
		form = CreateUserForm()
	return render(request, 'overallsystem/login.html', {'form': form})

@login_required(redirect_field_name=None)
@csrf_exempt
def main(request):
	songs = [read_file(track.track) for track in Tracks.objects.all().order_by('-listens')]
	# Uncomment this to add the tracks to database
	# songs = [track for track in read_file()]
	# for track in songs:
	# 	track = Tracks(track=track['id']).save()
	profile = Profiles.objects.get(user=request.user)
	pref = preference(profile, Profiles._meta.fields)
	mood = None
	rec_songs = None
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
	mood = determine_mood(preference(profile, Profiles._meta.fields))['mood']
	rec_songs = cluster_points(preference=preference(profile, Profiles._meta.fields))
	return render(request, 'overallsystem/recommendations.html', {'rec_songs': rec_songs, 'mood': mood, 'profile': profile})

@csrf_exempt
def backend_process(request):
	return render(request, 'overallsystem/backend_process.html', {'track_id': request.POST['track_id']})

@csrf_exempt
def add_to_pref(request):
	UserListens(user=Profiles.objects.get(user=request.user), track=Tracks.objects.get(track=request.POST['past_track']), listen_duration=request.POST['play_duration']).save()
	# if user play duration >= 50% of max duration add track to preference
	if int(request.POST['play_duration']) >= (int(request.POST['max_duration'])/2):
		profile = Profiles.objects.get(user=request.user)
		col_mean = compute_cols_mean([obj for obj in UserListens.objects.filter(user=Profiles.objects.get(user=request.user)) if obj.listen_duration >= (int(read_file(obj.track.track, False)['duration_ms'])/2)], profile.userfaves_set.all(), preference(profile, Profiles._meta.fields))
		Profiles(user=request.user, acousticness=col_mean['acousticness'], danceability=col_mean['danceability'], energy=col_mean['energy'], instrumentalness=col_mean['instrumentalness'], key=col_mean['key'], liveness=col_mean['liveness'], loudness=col_mean['loudness'], speechiness=col_mean['speechiness'], tempo=col_mean['tempo'], valence=col_mean['valence']).save()
	return HttpResponse()

@csrf_exempt
def disp_listens(request):
	listens = Tracks.objects.get(track=request.POST['track_id']).listens
	temp = get_template('overallsystem/listens-ratings.html')
	html = temp.render({'listens': listens})
	return HttpResponse(html)

@csrf_exempt
def upd_rating(request):
	# rating formula
	# 								(sum(listenduration)+(fvpl*maxdurationoftrack))
	#	rating = --------------------------------------------------------------- * 100
	# 					(sum(listens)*maxdurationoftrack)+(fvpl*maxdurationoftrack)
	if request.POST['past_track']:
		rating = compute_ratings(Tracks.objects.get(track=request.POST['past_track']).listens, [obj.listen_duration for obj in UserListens.objects.filter(track=Tracks.objects.get(track=request.POST['past_track']))], UserFaves.objects.filter(track=Tracks.objects.get(track=request.POST['past_track'])).count(), int(request.POST['max_duration']))
		print(rating)
		Tracks(track=request.POST['past_track'], listens=Tracks.objects.get(track=request.POST['past_track']).listens, ratings=rating).save()
	return HttpResponse(str(Tracks.objects.get(track=request.POST['past_track']).ratings)+'%')

@csrf_exempt
def duration(request):
	if request.POST['track_id']:
		track = read_file(request.POST['track_id'], False)
		return HttpResponse(int(track['duration_ms']))
	else:
		return HttpResponse()

@csrf_exempt
def convert_time(request):
	return HttpResponse(datetime.fromtimestamp(int(request.POST['play_duration'])/1000).strftime('%#M:%S'))

@csrf_exempt
def upd_cbl(request):
	# listens computation
	Tracks(track=request.POST['track_id'], listens=Tracks.objects.get(track=request.POST['track_id']).listens+1).save()
	track = read_file(request.POST['track_id'])
	return render(request, 'overallsystem/now-playing.html', {'track': track, 'fave': [obj.track.track for obj in Profiles.objects.get(user=request.user).userfaves_set.all()]})

@csrf_exempt
def add_to_fav(request):
	UserFaves(user=Profiles.objects.get(user=request.user), track=Tracks.objects.get(track=request.POST['track_id'])).save()
	rating = compute_ratings(Tracks.objects.get(track=request.POST['track_id']).listens, [obj.listen_duration for obj in UserListens.objects.filter(track=Tracks.objects.get(track=request.POST['track_id']))], UserFaves.objects.filter(track=Tracks.objects.get(track=request.POST['track_id'])).count(), int(request.POST['max_duration']))
	Tracks(track=request.POST['track_id'], ratings=rating).save()
	profile = Profiles.objects.get(user=request.user)
	col_mean = compute_cols_mean(profile.userlistens_set.all(), profile.userfaves_set.all(), preference(profile, Profiles._meta.fields))
	Profiles(user=request.user, acousticness=col_mean['acousticness'], danceability=col_mean['danceability'], energy=col_mean['energy'], instrumentalness=col_mean['instrumentalness'], key=col_mean['key'], liveness=col_mean['liveness'], loudness=col_mean['loudness'], speechiness=col_mean['speechiness'], tempo=col_mean['tempo'], valence=col_mean['valence']).save()
	return HttpResponse()

@csrf_exempt
def del_to_fav(request):
	UserFaves.objects.filter(user=Profiles.objects.get(user=request.user), track=Tracks.objects.get(track=request.POST['track_id'])).delete()
	profile = Profiles.objects.get(user=request.user)
	col_mean = compute_cols_mean(profile.userlistens_set.all(), profile.userfaves_set.all(), preference(profile, Profiles._meta.fields))
	Profiles(user=request.user, acousticness=col_mean['acousticness'], danceability=col_mean['danceability'], energy=col_mean['energy'], instrumentalness=col_mean['instrumentalness'], key=col_mean['key'], liveness=col_mean['liveness'], loudness=col_mean['loudness'], speechiness=col_mean['speechiness'], tempo=col_mean['tempo'], valence=col_mean['valence']).save()
	if all(value == None for value in col_mean.values()):
		return HttpResponse(False)
	return HttpResponse()

@csrf_exempt
def favorites(request):
	fave = Profiles.objects.get(user=request.user).userfaves_set.all()
	songs = [obj.track.track for obj in fave]
	favorites = [read_file(track) for track in songs]
	return render(request, 'overallsystem/favorites.html', {'fave': favorites})