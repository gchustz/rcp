#!/usr/bin/env python3

import psutil
from collections import namedtuple
from dataclasses import dataclass

# Global
# Long, but can be used later due to the extensive use of 'None's in the output and the sensitivity of ROS messages to wrong types.
KEY_PID = 'pid'
KEY_PPID = 'ppid'
KEY_NAME = 'name'
KEY_EXE = 'exe'
KEY_CMDLINE = 'cmdline'
KEY_ENVIRON = 'environ'
KEY_CREATE_TIME = 'create_time'
KEY_STATUS = 'status'
KEY_CWD = 'cwd'
KEY_USERNAME = 'username'
KEY_UIDS = 'uids'
KEY_GIDS = 'gids'
KEY_TERMINAL = 'terminal'
KEY_NICE = 'nice'
KEY_IONICE = 'ionice'
KEY_IO_COUNTERS = 'io_counters'
KEY_CTX_SWITCHES = 'num_ctx_switches'
KEY_NUM_FDS = 'num_fds'
KEY_NUM_THREADS = 'num_threads'
KEY_THREADS = 'threads'
KEY_CPU_TIMES = 'cpu_times'
KEY_CPU_PERCENT = 'cpu_percent'
KEY_CPU_AFFINITY = 'cpu_affinity'
KEY_CPU_NUM = 'cpu_num'
KEY_MEM_INFO = 'memory_info'
KEY_CONNECTIONS = 'connections'
KEY_OPEN_FILES = 'open_files'
KEY_MEMORY_MAPS = 'memory_maps'
KEY_MEMORY_FULL_INFO = 'memory_full_info'

PROCESS_ATTRS = [
    KEY_PID,
    KEY_PPID,
    KEY_NAME,
    KEY_EXE,
    KEY_CMDLINE,
    KEY_ENVIRON,
    KEY_CREATE_TIME,
    KEY_STATUS,
    KEY_CWD,
    KEY_USERNAME,
    KEY_UIDS,
    KEY_GIDS,
    KEY_TERMINAL,
    KEY_NICE,
    KEY_IONICE,
    KEY_IO_COUNTERS,
    KEY_CTX_SWITCHES,
    KEY_NUM_FDS,
    KEY_NUM_THREADS,
    KEY_THREADS,
    KEY_CPU_TIMES,
    KEY_CPU_PERCENT,
    KEY_CPU_AFFINITY,
    KEY_CPU_NUM,
    KEY_MEM_INFO
]

NONE_TO_BLANK = [
    KEY_EXE,
    KEY_CMDLINE,
    KEY_CWD,
    KEY_TERMINAL
]

ZEROED_IO_COUNTERS = psutil._pslinux.pio(read_count=0, write_count=0, read_bytes=0, write_bytes=0, read_chars=0, write_chars=0)
ZEROED_MEM_INFO = psutil._pslinux.pmem(rss=0, vms=0, shared=0, text=0, lib=0, data=0, dirty=0)

KEY_CTX_SWITCHES_VOLUNTARY = 'ctx_switches_voluntary'
KEY_CTX_SWITCHES_INVOLUNTARY = 'ctx_switches_involuntary'
KEY_UID_REAL = 'uid_real'
KEY_UID_EFFECTIVE = 'uid_effective'
KEY_UID_SAVED = 'uid_saved'
KEY_GID_REAL = 'gid_real'
KEY_GID_EFFECTIVE = 'gid_effective'
KEY_GID_SAVED = 'gid_saved'

REMOVE_KEYS = [
    KEY_GIDS,
    KEY_UIDS,
    KEY_CTX_SWITCHES,
    KEY_CONNECTIONS,
    KEY_OPEN_FILES,
    KEY_MEMORY_MAPS,
    KEY_MEMORY_FULL_INFO
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
    environ: dict
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
    num_fds: int
    io_counters: namedtuple
    threads: list
    uid_real: int
    uid_effective: int
    uid_saved: int
    gid_real: int
    gid_effective: int
    gid_saved: int

def make_process(**process_dict):
    for key in NONE_TO_BLANK:
        process_dict[key] = '' if process_dict[key] is None else process_dict[key]
    
    process_dict[KEY_NUM_FDS] = 0 if process_dict[KEY_NUM_FDS] is None else process_dict[KEY_NUM_FDS]
    process_dict[KEY_IO_COUNTERS] = ZEROED_IO_COUNTERS if process_dict[KEY_IO_COUNTERS] is None else process_dict[KEY_IO_COUNTERS]
    process_dict[KEY_ENVIRON] = {} if process_dict[KEY_ENVIRON] is None else process_dict[KEY_ENVIRON]
    process_dict[KEY_CTX_SWITCHES_VOLUNTARY] = process_dict[KEY_CTX_SWITCHES].voluntary
    process_dict[KEY_CTX_SWITCHES_INVOLUNTARY] = process_dict[KEY_CTX_SWITCHES].involuntary
    process_dict[KEY_UID_REAL] = process_dict[KEY_UIDS].real
    process_dict[KEY_UID_EFFECTIVE] = process_dict[KEY_UIDS].effective
    process_dict[KEY_UID_SAVED] = process_dict[KEY_UIDS].saved
    process_dict[KEY_GID_REAL] = process_dict[KEY_GIDS].real
    process_dict[KEY_GID_EFFECTIVE] = process_dict[KEY_GIDS].effective
    process_dict[KEY_GID_SAVED] = process_dict[KEY_GIDS].saved
    process_dict[KEY_IONICE] = process_dict[KEY_IONICE].value

    for key in REMOVE_KEYS:
        del process_dict[key]

    return Process(**process_dict)

def get_processes_info():
    return [make_process(**proc_dict.as_dict()) for proc_dict in psutil.process_iter(attrs=PROCESS_ATTRS)]

def main():
    for proc in get_processes_info():
        print(proc)
        print()

if __name__ == '__main__':
    main()