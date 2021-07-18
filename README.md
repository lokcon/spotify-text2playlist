# text2playlist - Convert a list of songs into a Spotify playlist
Perform searches from a list of songs and add them to a new single playlist in Spotify.

The python script search tracks in the Spotify database one by one,
and populate the results into a playlist under a specificed Spotify account.

## Requirements
* Python 2

## Dependencies
* [Spotipy](https://github.com/plamere/spotipy) - A python wrapper for the
Spotify Web API
* [Requests](https://github.com/kennethreitz/requests) - Python HTTP module, needed by Spotipy

## Usage
### Spotify API
To use the script, you need authorized Spotify API access.
Put your API secrets in `app_secrets.py`, like so:
```python
SECRETS = {
    "client_id": "a13b46c7a13b46c7a13b46c7a13b46c7",
    "client_secret": "d7e8f9g0d7e8f9g0d7e8f9g0d7e8f9g0",
    "redirect_uri":"http://your.redirect.uri"}
```

### Using the script
`python text2playlist.py --help`
```
usage: text2playlist.py [-h] username playlist tracks_filename

positional arguments:
  username         Spotify account
  playlist         Name of the playlist to be created
  tracks_filename  Path to a file of a list of tracks to be added

optional arguments:
  -h, --help       show this help message and exit
```

### Example Usage
songs.txt:
```
in my head - jason derulo
try - pink
it ends tonight - all american rejects
sugar - maroon 5
```

calling
`python text2laylist.py username "New Playlist" songs.txt`

```
Successfully loged in! (username)
Searches:
	#1 Matched | Jason Derulo - In My Head
	#2 Matched | P!nk - Try
	#3 Matched | The All-American Rejects - It Ends Tonight
	#4 Matched | Maroon 5 - Sugar
Do you want to add them to new playlist? New Playlist [Y/n] y
Playlist Successfully created!
4 tracks added to playlist: New Playlist
```

## To-do
* Smarter search when no result for a track is found
    * Use Google to get track info?
    * replace words like "ft.", "featuring" with spaces
