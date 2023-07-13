#!/usr/bin/env python3
import fnmatch
import psutil
from dataclasses import dataclass 
from collections import namedtuple

# Globals
DISK_NAME_LABEL = 'name'
PARTITIONS_LABEL = 'partitions'

# Data class definitions

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

def get_disk_stats(*device_exclusions):
    # Device exclusions should be written in a way that abide by fnmatch.fnmatch if is indentend match (i.e. *loop* for /dev/loop3000)
    
    # Create a list of disk io
    disks_dict = {}
    _disk_ios = psutil.disk_io_counters(perdisk=True)
    for disk_device_name, disk_io in _disk_ios.items():
        include = True
        for device_exclusion in device_exclusions:
            if fnmatch.fnmatch(disk_device_name, device_exclusion):
                include=False 
                break

        if include:
            disks_dict[disk_device_name] = dict(disk_io._asdict())
            disks_dict[disk_device_name][PARTITIONS_LABEL] = [] # Empty list to house any partitions found in the following steps
        

    # Create a list of partitions inside each device with matching names
    _partitions = psutil.disk_partitions()
    for device_name, disk_info in disks_dict.items():
        match_name = '*' + device_name + '*'
        for partition in _partitions:
            if fnmatch.fnmatch(partition.device, match_name):
                _partition_dict = dict(partition._asdict())
                _partition_usage = psutil.disk_usage(partition.mountpoint)
                _partition_usage = dict(_partition_usage._asdict())

                disk_info[PARTITIONS_LABEL].append(
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

def main():
    print(get_disk_stats())

if __name__ == '__main__':
    main()
