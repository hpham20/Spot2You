from dotenv import load_dotenv
from requests import post, get
import base64
import json
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

def get_artist_by_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    response = get(url, headers=headers)
    json_response = response.json()["name"]
    return json_response

def get_playlist_by_id(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)
    response = get(url, headers=headers)
    json_response = response.json()["tracks"]
    return json_response

token = get_token()

# get_artist_by_id(token, {ARTIST ID GOES HERE})
# result = get_playlist_by_id(token, {PLAYLIST ID GOES HERE})
# for item in result["items"]:
#     print(item["track"]["name"])