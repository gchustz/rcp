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
    cpu.msg
    cpucore.msg
    cputimes.msg
    disks.msg 
    diskpartition.msg

)

# Generate messages
generate_messages(
    DEPENDENCIES
    rcp
)

# Catkin specific configuration
catkin_package(
   CATKIN_DEPENDS message_runtime std_msgs)


include_directories()