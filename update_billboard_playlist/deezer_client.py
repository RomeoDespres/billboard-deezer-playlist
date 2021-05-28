import json
import requests


class DeezerClient:

    """Deezer API client.

    Parameters
    ----------
    token : str, optional
        API access token for authenticated requests. If None,
        authenticated requests will raise an AssertionError.
        Default: None.
    """

    def __init__(self, token=None):
        self.token = token
        self.base = "https://api.deezer.com/"

    def add_to_playlist(self, playlist_id, track_ids):
        """Add tracks to a playlist (requires authentication)."""
        request = "playlist/{}/tracks".format(playlist_id)
        params = {"request_method": "POST", "songs": ",".join(track_ids)}
        self.request(request, authenticated=True, **params)

    def clear_playlist(self, playlist_id):
        """Remove all tracks in a playlist."""
        track_ids = self.get_track_ids_in_playlist(playlist_id)
        self.delete_from_playlist(playlist_id, track_ids)

    def delete_from_playlist(self, playlist_id, track_ids):
        """Remove tracks from a playlist (requires authentication)."""
        request = "playlist/{}/tracks".format(playlist_id)
        params = {"request_method": "DELETE", "songs": ",".join(track_ids)}
        self.request(request, authenticated=True, **params)

    def get_track_ids_in_playlist(self, playlist_id):
        """Return list of IDs of the tracks in a playlist."""
        tracks = self.request("playlist/{}".format(playlist_id))["tracks"]
        return [str(track["id"]) for track in tracks["data"]]

    def request(self, request="", authenticated=False, **params):
        url = "/".join([self.base, request])
        params["output"] = "json"
        if authenticated:
            assert self.token is not None, "No access token provided"
            params["access_token"] = self.token
        return json.loads(requests.get(url, params).text)

    def search_track(self, track):
        """Return search results for a given track name."""
        return self.request("search", q='track:"{}"'.format(track))["data"]
