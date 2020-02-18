
import os
import posix
import sqlite3
import json
import time


class Repository:
    checks_dirs: list
    configured_dirs: list
    db: sqlite3.Connection

    def __init__(self, project_dirs: list, db_path: str = '~/.infracheck.sqlite3'):
        self.checks_dirs = []
        self.configured_dirs = []
        self._connect_to_db(db_path)

        for path in project_dirs:
            self.checks_dirs.append(path + '/checks')
            self.configured_dirs.append(path + '/configured')

    def _connect_to_db(self, db_path: str):
        self.db = sqlite3.connect(os.path.expanduser(db_path))

        try:
            self.db.execute(
                '''
                    CREATE TABLE checks_cache (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        check_name TEXT, 
                        data TEXT, 
                        date_added TEXT
                    );
                '''
            )
        except sqlite3.OperationalError:
            pass

        try:
            self.db.execute('CREATE INDEX check_name_index ON checks_cache(check_name);')
        except sqlite3.OperationalError:
            pass

        self.db.commit()

    def get_configured_checks(self, with_disabled=False):
        found = []

        for path in self.configured_dirs:
            if not os.path.isdir(path):
                continue

            configurations = os.scandir(path)

            for entry in configurations:
                if not with_disabled and not entry.name.endswith('.json'):
                    continue
                elif with_disabled and not (entry.name.endswith('.disabled') or entry.name.endswith('.json')):
                    continue

                found.append(os.path.splitext(entry.name)[0].replace('.json', ''))

        return list(set(found))

    def get_available_checks(self):
        results = []

        for path in self.checks_dirs:
            available_checks = os.scandir(path)

            def map_checks_to_name(check: posix.DirEntry):
                return str(check.name)

            results += map(map_checks_to_name, available_checks)

        return list(set(results))

    def _purge_cache(self, check_name: str):
        self.db.execute('DELETE FROM checks_cache WHERE check_name = ?', [check_name])

    def push_to_cache(self, check_name: str, data):
        self._purge_cache(check_name)
        self.db.execute(
            '''
                INSERT INTO checks_cache (id, check_name, data, date_added)
                VALUES (NULL, ?, ?, ?);
            ''',
            [check_name, json.dumps(data), time.time()]
        )

        self.db.commit()

    def retrieve_cache(self, check_name: str):
        cursor = self.db.execute('SELECT data FROM checks_cache WHERE check_name = ?', [check_name])
        data = cursor.fetchone()

        if not data:
            return None

        try:
            return json.loads(data[0])
        except:
            return None
