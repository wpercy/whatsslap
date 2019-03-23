
import tornado
import tornado.autoreload
from tornado.ioloop import IOLoop
from tornado.options import define, options

from handlers import WhatsAppHookHandler, IndexHandler, SpotifyAuthHandler, SpotifyCallbackHandler

from spotify import Spotify
from whatsapp import WhatsApp

import os

define('port', default=8888, help='port to listen on')

def main():

    dirname = os.path.dirname(os.path.realpath(__file__))

    spotify = Spotify()
    whatsapp = WhatsApp()

    app = tornado.web.Application([
        ('/', IndexHandler),
        ('/whatsapp/hook', WhatsAppHookHandler, dict(spotify=spotify)),
        ('/auth/spotify/callback', SpotifyCallbackHandler, dict(spotify=spotify)),
        ('/auth/spotify', SpotifyAuthHandler, dict(spotify=spotify)),
    ],
        autoreload=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
