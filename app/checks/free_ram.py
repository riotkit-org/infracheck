#!/usr/bin/env python3

import re
from os import environ
from sys import stderr

if 'MAX_RAM_PERCENTAGE' not in environ:
    print("Missing MAX_RAM_PERCENTAGE parameter.\nUsage ./free_ram.py.", file=stderr)
    exit(127)

def check_ram(meminfopath, maxPercent):
    meminfo = open(meminfopath).read()
    memTotalreg = re.compile("MemTotal:\s+(\d+)")
    memAvailreg = re.compile("MemAvailable:\s+(\d+)")
    memTotal = float( memTotalreg.split(meminfo)[1] )
    memAvail = float( memAvailreg.split(meminfo)[1] )
    if "MOCK_FREE_RAM" in environ and "MOCK_TOTAL_RAM" in environ:
        memAvail = float(environ["MOCK_FREE_RAM"]) * 1024
        memTotal = float(environ["MOCK_TOTAL_RAM"]) * 1024
    memUsed = memTotal - memAvail
    memUsedPercent = memUsed/memTotal * 100
    if memUsed/memTotal * 100 > maxPercent:
        print("RAM usage too high: {0:.0f}MiB/{1:.0f}MiB ({2:.0f}% used, {3:.0f}MiB left. Max usage allowed: {4:.0f}% ({5:.0f}MiB)".format(memUsed/1024, memTotal/1024, memUsedPercent, memAvail/1024, maxPercent, maxPercent/100.0 * memTotal/1024 ))
        return 1
    print("RAM usage OK: {0:.0f}MiB/{1:.0f}MiB ({2:.0f}% used, {3:.0f}MiB left. Max usage allowed: {4:.0f}% ({5:.0f}MiB)".format(memUsed/1024, memTotal/1024, memUsedPercent, memAvail/1024, maxPercent, maxPercent/100.0 * memTotal/1024 ))
    return 0


exit(check_ram("/proc/meminfo", float(environ["MAX_RAM_PERCENTAGE"])))
