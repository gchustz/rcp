#!/usr/bin/env python3

import psutil
import fnmatch
from collections import namedtuple
from dataclasses import dataclass
import re

# Globals
# DISK_NAME_LABEL = 'name'
KEY_PARTITIONS = 'partitions'
RE_PATTERN_PARTITION_DEVICES = re.compile(
    "^(\/dev/\d([a-z])([0-9]+)|\/dev\/nvme([0-9]+)n([0-9]+)p([0-9]+))$")

DUPLEX_STRS = {
    psutil.NIC_DUPLEX_UNKNOWN: 'unknown',
    psutil.NIC_DUPLEX_FULL: 'full',
    psutil.NIC_DUPLEX_HALF: 'half'
}

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

ZEROED_IO_COUNTERS = psutil._pslinux.pio(
    read_count=0, write_count=0, read_bytes=0, write_bytes=0, read_chars=0, write_chars=0)
ZEROED_MEM_INFO = psutil._pslinux.pmem(
    rss=0, vms=0, shared=0, text=0, lib=0, data=0, dirty=0)

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

# Data classes


@dataclass
class CpuCore:
    percent_usage: float
    mode_times: namedtuple
    mode_usages: namedtuple


@dataclass
class Cpu:
    percent_usage: float
    logical_count: int
    physical_count: int
    ctx_switches: int
    interrupts: int
    soft_interrupts: int
    syscalls: int
    cpus: list


@dataclass
class DiskPartition:
    device: str
    mountpoint: str
    percent: float
    total: int
    used: int
    free: int
    fstype: str
    opts: str
    maxfile: int
    maxpath: int


@dataclass
class Disk:
    name: str
    read_count: int
    write_count: int
    read_bytes: int
    write_bytes: int
    read_time: int
    write_time: int
    read_merged_count: int
    write_merged_count: int
    busy_time: int
    partitions: list


@dataclass
class NIC:
    name: str
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int
    isup: bool
    duplex: str
    speed: int
    mtu: int
    flags: str


@dataclass
class SystemPerf:
    cpu: Cpu
    memory: namedtuple
    swap: namedtuple
    disks: list
    network_interfaces: list
    temperature_sensors: list


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

# Helper functions:


def namedtuple_to_dict(namedtuple):
    return dict(namedtuple._asdict())


def get_cpu_info():
    # Reference: https://psutil.readthedocs.io/en/latest/#cpu

    # Gather measurements
    _stats = psutil.cpu_stats()
    _phys_count = psutil.cpu_count(logical=False)
    _log_count = psutil.cpu_count(logical=True)
    _cpu_times = psutil.cpu_times(percpu=True)
    _cpu_times_percent = psutil.cpu_times_percent(percpu=True)
    _cpu_percents = psutil.cpu_percent(percpu=True)
    _overall_percent_usage = sum(_cpu_percents) / len(_cpu_percents)

    # Build list of individual logical cpus
    _cpus = [CpuCore(percent_usage=percent_usage, mode_times=times, mode_usages=usages)
             for percent_usage, times, usages in zip(_cpu_percents, _cpu_times, _cpu_times_percent)]

    # Construct the cpu data object
    ret = Cpu(
        percent_usage=_overall_percent_usage,
        logical_count=_log_count,
        physical_count=_phys_count,
        ctx_switches=_stats.ctx_switches,
        interrupts=_stats.interrupts,
        soft_interrupts=_stats.soft_interrupts,
        syscalls=_stats.syscalls,
        cpus=_cpus
    )

    return ret


def get_disk_info(*device_exclusions):
    # Device exclusions should be written in a way that abide by fnmatch.fnmatch if is indentend match (i.e. *loop* for /dev/loop3000)

    # Create a list of disk io
    disks_dict = {}
    _disk_ios = psutil.disk_io_counters(perdisk=True)
    for disk_device_name, disk_io in _disk_ios.items():
        include = True
        for device_exclusion in device_exclusions:
            if fnmatch.fnmatch(disk_device_name, device_exclusion):
                include = False
                break

        # Now exclude the sdax or nvme0n0px for devices
        # Note, this will break loopxx if you want to maintain that functionality

        if include and RE_PATTERN_PARTITION_DEVICES.match(disk_device_name):
            include = False

        if include:
            disks_dict[disk_device_name] = namedtuple_to_dict(disk_io)
            # Empty list to house any partitions found in the following steps
            disks_dict[disk_device_name][KEY_PARTITIONS] = []

    # Create a list of partitions inside each device with matching names
    _partitions = psutil.disk_partitions()
    for device_name, disk_info in disks_dict.items():
        match_name = '*' + device_name + '*'
        for partition in _partitions:
            if fnmatch.fnmatch(partition.device, match_name):
                _partition_dict = namedtuple_to_dict(partition)
                _partition_usage = psutil.disk_usage(partition.mountpoint)
                _partition_usage = namedtuple_to_dict(_partition_usage)

                disk_info[KEY_PARTITIONS].append(
                    DiskPartition(**_partition_dict, **_partition_usage)
                )

                _partitions.remove(partition)

    # Create disk objects
    disks = []
    for disk_device_name, disk_info in disks_dict.items():
        disks.append(
            Disk(name=disk_device_name, **disk_info)
        )

    return disks


def get_nic_info(*nic_exclusions):
    nics = []

    _nic_stats = psutil.net_if_stats()
    _nic_ios = psutil.net_io_counters(pernic=True)

    _nic_keys = [key for key in _nic_stats if key in _nic_ios]

    for nic_name in _nic_keys:
        include = True
        for nic_exclusion in nic_exclusions:
            if fnmatch.fnmatch(nic_name, nic_exclusion):
                include = False
                break

        if include:
            _nic_stats_dict = namedtuple_to_dict(_nic_stats[nic_name])
            _nic_io_dict = namedtuple_to_dict(_nic_ios[nic_name])
            # Correct the duplex
            _nic_stats_dict['duplex'] = DUPLEX_STRS[_nic_stats_dict['duplex']]

            nics.append(
                NIC(name=nic_name, **_nic_io_dict, **_nic_stats_dict)
            )

    return nics


def get_system_perf_info(disk_device_exlusions: list, nic_exclusions: list):
    return SystemPerf(
        cpu=get_cpu_info(),
        memory=psutil.virtual_memory(),
        swap=psutil.swap_memory(),
        disks=get_disk_info(*disk_device_exlusions),
        network_interfaces=get_nic_info(*nic_exclusions),
        temperature_sensors=[]  # TODO: add this functionality back when on actual baremetal
    )


def make_process(**process_dict):
    for key in NONE_TO_BLANK:
        process_dict[key] = '' if process_dict[key] is None else process_dict[key]

    process_dict[KEY_NUM_FDS] = 0 if process_dict[KEY_NUM_FDS] is None else process_dict[KEY_NUM_FDS]
    process_dict[KEY_IO_COUNTERS] = ZEROED_IO_COUNTERS if process_dict[KEY_IO_COUNTERS] is None else process_dict[KEY_IO_COUNTERS]
    process_dict[KEY_ENVIRON] = {
    } if process_dict[KEY_ENVIRON] is None else process_dict[KEY_ENVIRON]
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
    print(get_cpu_info())
    print()
    print(get_disk_info('*loop*'))
    print()
    print(get_nic_info('*lo*'))
    print()


if __name__ == '__main__':
    main()
