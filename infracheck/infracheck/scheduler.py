
"""
Scheduler
=========

Schedules execution of health checks verification every X seconds.
"""
import time
from threading import Thread
from traceback import format_exc
from .repository import Repository
from .runner import Runner
from rkd.api.inputoutput import IO


class Scheduler(object):
    runner: Runner
    thread: Thread
    repository: Repository
    io: IO

    def __init__(self, runner: Runner, repository: Repository, io: IO):
        self.runner = runner
        self.repository = repository
        self.io = io

    def schedule_jobs_in_background(self, every_seconds: int):
        self.thread = Thread(target=self._run_checks_infinitely, args=(self, every_seconds))
        self.thread.setDaemon(True)
        self.thread.start()

    def _run_checks_infinitely(self, scheduler, every_seconds: int):
        while True:
            try:
                configured_checks = self.repository.get_configured_checks(with_disabled=False)

                self.io.info('Running {} checks...'.format(len(configured_checks)))
                self.runner.run_checks(configured_checks)

            except Exception:
                self.io.error('Exception happened during processing')
                self.io.error(format_exc())

            self.io.debug('Sleeping {}s'.format(every_seconds))
            time.sleep(every_seconds)
