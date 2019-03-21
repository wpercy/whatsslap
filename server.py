
import tornado
import tornado.autoreload
from tornado.ioloop import IOLoop
from tornado.options import define, options

from handlers import WhatsAppHookHandler, IndexHandler

import os

define('port', default=8888, help='port to listen on')

def main():

    dirname = os.path.dirname(os.path.realpath(__file__))

    app = tornado.web.Application([
        ('/', IndexHandler),
        ('/whatsapp/hook', WhatsAppHookHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)

    tornado.autoreload.watch('.')
    IOLoop.current().start()


if __name__ == '__main__':
    main()
