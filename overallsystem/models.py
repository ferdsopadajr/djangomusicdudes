from django.db import models

# Create your models here.
class Profiles(models.Model):
	user = models.CharField(max_length=100, primary_key=True)
	acousticness = models.FloatField(null=True)
	danceability = models.FloatField(null=True)
	energy = models.FloatField(null=True)
	instrumentalness = models.FloatField(null=True)
	key = models.FloatField(null=True)
	liveness = models.FloatField(null=True)
	loudness = models.FloatField(null=True)
	speechiness = models.FloatField(null=True)
	tempo = models.FloatField(null=True)
	valence = models.FloatField(null=True)

class Tracks(models.Model):
	track = models.CharField(max_length=50, primary_key=True)
	listens = models.IntegerField(default=0)
	ratings = models.FloatField(default=0)

class UserListens(models.Model):
	user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
	track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
	listen_duration = models.IntegerField(default=0)

class Playlists(models.Model):
	user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
	playlist_name = models.CharField(max_length=100)

class UserFaves(models.Model):
	user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
	track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('user', 'track')

class PlaylistTracks(models.Model):
	playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
	track = models.CharField(null=True, max_length=50)