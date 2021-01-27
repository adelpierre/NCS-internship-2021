cmake_minimum_required(VERSION 3.0.2)
project(rh_ball_plugin)

## Add support for C++11, supported in ROS Kinetic and newer
add_definitions(-std=c++11)

# Load catkin and all dependencies required for this package
find_package(catkin REQUIRED COMPONENTS 
  roscpp 
  gazebo_ros 
)

# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

# For example_world_plugin plugin
add_library(rh_ball_simple_world_plugin src/simple_world_plugin.cpp)
target_link_libraries(rh_ball_simple_world_plugin ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

# For rh_ball_plugin plugin
add_library(rh_ball_model_push_plugin src/model_push.cc)
target_link_libraries(rh_ball_model_push_plugin ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

catkin_package(
  DEPENDS 
    roscpp 
    gazebo_ros 
)
