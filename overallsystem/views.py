from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import csv

# Create your views here.
def login(request):
	maptoquadrant()
	return render(request, 'overallsystem/login.html')

# Energy + Valence Mapping - Map query to its corresponding mood (Thayer's Mood Model)
def maptoquadrant():
	# test - plot training data to quadrants
	with open('Training Data.csv', 'r') as file:
		reader = csv.DictReader(file)
		song_id = [[dict(row)['valence'], dict(row)['energy']] for row in reader]
		# x = valence, y = energy
		data1 = [float(song[0]) for song in song_id if float(song[0]) > 0.5 and float(song[1]) >= 0.5], [float(song[1]) for song in song_id if float(song[0]) > 0.5 and float(song[1]) >= 0.5]
		data2 = [float(song[0]) for song in song_id if float(song[0]) <= 0.5 and float(song[1]) > 0.5], [float(song[1]) for song in song_id if float(song[0]) <= 0.5 and float(song[1]) > 0.5]
		data3 = [float(song[0]) for song in song_id if float(song[0]) >= 0.5 and float(song[1]) < 0.5], [float(song[1]) for song in song_id if float(song[0]) >= 0.5 and float(song[1]) < 0.5]
		data4 = [float(song[0]) for song in song_id if float(song[0]) < 0.5 and float(song[1]) <= 0.5], [float(song[1]) for song in song_id if float(song[0]) < 0.5 and float(song[1]) <= 0.5]
		
		data = [data1, data2, data3, data4]
		colors = ['yellow', 'red', 'blue', 'black']
		groups = ['happy', 'angry', 'peaceful', 'sad']
		
		for data, color, group in zip(data, colors, groups):
			x, y = data
			plt.scatter(x, y, s = 20, edgecolors='none', c = color, label = group)
		
		plt.xlabel('Valence')
		plt.ylabel('Energy')
		plt.title('Mood Map')
		plt.xticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
		plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
		plt.axvline(0.5, color = 'k', linewidth = 1)
		plt.axhline(0.5, color = 'k', linewidth = 1)
		plt.legend(loc = 4)
		plt.show()
	file.close()