import base64
import urllib
import requests

from secrets import SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN

WHATSSLAP_URI = '4sII1rJjdgAQjhCQdZDOdL'

class Spotify(object):

    client_id = '8b4dd715add448f1b0ef8e3bc46bf3d3'
    client_secret = SPOTIFY_CLIENT_SECRET
    api_host = 'https://api.spotify.com'
    redirect_uri = 'http://wpercy.ngrok.io/auth/spotify/callback'
    scopes = 'playlist-modify-public playlist-read-collaborative'

    @classmethod
    def get_redirect_url(cls):
        _url = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}&scope={}'
        url = _url.format(cls.client_id, cls.redirect_uri, cls.scopes)

        return url

    @classmethod
    def exchange_auth_code(cls, code):
        url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': cls.redirect_uri,
            'client_id': cls.client_id,
            'client_secret': cls.client_secret
        }

        _r = requests.post(url, data=data)

        if _r.status_code != 200:
            raise Exception(_r.content)

        return _r.json()

    @classmethod
    def exchange_refresh_token(cls, refresh_token):
        url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': cls.client_id,
            'client_secret': cls.client_secret
        }

        _r = requests.post(url, data=data)

        if _r.status_code != 200:
            raise Exception(_r.content)

        print _r.json()

        return _r.json()


    @classmethod
    def add_song_to_playlist(cls, token, playlist_uri, song_uri):
        url = cls.api_host + '/v1/playlists/{}/tracks?uris={}'.format(urllib.quote(playlist_uri),urllib.quote(song_uri))

        _r = cls.spotify_post(url, token)

        print _r.status_code, _r.json()
        return _r.json()

    @classmethod
    def add_song_to_whatsslap(cls, token, song_uri):
        return cls.add_song_to_playlist(token, WHATSSLAP_URI, song_uri)


    @classmethod
    def spotify_get(cls, url, token):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        _r = requests.get(url, headers=headers)

        if _r.status_code == 401:
            creds = cls.exchange_refresh_token(SPOTIFY_REFRESH_TOKEN)
            _r = cls.spotify_post(url, creds['access_token'], data)

        return _r


    @classmethod
    def spotify_post(cls, url, token, data=None):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        _r = requests.post(url, data=data, headers=headers)

        import ipdb;ipdb.set_trace()

        if _r.status_code == 401:
            creds = cls.exchange_refresh_token(SPOTIFY_REFRESH_TOKEN)
            _r = cls.spotify_post(url, creds['access_token'], data)

        return _r


