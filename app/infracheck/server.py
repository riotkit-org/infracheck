
import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    app = None

    def get(self):
        result = self.app.perform_checks()
        self.set_status(500 if not result['status'] else 200)
        self.add_header('Content-Type', 'application/json')
        self.write(
            json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
        )

    def data_received(self, chunk):
        pass


class HttpServer:
    app = None
    port = 7422

    def __init__(self, app, port: int):
        self.app = app
        self.port = port

    def run(self):
        MainHandler.app = self.app

        srv = tornado.web.Application([(r"/", MainHandler)])
        srv.listen(self.port)
        tornado.ioloop.IOLoop.current().start()
