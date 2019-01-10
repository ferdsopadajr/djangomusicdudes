from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from overallsystem.modules.kmeans import cluster_points, read_file
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MainForm, CreateUserForm
from .models import Profiles

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
	if request.path == '/main/' or request.path == '/':
		return render(request, 'overallsystem/main.html', {'form': MainForm(), 'songs': songs, 'profiles': Profiles.objects.get(user=request.user)})
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
def gen_rec(request):
	rec_songs = cluster_points(request.POST['track_id'])
	return render(request, 'overallsystem/recommendations.html', {'rec_songs': rec_songs})