import requests
import json
import base64
import csv

#access token
access_token = 'BQBD3f9QOLdtC87UGBK3MQJruSj40CV-kJ-qu_5xqs_ymh4W0Q2TVLhbiEGApphUqDDySCqBzZkQ6Wri9g1rVWnQYLmk7IDdyIbJLCn_NhUTMqYz95k0X_8W91i4wsj4yYT8Dsd1'

#read csv file
with open('452Tracks.csv', 'r') as old_file:
	reader = csv.DictReader(old_file)
	song_id = [dict(row) for row in reader]
old_file.close()

headers = {
	'Authorization' : 'Bearer ' + access_token
}

with open('New452Tracks.csv', 'w', newline = '') as new_file:
	fieldnames = []
	for value in song_id:
		request = 'https://api.spotify.com/v1/tracks/' + value['id']
		response = requests.get(request, headers = headers, params = {'market' : 'ES'})
		value['artists'] = response.json()['artists']
		fieldnames = value.keys()
		break
	writer = csv.DictWriter(new_file, fieldnames = list(fieldnames))	
	writer.writeheader()
	for value in song_id:
		artists = []
		request = 'https://api.spotify.com/v1/tracks/' + value['id']
		response = requests.get(request, headers = headers, params = {'market' : 'ES'})
		for instance in response.json()['artists']:
			artists.append(instance['name'])
		value['artists'] = ", ".join(artists)
		print(value['id'], '=', value['artists'])
		writer.writerow(value)
	print('Success!')