import json
import os


PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')


def configure():
    """Ask for credentials and register them."""
    credentials = {}
    credentials['token'] = input('Deezer API access token: ')
    credentials['playlist_id'] = input('Deezer playlist ID: ')
    with open(PATH, 'w') as f:
        json.dump(credentials, f)


def get_token():
    """Return Deezer API access token."""
    return read_credentials()['token']


def get_playlist_id():
    """Return Billboard Hot 100 playlist ID."""
    return read_credentials()['playlist_id']


def read_credentials():
    """Return credentials."""
    if not os.path.isfile(PATH):
        configure()
    with open(PATH) as f:
        return json.load(f)

