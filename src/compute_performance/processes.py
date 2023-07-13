#!/usr/bin/env python3

import psutil
from collections import namedtuple
from dataclasses import dataclass

# Global
PROCESS_ATTRS = [
    'pid',
    'ppid',
    'name',
    'exe',
    'cmdline',
    'environ',
    'create_time',
    'status',
    'cwd',
    'username',
    'uids',
    'gids',
    'terminal',
    'nice',
    'ionice',
    'io_counters',
    'num_ctx_switches',
    'num_fds',
    'num_threads',
    'threads',
    'cpu_times',
    'cpu_percent',
    'cpu_affinity',
    'cpu_num',
    'memory_info',
    'connections'
]

@dataclass
class Process:
    name: str  
    username: str
    pid: int
    ppid: int
    status: str
    cpu_percent: float
    memory_percent: float
    create_time: float
    exe: str
    cmdline: list 
    terminal: str
    environ: str
    cwd: str
    nice: int 
    ionice: int
    cpu_num: int
    num_threads: int
    cpu_affinity: list 
    ctx_switches_voluntary: int
    ctx_switches_involuntary: int
    cpu_times: namedtuple
    memory_info: namedtuple
    threads: list
    uids_real: int
    uids_effective: int
    uids_saved: int
    gids_real: int
    gids_effective: int
    gids_saved: int

def main():
    min_idx = 200
    max_idx = 200
    idx = 0
    for proc in psutil.process_iter(attrs=PROCESS_ATTRS):
        if idx >= min_idx:
            print(proc.as_dict())
            print()

        if idx >= max_idx:
            break

        idx += 1

if __name__ == '__main__':
    main()