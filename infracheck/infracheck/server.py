
import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):  # pragma: no cover
    app = None
    wait_time = 0
    lazy = False
    force = False

    def get(self):
        result = self.app.perform_checks(force=self.force, wait_time=self.wait_time, lazy=self.lazy)
        self.set_status(500 if not result['global_status'] else 200)
        self.add_header('Content-Type', 'application/json')
        self.write(
            json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
        )

    def data_received(self, chunk):
        pass


class HttpServer:
    app = None
    port: int
    path_prefix: str
    wait_time: int
    lazy: bool
    force: bool

    def __init__(self, app, port: int, server_path_prefix: str, wait_time: int, lazy: bool, force: bool):
        self.app = app
        self.port = port
        self.path_prefix = server_path_prefix
        self.wait_time = wait_time
        self.lazy = lazy
        self.force = force

    def run(self):
        MainHandler.app = self.app
        MainHandler.wait_time = self.wait_time
        MainHandler.lazy = self.lazy
        MainHandler.force = self.force

        srv = tornado.web.Application([(r"" + self.path_prefix + "/", MainHandler)])
        srv.listen(self.port)
        tornado.ioloop.IOLoop.current().start()
