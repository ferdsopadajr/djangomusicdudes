from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Profiles(models.Model):
	user = models.CharField(max_length=100, primary_key=True)
	pref_mean_x = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
	pref_mean_y = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

class Playlists(models.Model):
	user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
	playlist_name = models.CharField(max_length=100)

class UserFaves(models.Model):
	user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
	track = models.CharField(max_length=50)

class PlaylistTracks(models.Model):
	playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
	track = models.CharField(null=True, max_length=50)