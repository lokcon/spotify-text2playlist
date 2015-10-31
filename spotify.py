import spotipy, spotipy.util
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

            print("Successfully loged in! (%s)" % username)
        else:
            self.spotipy = spotipy.Spotify()
            self.user_id = None


    def create_playlist(self, name):
        result = self.spotipy.user_playlist_create(
            user = self.user_id, name = name, public = False)

        return result['id']


    def list_playlists(self):
        return self.spotipy.user_playlists(user = self.user_id)


    def search_track(self, string, limit = 10):
        results = self.spotipy.search(q = string, limit = limit)

        tracks = collections.OrderedDict()
        for track in results['tracks']['items']:
            artists = [(artist['name'] + ', ') for artist in track['artists']]
            artists_string = "".join(artists)[:-2] # Throw the last ", " away
            track_name = track['name']

            tracks[track['uri']] = (artists_string, track_name)

        return tracks


    def search_track_first(self, string):
        results = self.search_track(string, limit = 1)
        if results:
            return results.items()[0]
        else:
            return None


    def search_tracks(self, tracks, verbal = False):
        print("Searches:")

        # Search tracks
        track_ids = []
        count = 0
        for track in tracks:
            try:
                track_id, (artists, track_name) = self.search_track_first(track)
            except TypeError: # current track not found
                print("\tNo result for \"%s\"" % track)
            else:
                count += 1
                track_ids.append(track_id)

                if verbal:
                    print("\t#%d Matched %s - %s" % (count, artists, track_name))

        return track_ids


    def tracks_to_playlist(self, track_ids, new_playlist_name, verbal = False):
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


def prompt_confirm(message):
    CONFIRM_TEXT = "%s [Y/n] "

    sys.stdout.write(CONFIRM_TEXT % message)

    answer = raw_input().lower()
    if answer in ["y", "ye", "yes", ""]:
        return True
    elif answer in ["n", "no"]:
        return False
    else:
        print("Invalid option received. Assumed NO.")

    return False


def main():
    if len(sys.argv) != 4:
        print("Invalid number of arguments.")
    else:
        # command line arguments
        (username, playlist, tracks_filename) = sys.argv[1:]

        # Construct track lists
        with open(tracks_filename) as f:
            tracks = [line.rstrip() for line in f if line.rstrip()]

        sp = Spotify(SECRETS, username)
        track_ids = sp.search_tracks(tracks, verbal = True)

        question = "Do you want to add them to new playlist? %s" % playlist
        if prompt_confirm(question):
            sp.tracks_to_playlist(track_ids, playlist, verbal = True)


if __name__ == "__main__":
    main()
