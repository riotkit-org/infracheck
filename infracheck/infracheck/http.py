
"""
HTTP
====

Exposes simple HTTP endpoint with JSON response
"""

import tornado.ioloop
import tornado.web
import json
from .controller import Controller
from .model import ExecutedChecksResultList


class CheckExposingHandler(tornado.web.RequestHandler):  # pragma: no cover
    app: Controller

    def get(self):
        result: ExecutedChecksResultList = self.app.retrieve_checks()

        self.set_status(500 if not result.is_global_status_success() else 200)
        self.add_header('Content-Type', 'application/json')
        self.write(
            json.dumps(result.to_hash(), sort_keys=True, indent=4, separators=(',', ': '))
        )

    def data_received(self, chunk):
        pass


class VersionHandler(tornado.web.RequestHandler):  # pragma: no cover
    app: Controller

    def get(self):
        self.set_status(200)
        self.add_header('Content-Type', 'application/json')
        self.write(
            json.dumps(self.app.get_version(), sort_keys=True, indent=4, separators=(',', ': '))
        )

    def data_received(self, chunk):
        pass


class HttpServer(object):
    app = None
    port: int
    path_prefix: str

    def __init__(self, app: Controller, port: int, server_path_prefix: str):
        self.app = app
        self.port = port
        self.path_prefix = server_path_prefix

    def run(self):
        CheckExposingHandler.app = self.app
        VersionHandler.app = self.app

        srv = tornado.web.Application([
            (r"" + self.path_prefix + "/", CheckExposingHandler),
            (r"" + self.path_prefix + "/version", VersionHandler)
        ])

        srv.listen(self.port)
        tornado.ioloop.IOLoop.current().start()
