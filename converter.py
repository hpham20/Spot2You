import spotify
import youtube

def main():
    token = spotify.get_token()

    # Retrieve playlist information from Spotify (name, song names, artists)
    spotifyPlaylistId = ""
    playlistName = spotify.get_tracks_from_playlist(token, spotifyPlaylistId)[0]
    songsToConvert = spotify.get_tracks_from_playlist(token, spotifyPlaylistId)[1]

    # Run YouTube search for every song and get the first result
    songsInYoutube = youtube.search_for_song(songsToConvert)

    # Create and add to new playlist on YouTube
    playlistId = youtube.create_playlist(playlistName)
    youtube.add_to_playlist(playlistId, songsInYoutube)

if __name__ == "__main__":
    main()