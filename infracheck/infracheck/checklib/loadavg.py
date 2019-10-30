
import abc
import os
import re


class BaseLoadAverageCheck(abc.ABC):
    @staticmethod
    def get_complete_avg() -> str:
        avg = os.getloadavg()
        return '{:.2f}, {:.2f}, {:.2f}'.format(avg[0], avg[1], avg[2])

    @staticmethod
    def get_load_average(timing: str) -> float:
        if os.getenv('MOCK_LOAD_AVERAGE'):
            return float(os.getenv('MOCK_LOAD_AVERAGE'))

        if timing not in ['1', '5', '15']:
            raise Exception('Invalid argument, expected type to be: 1, 5 or 15')

        load = {'1': os.getloadavg()[0], '5': os.getloadavg()[1], '15': os.getloadavg()[2]}
        return load[timing]

    @staticmethod
    def available_cpu_count() -> int:
        """ Number of available virtual or physical CPUs on this system, i.e.
        user/real as output by time(1) when called with an optimally scaling
        userspace-only program

        :url: https://stackoverflow.com/a/1006301/6782994
        """

        if os.getenv('MOCK_CPU_COUNT'):
            return int(os.getenv('MOCK_CPU_COUNT'))

        # cpuset
        # cpuset may restrict the number of *available* processors
        try:
            with open('/proc/self/status') as f:
                m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$', f.read())

                if m:
                    res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
                    if res > 0:
                        return int(res)
        except IOError:
            pass

        # Python 2.6+
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass

        # Linux
        try:
            with open('/proc/cpuinfo') as f:
                res = f.read().count('processor\t:')

                if res > 0:
                    return int(res)
        except IOError:
            pass

        raise Exception('Can not determine number of CPUs on this system')