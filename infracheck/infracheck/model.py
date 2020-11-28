from datetime import datetime
from typing import Dict


class ExecutedCheckResult(object):
    """
    Represents a single result of a single check
    """

    output: str
    exit_status: bool
    hooks_output: str
    configured_name: str
    refresh_time: datetime

    def __init__(self, configured_name: str, output: str, exit_status: bool, hooks_output: str):
        self.configured_name = configured_name
        self.output = output
        self.exit_status = exit_status
        self.hooks_output = hooks_output
        self.refresh_time = datetime.now()

    @classmethod
    def from_not_ready(cls, configured_name: str):
        check = cls(
            configured_name=configured_name,
            output='Check not ready',
            exit_status=False,
            hooks_output=''
        )

        check.refresh_time = None

        return check

    def to_hash(self) -> dict:
        return {
            'status': self.exit_status,
            'output': self.output,
            'hooks_output': self.hooks_output,
            'ident': self.configured_name + '=' + str(self.exit_status),
            'checked_at': self.refresh_time.strftime('%Y-%m-%d %H-%M-%S') if self.refresh_time else ''
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
