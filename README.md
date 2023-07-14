# RCP - ROS Compute Performance Nodes
This is a ros-wrapper for psutil to provide visibility into the monitoring of compute system resources and individual processes.

*Note: Currently only supporting Linux*

## Installation

`cd <your/workspace>/src/`

`git clone https://github.com/gchustz/rcp` (or `git clone git@github.com:gchustz/rcp` for ssh)

`pip3 install psutil==5.9.5` *Note: Current ros1 / Ubuntu 20.04 build psutil is broken.

*Optional* `pip3 install pynvml=11.5.0`

`cd <your/workspace/>`

`catkin_make`

## Usage
### System Performance
Statistics, usage, and counters for:
- CPU
- Memory
- Swap
- Disks
- Network Interfaces
- (WIP) Temperature Sensors

`roslaunch rcp system_perf.launch`

Which starts topic `/system`

### Process Monitoring
Per process:
- CPU utilization
- Memory
- I/O
- etc.

`roslaunch rcp processes.launch`

Which starts topic `/system/processes`

### NVIDIA GPU Monitoring
Utilization for:
- Gpu processor
- Gpu Memory
- Encoder
- Decoder

Along with other values such as temperature, powerdraw, and per-process information

`roslaunch rcp nvidia_gpu.launch`

Which starts topic `/system/nvidia_gpu`

### All of the above
`roslaunch rcp all.launch`

## Future Plans
- [X] Incorporate NVIDIA GPU statistics
- [ ] Incorporate deeper NVIDIA GPU statistics (i.e. memory temperatures)
- [ ] Add temperature sensors from psutil
- [X] Move Configuration values out to launch file arguments / config files
- [ ] Refactor and move the backend into a separate github
- [ ] Build ROS2 implementation