from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import googleapiclient.errors
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

scopes = [
    "https://www.googleapis.com/auth/youtube.readonly", 
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "credentials.json"

flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_local_server(port=3000)

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

def search_for_song(artist, title):
    
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        type="video",
        q=artist + " " + title
    )
    response = request.execute().get("items", [])
    
    print(response[0]["id"]["videoId"])

def get_playlist_by_channel_id(channel_id):
    
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=25
    )

    response = request.execute().get("items", [])

    for playlist in response:
        print(f"Playlist Title: {playlist['snippet']['title']}")
        print(f"Playlist ID: {playlist['id']}")
        print(f"Number of Videos: {playlist['contentDetails']['itemCount']}")
        print("------")

# Create a playlist. Returns its id
def create_playlist():
    
    request = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": "PLAYLIST TITLE HERE"
            }
        }
    )

    response = request.execute().get("id")
    return response

def add_to_playlist():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"

    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port=3000)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": "PLAYLIST ID HERE",
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": "VIDEO ID HERE"
                }
            }
        }
    )

    response = request.execute().get("status")
    print(response)

# playlistID = create_playlist()
# get_playlist_by_channel_id("")
# add_to_playlist()