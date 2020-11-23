
"""
Repository
==========

A data source - database, cache, list of checks, etc.
"""

import os
import posix
import sqlite3
import time
from typing import Union, List
from .model import ExecutedCheckResult
from pickle import loads as deserialize, dumps as serialize
from threading import RLock


class Repository:
    """
    Provides data fetching and caching mechanism
    """

    checks_dirs: list
    configured_dirs: list
    db: sqlite3.Connection
    db_lock: RLock

    def __init__(self, project_dirs: list, db_path: str = '~/.infracheck.sqlite3'):
        self.checks_dirs = []
        self.configured_dirs = []
        self.db_path = db_path
        self.db_lock = RLock()
        self._connect_to_db(db_path)

        for path in project_dirs:
            self.checks_dirs.append(path + '/checks')
            self.configured_dirs.append(path + '/configured')

    def _connect_to_db(self, db_path: str):
        self.db = sqlite3.connect(os.path.expanduser(db_path), check_same_thread=False)

        try:
            self._execute(
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
            self._execute('CREATE INDEX check_name_index ON checks_cache(check_name);')
        except sqlite3.OperationalError:
            pass

        self.db.commit()

    def get_configured_checks(self, with_disabled: bool = False) -> List[str]:
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

    def get_available_checks(self) -> List[str]:
        results = []

        for path in self.checks_dirs:
            available_checks = os.scandir(path)

            def map_checks_to_name(check: posix.DirEntry):
                return str(check.name)

            results += map(map_checks_to_name, available_checks)

        return list(set(results))

    def _purge_cache(self, check_name: str):
        self._execute('DELETE FROM checks_cache WHERE check_name = ?', [check_name])

    def push_to_cache(self, check_name: str, data: ExecutedCheckResult):
        self._purge_cache(check_name)

        self._execute(
            '''
                INSERT INTO checks_cache (id, check_name, data, date_added)
                VALUES (NULL, ?, ?, ?);
            ''',
            [check_name, serialize(data), time.time()]
        )

        self.db.commit()

    def _execute(self, query: str, parameters = None):
        if parameters is None:
            parameters = []

        with self.db_lock:
            return self.db.execute(query, parameters)

    def retrieve_from_cache(self, check_name: str) -> Union[ExecutedCheckResult, None]:
        cursor = self._execute('SELECT data, date_added FROM checks_cache WHERE check_name = ? ' +
                               'ORDER BY date_added DESC LIMIT 1', [check_name])
        data = cursor.fetchone()

        if not data:
            return None

        try:
            return deserialize(data[0])
        except:
            return None
