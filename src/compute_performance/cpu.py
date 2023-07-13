#!/usr/bin/env python3
from dataclasses import dataclass
import psutil
from collections import namedtuple


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


def get_cpu_stats():
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


def main():
    print(get_cpu_stats())


if __name__ == '__main__':
    main()
