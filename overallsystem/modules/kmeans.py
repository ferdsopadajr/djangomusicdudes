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
	with open('452Tracks.csv', 'r') as file:
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

def calc_dist(tracks, query):
	distance = {key:[] for key in query if key not in ['quadrant', 'track_name', 'id', 'genre', 'duration_ms', 'energy', 'mode', 'valence']}

	for track_id in tracks:
		feats = read_file(track_id)[0]
		for i in feats:
			if i in ['track_name', 'id', 'genre', 'duration_ms', 'energy', 'mode', 'valence']:
				continue
			distance[i].append([track_id, np.linalg.norm(float(query[i]) - float(feats[i]))])
	return distance

def get_min(distance):
	return [track for key in distance for track in distance[key] if track[1] == min([track[1] for track in distance[key]])]

def euclidean_distance(point, centroids = None, dim = '2d', query = None):
	distance = {}
	if dim == '1d':
		# Get distance for each audio feature in the cluster
		if query['id'] in point:
			point.remove(query['id'])
		
		distance = calc_dist(point, query)

		# Get the track with minimum distance for each audio feature
		minimum = get_min(distance)
		freq = {item[0]:0 for item in minimum}
		for item in minimum:
			freq[item[0]] = [item[0] for item in minimum].count(item[0])

		return [key for key in freq if freq[key] == max(freq.values())]
	else:
		# Get distance for each point to the centroids in the quadrant
		cluster = 0
		for key in centroids:
			distance[key] = np.linalg.norm(np.array(point[:2]) - np.array(centroids[key]))
			if min(distance.values()) == distance[key]:
				cluster = key
		return cluster

def gen_centroids(quadrant):
	return [round(np.random.uniform(low = quadrant['v_low'], high = quadrant['v_high']), 3), round(np.random.uniform(low = quadrant['e_low'], high = quadrant['e_high']), 3)]

def k_means(quadrant, k_count = 5):
	# Generate random points for centroids
	centroids = {}
	for count in range(k_count):
		centroids[count] = gen_centroids(quadrant)

	# Start k-means clustering
	clusters = {key:[] for key in centroids.keys()}
	old_clusters = {}
	diff = []

	# Run while loop until none of the cluster assignments change
	while True:
		# Copy old clusters' values
		old_clusters = deepcopy(clusters)
		# Reset clusters assignment
		clusters = {key:[] for key in clusters}

		# Find nearest centroid for each data point using Euclidean Distance
		for track in quadrant['data_points']:
			point = [float(track['valence']), float(track['energy']), track['id']]
			clusters[euclidean_distance(point, centroids)].append(point)

		# Update centroids
		for key in centroids:
			if any(clusters[key]):
				centroids[key][0] = round(mean(point[0] for point in clusters[key]), 3)
				centroids[key][1] = round(mean(point[1] for point in clusters[key]), 3)

		# Check change in clusters assignment
		diff = [point for key in clusters for point in clusters[key] if point not in old_clusters[key]]

		# Check if clusters is ready to be returned
		if not diff:
			for key in clusters:
				if not clusters[key]:
					centroids[key] = gen_centroids(quadrant)
			if all([any(clusters[key]) for key in clusters]):
				break
	return clusters

def elbow_method(quadrant):
	sse = {key:0 for key in range(2, 10)}
	cl_mean = []
	for k_count in range(2, 10):
		clusters = k_means(quadrant, k_count)
		for key in clusters:
			cl_mean.clear()
			cl_mean = [round(mean([point[0] for point in clusters[key]]), 3), round(mean([point[1] for point in clusters[key]]), 3)]
			print('key:',key,'=',clusters[key], cl_mean)
			for point in clusters[key]:
				sse[k_count] += (pow(abs(point[0] - cl_mean[0]), 2) + pow(abs(point[1] - cl_mean[1]), 2))
	sse = {key:round(sse[key], 3) for key in sse}
	plt.plot(sse.keys(), sse.values(), 'bx-')
	plt.xlabel('Number of Clusters K')
	plt.ylabel('Sum of Squared Errors')
	plt.title('Elbow Method For Optimal K')
	plt.show()

def cluster_points(track_id):
	''' Pseudocode for this method
			while songs_to_recommend != quota:
				regenerate random points for centroids

				while cluster assignments change:
					for each data_point.cluster = nearest centroid, using Euclidean Distance
					new centroid = mean of all cluster.data_points
	'''

	# Get mood quadrant to start clustering
	quadrant = determine_mood(read_file(track_id)[0])

	# Elbow method to determine clusters count
	# sse = elbow_method(quadrant)

	# Run while loop until songs_to_recommend != quota
	songs_to_recommend = []
	start = time.time()
	while len(songs_to_recommend) != 10:
		
		# Start K-means clustering
		clusters = k_means(quadrant)

		# Similarity using other audio features
		for key in clusters:
			if len(songs_to_recommend) != 10:
				for track in euclidean_distance([track[2] for track in clusters[key]], dim = '1d', query = quadrant['feat']):
					if len(songs_to_recommend) != 10:
						if track not in songs_to_recommend:
							songs_to_recommend.append(track)
					else:
						break
			else:
				break

	# Elapsed time in getting recommendations
	print('Elapsed time:', timedelta(seconds = time.time() - start))

	# Recommendations ranking
	distance = calc_dist(songs_to_recommend, quadrant['feat'])
	rank = {k:{} for k in distance}

	# Get indices of each recommended track in minimum ranking of each audio feature
	for key in distance:
		distance[key] = sorted(distance[key], key = lambda item : item[1])
		count = 0
		while distance[key]:
			rank[key][count] = [item for item in distance[key] if item[1] == min([item[1] for item in distance[key]])]
			distance[key] = [item for item in distance[key] if item not in rank[key][count]]
			count += 1

	# Attach to each recommended tracks their indices in minimum ranking of each audio feature
	sorted_rec = [[k,[]] for k in songs_to_recommend]
	for k in rank:
		for v in rank[k]:
			for i in rank[k][v]:
				for item in sorted_rec:
					if item[0] == i[0]:
						item[1].append(v)

	# Average the indices in minimum ranking of each audio feature of each recommended track
	for item in sorted_rec:
		item[1] = round(mean(x for x in item[1]), 3)

	# Return sorted recommendations
	return [item[0] for item in sorted(sorted_rec, key = lambda item : item[1])]