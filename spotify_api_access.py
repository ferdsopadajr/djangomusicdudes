import requests
import json
import base64
import csv

#access token
access_token = 'BQAdGQye2Tr9KBF2WcrLQKp-2b8CV6tZV1JMQuN8it3Nl506DYT2CSGfOUql-FdJe8nK9PUPKYwwMPvLBFp2I8DZPjUVQmnpkRHV080X9rC4JjZt5xkN0DeSExOiEVE-RXwMcjXJ'

#read csv file
# with open('452Tracks.csv', 'r') as old_file:
# 	reader = csv.DictReader(old_file)
# 	song_id = [dict(row) for row in reader]
# old_file.close()

# headers = {
# 	'Authorization' : 'Bearer ' + access_token
# }

# with open('452Tracks.csv', 'w', newline = '') as new_file:
# 	fieldnames = []
# 	for value in song_id:
# 		request = 'https://api.spotify.com/v1/tracks/' + value['id']
# 		response = requests.get(request, headers = headers, params = {'market' : 'ES'})
# 		value['name'] = response.json()['name']
# 		fieldnames = value.keys()
# 		break
# 	writer = csv.DictWriter(new_file, fieldnames = list(fieldnames))	
# 	writer.writeheader()
# 	for value in song_id:
# 		request = 'https://api.spotify.com/v1/tracks/' + value['id']
# 		response = requests.get(request, headers = headers, params = {'market' : 'ES'})
# 		value['name'] = response.json()['name']
# 		writer.writerow(value)
# 	print('Success!')