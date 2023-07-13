#!/usr/bin/env python3

import psutil
import fnmatch
from dataclasses import dataclass

# Globals
DUPLEX_STRS = {
    psutil.NIC_DUPLEX_UNKNOWN: 'unknown',
    psutil.NIC_DUPLEX_FULL: 'full',
    psutil.NIC_DUPLEX_HALF: 'half'
}

# Data classes


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
            _nic_stats_dict = dict(_nic_stats[nic_name]._asdict())
            _nic_io_dict = dict(_nic_ios[nic_name]._asdict())

            nics.append(
                NIC(name=nic_name, **_nic_io_dict, **_nic_stats_dict)
            )

    return nics


def main():
    print(get_nic_info('*lo*'))


if __name__ == '__main__':
    main()
