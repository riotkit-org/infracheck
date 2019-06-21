
import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):  # pragma: no cover
    app = None

    def get(self):
        result = self.app.perform_checks()
        self.set_status(500 if not result['global_status'] else 200)
        self.add_header('Content-Type', 'application/json')
        self.write(
            json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
        )

    def data_received(self, chunk):
        pass


class HttpServer:
    app = None
    port = 7422
    path_prefix = ''

    def __init__(self, app, port: int, server_path_prefix: str):
        self.app = app
        self.port = port
        self.path_prefix = server_path_prefix

    def run(self):
        MainHandler.app = self.app

        srv = tornado.web.Application([(r"" + self.path_prefix + "/", MainHandler)])
        srv.listen(self.port)
        tornado.ioloop.IOLoop.current().start()
