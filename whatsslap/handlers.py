import re
import urlparse

from tornado.web import RequestHandler

from secrets import SPOTIFY_CREDENTIALS

class IndexHandler(RequestHandler):

    def get(self):
        self.write("""
            <html>
                <head><meta charset="UTF-8"></head>
                <body><h1>WhatsSlap &#x1F3B6 &#x1F37B!</h1></body>
            </html>
        """)


class WhatsAppHookHandler(RequestHandler):

    def initialize(self, db=None, spotify=None):
        self.db = db
        self.spotify = spotify

    def get(self):
        self.set_status(405)
        self.write("method not allowed")
        self.finish()

    def post(self):
        params = dict(urlparse.parse_qsl(self.request.body))
        body = params['Body']
        print body
        match = re.search(r"(https?:\/\/open\.spotify\.com(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?)", body)
        if not match or 'open.spotify.com' not in match.group(0):
            self.write('no link')
            self.finish()
            return

        url = match.group(0)
        song_id = url.split('?')[0].split('/')[-1]
        song_uri = 'spotify:track:{}'.format(song_id)

        _j = self.spotify.add_song_to_whatsslap(SPOTIFY_CREDENTIALS['access_token'], song_uri)

        self.set_status(201)
        self.finish()


class SpotifyAuthHandler(RequestHandler):

    def initialize(self, spotify=None, **kwargs):
        self.spotify = spotify

    def get(self):
        url = self.spotify.get_redirect_url()
        self.redirect(url)


class SpotifyCallbackHandler(RequestHandler):

    def initialize(self, spotify=None, **kwargs):
        self.spotify = spotify

    def get(self):
        code = self.get_argument('code')
        creds = self.spotify.exchange_auth_code(code)

        self.finish()
