import re
import urlparse

from tornado.web import RequestHandler

class IndexHandler(RequestHandler):

    def get(self):
        self.write("""
            <html>
                <head><meta charset="UTF-8"></head>
                <body><h1>WhatsSlap &#x1F3B6 &#x1F37B!</h1></body>
            </html>
        """)


class WhatsAppHookHandler(RequestHandler):

    def get(self):
        self.set_status(405)
        self.write("method not allowed")
        self.finish()

    def post(self):
        params = dict(urlparse.parse_qsl(self.request.body))
        body = params['Body']
        match = re.search(r"(https?:\/\/open\.spotify\.com(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?)", body)
        if not match or 'open.spotify.com' not in match.group(0):
            self.write('no link')
            self.finish()
            return

        url = match.group(0)

        self.set_status(201)
        self.finish()

