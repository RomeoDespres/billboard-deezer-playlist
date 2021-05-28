import logging
import re

import billboard
from tqdm import tqdm

import credentials
import deezer_client


def get_hot_100_track_ids(client):
    """Yield Deezer IDs for chart songs that can be found."""
    songs = billboard.ChartData("hot-100").entries
    logging.info(f"Fetched {len(songs)} songs from Billboard")
    for song in tqdm(songs):
        track_id = get_track_id(song.title, song.artist, client)
        if track_id is not None:
            yield track_id


def preprocess(artist):
    """Return artist name preprocessed for better search."""
    artist = artist.lower()
    search = re.search(r"( feat)|( & )|( \+ )", artist)
    if search is not None:
        return artist[: search.span()[0]]
    return artist


def get_track_id(title, artist, client):
    """Return Deezer ID of a song, or None if it can't be found."""
    logging.info(f"Looking for {title} by {artist}")
    logging.info(f"Changed {artist} to {preprocess(artist)}")
    artist = preprocess(artist)
    for query in (title, artist), (title,):
        tracks = client.search_track(*query)
        logging.info(f"Found {len(tracks)} tracks matching {query}")
        for track in tracks:
            track_artist = preprocess(track["artist"]["name"])
            logging.info(f"Matching {artist} against {track_artist}")
            if preprocess(track_artist) == artist:
                logging.info("Matched")
                return str(track["id"])
        if tracks:
            track = tracks[0]
            title, artist = track["title"], track["artist"]["name"]
            logging.info(f"No match. Returning {title} by {artist}.")
            return str(track["id"])


def update_playlist():
    """Update Billboard Hot 100 Deezer playlist."""
    playlist_id = credentials.get_playlist_id()
    logging.info(f"Using playlist {playlist_id}")
    client = deezer_client.DeezerClient(credentials.get_token())
    logging.info("Connected to Deezer API")
    client.clear_playlist(playlist_id)
    logging.info("Cleared playlist.")
    client.add_to_playlist(playlist_id, get_hot_100_track_ids(client))
    logging.info("Done.")
