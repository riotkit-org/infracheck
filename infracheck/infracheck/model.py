from datetime import datetime, timedelta
from typing import Dict, List, Union, Optional
from dataclasses import dataclass
from croniter import croniter
from rkd.api.inputoutput import IO

QUIET_PERIODS_DATA_STRUCT = List[Dict[str, Union[str, int]]]
HOOKS_STRUCT = Dict[str, List[str]]
INPUT_VARIABLES_STRUCT = Dict[str, Union[str, int]]


@dataclass
class ConfiguredCheck(object):
    name: str
    check_type: str  # type
    description: str
    input_variables: INPUT_VARIABLES_STRUCT
    hooks: HOOKS_STRUCT
    quiet_periods: QUIET_PERIODS_DATA_STRUCT
    results_cache_time: Optional[int]
    io: IO

    @classmethod
    def from_config(cls, name: str, config: dict, io: IO):
        quiet_periods = config.get('quiet_periods', [])

        if quiet_periods:
            for period in quiet_periods:
                period: dict
                if "starts" not in period or "duration" not in period:
                    # todo: exception class
                    raise Exception(
                        '"quiet_periods" contains invalid structure. Valid entry example: '
                        '{"starts": "30 00 * * *", "duration": 60}'
                    )

        # cache life time is disabled
        if "results_cache_time" not in config or not config.get('results_cache_time'):
            io.debug('results_cache_time not configured for {}'.format(name))

        # todo: exception class
        if not isinstance(quiet_periods, list):
            raise Exception('"quiet_periods" should be a list')

        return cls(
            name=name,
            check_type=config.get('type'),
            description=config.get('description', ''),
            input_variables=config.get('input', {}),
            hooks=config.get('hooks', {}),
            quiet_periods=quiet_periods,
            results_cache_time=int(config.get('results_cache_time')) if "results_cache_time" in config else None,
            io=io
        )

    def should_status_be_ignored(self) -> bool:
        """
        Decides if health check failure status could be ignored in this time
        :return:
        """

        if not self.quiet_periods:
            return False

        for period in self.quiet_periods:
            period: dict
            if "starts" not in period or "duration" not in period:
                continue

            last_execution = croniter(period.get('starts'), start_time=self._time_now()).get_prev(ret_type=datetime)
            duration = timedelta(minutes=int(period.get('duration')))
            current_time = self._time_now()

            self.io.debug(f'Quiet hours: last_execution={last_execution}, duration={duration}')

            # happening NOW
            if last_execution + duration >= current_time:
                self.io.debug('Quiet hours started')
                return True

        return False

    @staticmethod
    def _time_now() -> datetime:
        return datetime.now()

    def should_check_run(self, last_cache_write_time: Optional[datetime]) -> bool:
        if not self.results_cache_time:
            return True

        cache_lifetime_seconds = timedelta(seconds=self.results_cache_time)

        if not last_cache_write_time:
            self.io.debug('No last cache write time for {}'.format(self.name))
            return True

        return last_cache_write_time + cache_lifetime_seconds <= datetime.now()


class ExecutedCheckResult(object):
    """
    Represents a single result of a single check
    """

    output: str
    exit_status: bool
    hooks_output: str
    configured_name: str
    refresh_time: datetime
    description: str
    is_silenced: bool

    def __init__(self, configured_name: str, output: str, exit_status: bool, hooks_output: str,
                 description: str, is_silenced: bool):

        self.configured_name = configured_name
        self.output = output
        self.exit_status = exit_status
        self.hooks_output = hooks_output
        self.refresh_time = datetime.now()
        self.description = description
        self.is_silenced = is_silenced

    @classmethod
    def from_not_ready(cls, configured_name: str, description: str):
        check = cls(
            configured_name=configured_name,
            output='Check not ready',
            exit_status=False,
            hooks_output='',
            description=description,
            is_silenced=False
        )

        check.refresh_time = None

        return check

    def to_hash(self) -> dict:
        return {
            'status': self.exit_status,
            'output': self.output,
            'description': self.description,
            'hooks_output': self.hooks_output,
            'ident': self.configured_name + '=' + str(self.exit_status),
            'checked_at': self.refresh_time.strftime('%Y-%m-%d %H-%M-%S') if self.refresh_time else '',
            'silenced': f'silenced={self.is_silenced}'
        }


class ExecutedChecksResultList(object):
    checks: Dict[str, ExecutedCheckResult]

    def __init__(self):
        self.checks = {}

    def add(self, config_name: str, result: ExecutedCheckResult) -> None:
        self.checks[config_name] = result

    def to_hash(self) -> dict:
        checks_as_hash = {}

        for name, details in self.checks.items():
            checks_as_hash[name] = details.to_hash()

        return {
            'checks': checks_as_hash,
            'global_status': self.is_global_status_success()
        }

    def is_global_status_success(self) -> bool:
        for name, details in self.checks.items():
            if not details.exit_status:
                return False

        return True
