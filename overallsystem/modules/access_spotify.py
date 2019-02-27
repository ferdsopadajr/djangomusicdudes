import requests
import base64
import json

def get_token(auth_code):
	endpoint = 'https://accounts.spotify.com/api/token'
	headers = {'Authorization' : 'Basic ' + base64.b64encode(bytes('a48c9d16e27c435b83a238aaa57d1844:597d426ce9d84c0fbedb3bf0c03eb40c', 'utf-8')).decode('utf-8'), 'Content-Type' : 'application/x-www-form-urlencoded'}
	response = requests.post(endpoint, headers = headers, params = {'grant_type' : 'authorization_code', 'code' : auth_code, 'redirect_uri' : 'https://localhost:8000/callback/'})
	return response

def get_auth_code():
	endpoint = 'https://accounts.spotify.com/authorize'
	response = requests.get(endpoint, params = {'client_id' : 'a48c9d16e27c435b83a238aaa57d1844', 'response_type' : 'code', 'redirect_uri' : 'https://localhost:8000/callback/', 'scope' : 'user-read-email streaming user-modify-playback-state user-read-playback-state user-read-currently-playing user-read-private user-read-birthdate'})
	return response.url

def play_song(access_token, refresh_token, track):
	endpoint = 'https://api.spotify.com/v1/me/player/play'
	headers = {'Authorization' : 'Bearer ' + access_token, 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
	data = '{"uris" : ["spotify:track:' + track + '"]}'
	response = requests.put(endpoint, headers = headers, data = data)
	if response.status_code != 204:
		endpoint = 'https://accounts.spotify.com/api/token'
		headers = {'Authorization' : 'Basic ' + base64.b64encode(bytes('a48c9d16e27c435b83a238aaa57d1844:597d426ce9d84c0fbedb3bf0c03eb40c', 'utf-8')).decode('utf-8'), 'Content-Type' : 'application/x-www-form-urlencoded'}
		response = requests.post(endpoint, headers = headers, params = {'grant_type' : 'refresh_token', 'refresh_token' : refresh_token})
		play_song(response.json['access_token'], refresh_token, track)
	return response

def set_volume(access_token, volume):
	endpoint = 'https://api.spotify.com/v1/me/player/volume'
	headers = {'Authorization' : 'Bearer ' + access_token, 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
	response = requests.put(endpoint, headers = headers, params = {'volume_percent' : volume})
	return response