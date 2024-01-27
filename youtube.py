from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
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

youtube = build(
    api_service_name, api_version, credentials=credentials)

# Takes list of Spotify songs and returns YouTube version 
def search_for_song(searchQueries):
    songIdList = []
    for query in searchQueries:
        request = youtube.search().list(
            part="snippet",
            maxResults=5,
            type="video",
            q=query
        )
        response = request.execute().get("items", [])
        songIdList.append(response[0]["id"]["videoId"])
    return songIdList

# Retrieves all playlists given a channel ID
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
def create_playlist(playlistTitle):
    request = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": playlistTitle
            }
        }
    )
    response = request.execute().get("id")
    return response

# Takes PlaylistID and list of song IDs. Adds each song to the playlist
def add_to_playlist(playlistId, videoIdList):
    for videoId in videoIdList:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlistId,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": videoId
                    }
                }
            }
        )
        response = request.execute().get("status")