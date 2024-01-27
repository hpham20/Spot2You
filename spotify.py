from dotenv import load_dotenv
from requests import post, get
import base64
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

encoded_bytes = (CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")
encoded_credentials = str(base64.b64encode(encoded_bytes), "utf-8")

# Use Client ID and Client Secret to obtain access token
def get_token():
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        'Authorization': 'Basic ' + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = { "grant_type": "client_credentials" }

    response = post(url, headers=headers, data=data)
    token = response.json()["access_token"]
    return token

# Establish header for reuse in future requests
def get_auth_header(token):
    return { "Authorization": "Bearer " + token }

# Returns list of tracks and their respective artist from given Playlist ID
def get_tracks_from_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)
    response = get(url, headers=headers)

    playlistName = response.json()["name"]
    json_response = response.json()["tracks"]["items"]

    trackList = []

    for item in json_response:
        artist = item["track"]["artists"][0]["name"]
        songTitle = item["track"]["name"]

        trackList.append(artist + " " + songTitle)

    return playlistName, trackList