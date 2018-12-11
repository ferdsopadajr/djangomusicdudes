from copy import deepcopy
import csv
from datetime import timedelta
from math import *
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import time

# K-Means Clustering Module

def read_file(track_id = None):
	with open('Training Data.csv', 'r') as file:
		reader = csv.DictReader(file)
		if not track_id:
			return [dict(row) for row in reader]
		else:
			return [dict(row) for row in reader if dict(row)['id'] == track_id]
	file.close()

def determine_mood(row):
	# Return mood quadrant of track
	songs = read_file()
	if float(row['valence']) > 0.5 and float(row['energy']) >= 0.5:
		return {'mood': 'happy', 'v_low': 0.501, 'v_high': 1.001, 'e_low': 0.5, 'e_high': 1.001, 'feat': row, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}
	elif float(row['valence']) <= 0.5 and float(row['energy']) > 0.5:
		return {'mood': 'angry', 'v_low': 0, 'v_high': 0.501, 'e_low': 0.501, 'e_high': 1.001, 'feat': row, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}
	elif float(row['valence']) >= 0.5 and float(row['energy']) < 0.5:
		return {'mood': 'peaceful', 'v_low': 0.5, 'v_high': 1.001, 'e_low': 0, 'e_high': 0.5, 'feat': row, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}
	elif float(row['valence']) < 0.5 and float(row['energy']) <= 0.5:
		return {'mood': 'sad', 'v_low': 0, 'v_high': 0.5, 'e_low': 0, 'e_high': 0.501, 'feat': row, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}

def plot_points():
	# Energy + Valence Mapping - Plot points to their corresponding mood (Thayer's Mood Model)
	songs = read_file()

	# x = valence, y = energy
	data1 = [float(feat[0]) for feat in songs if float(feat[0]) > 0.5 and float(feat[1]) >= 0.5], [float(feat[1]) for feat in songs if float(feat[0]) > 0.5 and float(feat[1]) >= 0.5]
	data2 = [float(feat[0]) for feat in songs if float(feat[0]) <= 0.5 and float(feat[1]) > 0.5], [float(feat[1]) for feat in songs if float(feat[0]) <= 0.5 and float(feat[1]) > 0.5]
	data3 = [float(feat[0]) for feat in songs if float(feat[0]) >= 0.5 and float(feat[1]) < 0.5], [float(feat[1]) for feat in songs if float(feat[0]) >= 0.5 and float(feat[1]) < 0.5]
	data4 = [float(feat[0]) for feat in songs if float(feat[0]) < 0.5 and float(feat[1]) <= 0.5], [float(feat[1]) for feat in songs if float(feat[0]) < 0.5 and float(feat[1]) <= 0.5]
	
	data = [data1, data2, data3, data4]
	colors = ['yellow', 'red', 'blue', 'black']
	groups = ['happy', 'angry', 'peaceful', 'sad']
	
	for data, color, group in zip(data, colors, groups):
		x, y = data
		plt.scatter(x, y, s = 20, edgecolors='none', c = color, label = group)

	plt.style.use('seaborn-whitegrid')
	plt.xlabel('Valence')
	plt.ylabel('Energy')
	plt.title('Mood Map')
	plt.xticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
	plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
	plt.axvline(0.5, color = 'k', linewidth = 1)
	plt.axhline(0.5, color = 'k', linewidth = 1)
	plt.legend(loc = 4)
	plt.show()

def euclidean_distance(point, centroids = None, dim = '2d', query = None):
	distance = {}
	if dim == '1d':
		# Get distance for each audio feature in the cluster
		if query['id'] in point:
			point.remove(query['id'])
		distance = {key:[] for key in query if key not in ['quadrant', 'track_name', 'id', 'genre', 'duration_ms', 'energy', 'mode', 'valence']}
		
		for track_id in point:
			feats = read_file(track_id)[0]
			for i in feats:
				if i in ['quadrant', 'track_name', 'id', 'genre', 'duration_ms', 'energy', 'mode', 'valence']:
					continue
				distance[i].append([track_id, round(abs(float(query[i])-float(feats[i])),3)])

		# Get the track with minimum distance for each audio feature
		minimum = [track for key in distance for track in distance[key] if track[1] == min([track[1] for track in distance[key]])]
		freq = {item[0]:0 for item in minimum}
		for item in minimum:
			freq[item[0]] = [item[0] for item in minimum].count(item[0])

		return [key for key in freq if freq[key] == max(freq.values())]
	else:
		# Get distance for each point to the centroids in the quadrant
		cluster = 0
		for key in centroids:
			distance[key] = sqrt(pow(abs(point[0] - centroids[key][0]), 2) + pow(abs(point[1] - centroids[key][1]), 2))
			if min(distance.values()) == distance[key]:
				cluster = key
		return cluster

def cluster_points(k_count, track_id):
	''' Pseudocode for this method
			while songs_to_recommend != quota:
				regenerate random points for centroids

				while cluster assignments change:
					for each data_point.cluster = nearest centroid, using Euclidean Distance
					new centroid = mean of all cluster.data_points
	'''

	# Get mood quadrant to start clustering
	quadrant = determine_mood(read_file(track_id)[0])

	centroids = {}
	songs_to_recommend = []

	# Run while loop until songs_to_recommend != quota
	start = time.time()
	while len(songs_to_recommend) != 15:
		# Generate random points for centroids
		centroids.clear()
		for count in range(k_count):
			centroids[count] = [round(np.random.uniform(low = quadrant['v_low'], high = quadrant['v_high']), 3), round(np.random.uniform(low = quadrant['e_low'], high = quadrant['e_high']), 3)]
		
		# Start k-means clustering
		clusters = {key:[] for key in centroids.keys()}
		old_clusters = {}
		diff = []

		# Run while loop until none of the cluster assignments change
		while True:
			old_clusters = deepcopy(clusters) # Copy old clusters' values
			clusters = {key:[] for key in clusters} # Reset clusters assignment

			# Find nearest centroid for each data point using Euclidean Distance
			for track in quadrant['data_points']:
				point = [float(track['valence']), float(track['energy']), track['id']]
				clusters[euclidean_distance(point, centroids)].append(point)
			# print('old_clus:', old_clusters)
			# print('clus:', clusters)

			# Update centroids
			for key in centroids:
				if any(clusters[key]):
					centroids[key][0] = round(mean(point[0] for point in clusters[key]), 3)
					centroids[key][1] = round(mean(point[1] for point in clusters[key]), 3)

			# Check change in clusters assignment
			diff = [point for key in clusters for point in clusters[key] if point not in old_clusters[key]]
			# print('clusters_diff:\n', diff)

			if not diff:
				break

		# Similarity using other audio features
		for key in clusters:
			if len(songs_to_recommend) != 15:
				for track in euclidean_distance([track[2] for track in clusters[key]], dim = '1d', query = quadrant['feat']):
					if len(songs_to_recommend) != 15:
						if track not in songs_to_recommend:
							songs_to_recommend.append(track)
						print('len:',len(songs_to_recommend))
					else:
						break
			else:
				break

	# Elapsed time in getting recommendations
	print(centroids,timedelta(seconds = time.time() - start))

	for item in songs_to_recommend:
		print('songs_to_recommend:', item)