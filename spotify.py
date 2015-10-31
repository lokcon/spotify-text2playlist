import spotipy.util
import collections
import sys
from app_secrets import SECRETS
from pprint import pprint


class Spotify:
    SCOPE = "playlist-modify-private playlist-read-private"

    def __init__(self, secrets, username = ""):

        # Auth
        if secrets:
            auth_token = spotipy.util.prompt_for_user_token(
                        username = username,
                        scope = self.SCOPE,
                        client_id = secrets["client_id"],
                        client_secret = secrets["client_secret"],
                        redirect_uri = secrets["redirect_uri"])

            self.spotipy = spotipy.Spotify(auth = auth_token)
            self.user_id = self.spotipy.current_user()["id"]

            print("Successfully logined!")
        else:
            self.spotipy = spotipy.Spotify()
            self.user_id = None


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


    def search_song_first(self, string):
        results = self.search_song(string, limit = 1)
        if results:
            return results.items()[0]
        else:
            return None

    def search_songs(self, songs, verbal = False):
        # Search tracks
        tracks = []
        count = 0
        for song in songs:
            try:
                track_id, (artists, song_name) = self.search_song_first(song)
            except TypeError: # current track not found
                print("\tNot found: \"%s\"" % song)

                continue
            else:
                count += 1
                tracks.append(track_id)

                if verbal:
                    print("#%02d Found: %s (%s)" % (count, song_name, artists))

        return tracks


    def songs_to_playlist(self, track_ids, new_playlist_name, verbal = False):
        # Create playlist
        new_playlist_id = self.create_playlist(new_playlist_name)

        if verbal:
            print("Playlist Successfully created!")

        # Add tracks to playlist
        self.spotipy.user_playlist_add_tracks(
            user = self.user_id,
            playlist_id = new_playlist_id,
            tracks = track_ids)

        if verbal:
            print("%d tracks added to playlist: %s" %
                    (len(track_ids), new_playlist_name))



def main():
    if len(sys.argv) != 4:
        print("Invalid number of arguments.")
    else:
        # command line arguments
        (username, playlist, songs_filename) = sys.argv[1:]

        # Construct song lists
        with open(songs_filename) as f:
            songs = [line.rstrip() for line in f]

        sp = Spotify(SECRETS, username)
        track_ids = sp.search_songs(songs, verbal = True)
        sp.songs_to_playlist(track_ids, playlist, verbal = True)


if __name__ == "__main__":
    main()
