from django.db import models

# Create your models here.
class Profiles(models.Model):
	user = models.CharField(max_length=100, primary_key=True)
	pref_mean_x = models.FloatField(null=True)
	pref_mean_y = models.FloatField(null=True)

class Tracks(models.Model):
	track_id = models.CharField(max_length=50, primary_key=True)
	listens = models.IntegerField(default=0)
	ratings = models.FloatField(default=0)

class Playlists(models.Model):
	user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
	playlist_name = models.CharField(max_length=100)

class UserFaves(models.Model):
	user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
	track = models.CharField(max_length=50)

class PlaylistTracks(models.Model):
	playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
	track = models.CharField(null=True, max_length=50)