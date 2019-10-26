
import subprocess
from typing import Union, Tuple


class SSH:
    user: str
    port: int
    host: str
    ssh_opts: str
    ssh_bin: str
    timeout: int
    sshpass_bin: str

    def __init__(self, user: str, port: int, host: str, ssh_opts: str, private_key: str,
                 ssh_bin: str, password: str, timeout: int, sshpass_bin: str):
        self.user = user
        self.port = port
        self.host = host
        self.ssh_opts = ssh_opts
        self.ssh_bin = ssh_bin
        self.password = password
        self.timeout = timeout
        self.sshpass_bin = sshpass_bin

        if private_key:
            self.ssh_opts += ' -i %s' % private_key

    def execute(self, remote_command: Union[str, list]) -> Tuple[str, int]:
        local_command = [self.ssh_bin]

        if self.password:
            local_command = [self.sshpass_bin, '-p', self.password] + local_command

        if self.ssh_opts:
            local_command += self.ssh_opts.split(' ')

        local_command += [
            '-p', str(self.port),
            self.user + '@' + self.host
        ]

        if type(remote_command) == str:
            local_command.append(remote_command)
        else:
            local_command += remote_command

        try:
            out = subprocess.check_output(local_command, stderr=subprocess.STDOUT, timeout=self.timeout).decode('utf-8')
            exit_code = 0
        except subprocess.CalledProcessError as e:
            out = e.output.decode('utf-8')
            exit_code = e.returncode

        return out, exit_code
