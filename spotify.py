import spotipy.util
import collections
import sys
from pprint import pprint
from app_secrets import secrets


class Spotify:
    def __init__(self, app_client_id = "", app_client_secret = "",
    redirect_url = "", username = "", auth = False):

        # Auth
        if auth:
            token = spotipy.util.prompt_for_user_token(
                        username = username,
                        scope = "playlist-modify-private playlist-read-private",
                        client_id = app_client_id,
                        client_secret = app_client_secret,
                        redirect_uri = redirect_url)
        else:
            token = None

        self.spotipy = spotipy.Spotify(auth = token)
        self.user_id = self.spotipy.current_user()["id"]

        print("Successfully logined!")


    def create_playlist(self, name):
        result = self.spotipy.user_playlist_create(
            user = self.user_id, name = name, public = False)

        return result['id']


    def list_playlists(self):
        return self.spotipy.user_playlists(user = self.user_id)


    def search_song(self, string, limit = 10):
        results = self.spotipy.search(q = string, limit = limit)

        songs = collections.OrderedDict()
        for track in results['tracks']['items']:
            artists = [(artist['name'] + ', ') for artist in track['artists']]
            artists_string = "".join(artists)[:-2] # Throw the last ", " away
            song_name = track['name']

            songs[track['uri']] = (artists_string, song_name)

        return songs


    def search_song_top(self, string):
        return self.search_song(string, limit = 1).items()[0]


    def songs_to_playlist(self, songs, new_playlist_name):
        # Create playlist
        new_playlist_id = self.create_playlist(new_playlist_name)

        # Search tracks
        tracks = []
        for song in songs:
            track_id, (artists, song_name) = self.search_song_top(song)
            print("Added: %-15s - %s" % (song_name, artists))
            tracks.append(track_id)

        # Add tracks to playlist
        self.spotipy.user_playlist_add_tracks(
            user = self.user_id,
            playlist_id = new_playlist_id,
            tracks = tracks)



def main():
    if len(sys.argv) != 4:
        print("Invalid number of arguments.")


if __name__ == "__main__":
    main()
