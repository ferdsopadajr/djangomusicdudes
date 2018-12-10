from copy import deepcopy
import csv
from math import *
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean

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
	for feat in row:
		if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5:
			return {'mood': 'happy', 'v_low': 0.501, 'v_high': 1.001, 'e_low': 0.5, 'e_high': 1.001, 'feat': feat, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}
		elif float(feat['valence']) <= 0.5 and float(feat['energy']) > 0.5:
			return {'mood': 'angry', 'v_low': 0, 'v_high': 0.501, 'e_low': 0.501, 'e_high': 1.001, 'feat': feat, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}
		elif float(feat['valence']) >= 0.5 and float(feat['energy']) < 0.5:
			return {'mood': 'peaceful', 'v_low': 0.5, 'v_high': 1.001, 'e_low': 0, 'e_high': 0.5, 'feat': feat, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}
		elif float(feat['valence']) < 0.5 and float(feat['energy']) <= 0.5:
			return {'mood': 'sad', 'v_low': 0, 'v_high': 0.5, 'e_low': 0, 'e_high': 0.501, 'feat': feat, 'data_points': [feat for feat in songs if float(feat['valence']) > 0.5 and float(feat['energy']) >= 0.5]}

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

'''
x = {1: [0.011,0.696,0,2,0.302,-2.743,0.103,114.944],
		 2: [0.022,0.932,0,11,0.093,-7.755,0.161,139.974],
		 3: [0.942,0.717,0.85,1,0.139,-6.539,0.045,143.779]}

quer = [0.514,0.735,0.09,5,0.159,-11.84,0.046,98.002]
d = {k:[] for k,v in enumerate(quer)}

for k in x:
  for v in d:
    print(quer[v],'-',x[k][v],'=',round(quer[v]-x[k][v],3))
    d[v].append([k,abs(round(quer[v]-x[k][v],3))])
  print('\n')
print(d)

for k in d:
  print([i[0] for i in d[k] if i[1] == min([i[1] for i in d[k]])])
  print('\n')
'''

def euclidean_distance(point, centroids = None, dim = '2d', query = None):
	distance = {}
	if dim == '1d':
		point.remove(query['id'])
		distance = {key:[] for key in query}
		for track_id in point:
			feats = read_file(track_id)
			distance['acousticness'].append(abs(float(query['acousticness']) - float(feats[0]['acousticness'])))
		print(distance['acousticness'], min(distance['acousticness']))
	else:
		cluster = 0
		for key in centroids:
			distance[key] = sqrt(pow(abs(point[0] - centroids[key][0]), 2) + pow(abs(point[1] - centroids[key][1]), 2))
			if min(distance.values()) == distance[key]:
				cluster = key
		return cluster

def cluster_points(clusters, track_id):
	''' Pseudocode for this method
			while songs_to_recommend != quota:
				regenerate random points for centroids

				while cluster assignments change:
					for each data_point.cluster = nearest centroid, using Euclidean Distance
					new centroid = mean of all cluster.data_points
	'''

	# Get mood quadrant to start clustering
	quadrant = determine_mood(read_file(track_id))

	# Run while loop until songs_to_recommend != quota
	songs_to_recommend = []

	# Generate random points for centroids
	centroids = {}
	for count in range(clusters):
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
		for track in quadrant['data_points'][:15]:
			point = [float(track['valence']), float(track['energy']), track['id']]
			clusters[euclidean_distance(point, centroids)].append(point)
		print('old_clus:', old_clusters)
		print('clus:', clusters)

		# Update centroids
		for key in centroids:
			if any(clusters[key]):
				centroids[key][0] = round(mean(point[0] for point in clusters[key]), 3)
				centroids[key][1] = round(mean(point[1] for point in clusters[key]), 3)

		# Check change in clusters assignment
		diff = [point for key in clusters for point in clusters[key] if point not in old_clusters[key]]
		print('clusters_diff:\n', diff)

		if not diff:
			break

	# Similarity using other audio features
	euclidean_distance([point[2] for key in clusters for track in clusters[key] if track[2] == track_id for point in clusters[key]], dim = '1d', query = quadrant['feat'])