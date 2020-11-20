
# pragma: no cover

import sys
import os
import argparse
import json
from enum import Enum
from .http import HttpServer

t = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "/../"

if os.path.isdir(t):
    sys.path.insert(0, t)


from .controller import Controller


class LogLevel(Enum):
    info = 'info'
    debug = 'debug'
    warning = 'warning'
    error = 'error'
    fatal = 'fatal'

    def __str__(self):
        return self.value


def main():
    #
    # Arguments parsing
    #
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--list-available-types',
        help='List all available check types that can be used',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--list-all-configurations',
        help='List all configured checks',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--list-enabled-configurations',
        help='List only enabled configurations',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--directory', '-d',
        help='Alternative project directory',
        default=''
    )
    parser.add_argument(
        '--server-port', '-p',
        help='Server port, default is 7422',
        default=7422
    )
    parser.add_argument(
        '--db-path', '-b',
        help='Database path',
        default='~/.infracheck.sqlite3'
    )
    parser.add_argument(
        '--wait', '-w',
        help='Seconds between doing checks',
        default=0
    )
    parser.add_argument(
        '--timeout', '-t',
        help='Timeout for a single healthcheck to execute',
        default=10
    )
    parser.add_argument(
        '--refresh-time', '-r',
        help='Refresh time in seconds - how often perform health checks. Defaults to 120 (seconds) = 2 minutes',
        default=120
    )
    parser.add_argument(
        '--no-server', '-n',
        help='Do not run the server, just run all the checks from CLI',
        action='store_true'
    )
    parser.add_argument(
        '--server-path-prefix',
        help='Optional path prefix to the routing, eg. /this-is-a-secret will make urls looking like: '
             'http://localhost:8000/this-is-a-secret/',
        default=''
    )
    parser.add_argument(
        '--log-level', '-l',
        help='Logging level name - debug, info, warning, error, fatal. Defaults to "info"',
        type=LogLevel,
        choices=list(LogLevel),
        default='info'
    )
    parser.add_argument(
        '--version', '-v',
        help='Get application version',
        action='store_true'
    )

    parsed = parser.parse_args()
    project_dir = parsed.directory if parsed.directory else os.getcwd()
    server_port = int(parsed.server_port if parsed.server_port else 7422)
    server_path_prefix = parsed.server_path_prefix if parsed.server_path_prefix else ''
    wait_time = int(parsed.wait)
    timeout = int(parsed.timeout)

    app = Controller(
        project_dir=project_dir,
        server_port=server_port,
        server_path_prefix=server_path_prefix,
        db_path=parsed.db_path,
        wait_time=wait_time,
        timeout=timeout,
        log_level=str(parsed.log_level)
    )

    if parsed.version:
        print(app.get_version()['version'])
        sys.exit(0)

    # action: --list-all-configurations
    if parsed.list_all_configurations:
        for name in app.list_enabled_configs():
            print(name)

        sys.exit(0)

    # action: --list-available-types
    if parsed.list_available_types:
        for name in app.list_available_checks():
            print(name)

        sys.exit(0)

    # action: --list-enabled-configurations
    if parsed.list_enabled_configurations:
        for name in app.list_all_configs():
            print(name)

        sys.exit(0)

    # action: perform health checking
    if not parsed.no_server:
        app.spawn_threaded_application(refresh_time=int(parsed.refresh_time))
        server = HttpServer(app=app, port=server_port, server_path_prefix=server_path_prefix)
        server.run()

        sys.exit(0)

    if parsed.no_server:
        result = app.perform_checks().to_hash()
        print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))

        if not result['global_status']:
            sys.exit(1)

    sys.exit(0)
