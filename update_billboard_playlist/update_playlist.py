import billboard
import re
from tqdm import tqdm

import credentials
import deezer_client


def get_hot_100_track_ids(client):
    """Yield Deezer IDs for chart songs that can be found."""
    for song in tqdm(billboard.ChartData('hot-100').entries):
        track_id = get_track_id(song.title, song.artist, client)
        if track_id is not None:
            yield track_id


def preprocess(artist):
    """Return artist name preprocessed for better search."""
    artist = artist.lower()
    search = re.search(r'( feat)|( & )|( \+ )', artist)
    if search is not None:
        return artist[:search.span()[0]]
    return artist


def get_track_id(title, artist, client):
    """Return Deezer ID of a song, or None if it can't be found."""
    tracks = client.search_track(title)
    artist = preprocess(artist)
    for track in tracks:
        if preprocess(track['artist']['name']) == artist:
            return str(track['id'])


def update_playlist():
    """Update Billboard Hot 100 Deezer playlist."""
    playlist_id = credentials.get_playlist_id()
    client = deezer_client.DeezerClient(credentials.get_token())
    client.clear_playlist(playlist_id)
    client.add_to_playlist(playlist_id, get_hot_100_track_ids(client))

