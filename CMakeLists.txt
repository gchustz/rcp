cmake_minimum_required(VERSION 2.8.3)

project(rcp)

# Catkin library
find_package(catkin REQUIRED COMPONENTS
             message_generation
             std_msgs)

# Run setup.py
catkin_python_setup()

# Generate messages in the 'msg' directory
add_message_files(
    DIRECTORY msg
    FILES 
    KeyValue.msg
    Cpu.msg
    CpuCore.msg
    CpuTimes.msg
    Memory.msg
    Swap.msg
    Disk.msg 
    DiskPartition.msg
    NetworkInterface.msg
    TemperatureSensor.msg
    ProcessMemInfo.msg
    ProcessIoCounters.msg
    ProcessCpuTimes.msg
    Thread.msg
    Process.msg
    ProcessArray.msg
    SystemPerf.msg
    NvidiaGpuProcess.msg
    NvidiaGpuDevice.msg
    NvidiaGpuSystem.msg
)

# Generate messages
generate_messages(
    DEPENDENCIES
    std_msgs
    rcp
)

# Catkin specific configuration
catkin_package(
   CATKIN_DEPENDS message_runtime std_msgs)


include_directories()